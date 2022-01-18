import algorithms
import data_gen

def run_experiment(website_list, budget, algorithm):
    website_data = data_gen.generate_data(budget, website_list, 0.1, 0.7, 0.2)
    results = algorithms.run_test(website_data, budget, algorithm)
    return results
