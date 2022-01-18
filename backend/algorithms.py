def run_test(data, budget, algorithm):
    #1 Unpack data 
    #2 Pass to right test
    unpacked_data = data
    if algorithm == "mv":
        results = standard_multivariate_test(unpacked_data, budget)
    elif algorithm == 'thompson':
        results = thompson_sampling(unpacked_data, budget)
    elif algorithm == 'epsilon_greedy':
        results = epsilon_greedy(unpacked_data, budget)
    return results

def standard_multivariate_test(data, budget):
    pass


def thompson_sampling(data, budget):
    pass


def epsilon_greedy(data, budget):
    pass


### HELPER FUNCTIONS ###

def calculate_means(unpacked_data):
    pass
