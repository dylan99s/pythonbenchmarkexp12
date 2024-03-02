import time
import cProfile
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import csv

def expression1(n):
    return n * (n - 1) / 2

def expression2(n):
    return (n - 1) * (n / 2)

def benchmark_expression(func, n, iterations=100000):
    start_time = time.perf_counter()
    for _ in range(iterations):
        _ = func(n)
    end_time = time.perf_counter()
    return end_time - start_time

def run_benchmarks(n, iterations):
    times1 = []
    times2 = []
    expr2_faster_iters = []

    for i in range(iterations):
        time1 = benchmark_expression(expression1, n)
        time2 = benchmark_expression(expression2, n)
        
        times1.append(time1)
        times2.append(time2)
        
        if time2 < time1:
            expr2_faster_iters.append(i)
    
    return times1, times2, expr2_faster_iters, n, iterations

def save_and_plot_results(times1, times2, expr2_faster_iters, n, iterations):
    # makes science number normal number
    adjusted_n = int(n)
    mean1, std1 = np.mean(times1), np.std(times1)
    mean2, std2 = np.mean(times2), np.std(times2)
    t_stat, p_value = stats.ttest_ind(times1, times2)


    data_filename = f"{adjusted_n}n{iterations}i_data.csv"
    analysis_filename = f"{adjusted_n}n{iterations}i_analysis.csv"
    
    with open(data_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Iteration', 'Expression 1 Time', 'Expression 2 Time'])
        for i, (time1, time2) in enumerate(zip(times1, times2), 1):
            writer.writerow([i, time1, time2])
    
    with open(analysis_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Statistic', 'Expression 1', 'Expression 2'])
        writer.writerow(['Mean', mean1, mean2])
        writer.writerow(['Standard Deviation', std1, std2])
        writer.writerow(['T-statistic', t_stat, ''])
        writer.writerow(['P-value', p_value, ''])

    print(f"Data saved to {data_filename}")
    print(f"Statistical analysis saved to {analysis_filename}")

    plt.figure(figsize=(10, 6))
    plt.plot(times1, label='n * (n - 1) / 2', marker='o')
    plt.plot(times2, label='(n - 1) * (n / 2)', marker='x')
    plt.title(f'Benchmarking Expressions for n={adjusted_n}')
    plt.xlabel('Iteration')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{adjusted_n}n{iterations}i_figure.pdf")

if __name__ == "__main__":
    # n < or = to 1 need to be written in scientific notation or things get weird

    n = 530
    iterations = 100
    times1, times2, expr2_faster_iters, n, iterations = run_benchmarks(n, iterations)
    cProfile.run('run_benchmarks(n, iterations)', sort='time')
    save_and_plot_results(times1, times2, expr2_faster_iters, n, iterations)
