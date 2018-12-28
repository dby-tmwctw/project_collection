from collections import defaultdict
from random import random, randrange

### Model

def markov_chain(data, order):
    """
    Create a Markov chain with the given order from the
    given list of data.
    """
    markov_dictionary = {}
    # Look through all states included in data and build dictionary
    for index1 in range(0, len(data) - order):
        element_list = []
        # Create a tuple out of the data
        for index2 in range(0, order):
            element_list.append(data[index1 + index2])
        element_tuple = tuple(element_list)
        # If the tuple is in the dictionary, then read off next
        # value, if not then add a new key and read off next value
        if element_tuple in markov_dictionary.keys():
            markov_dictionary[element_tuple][data[index1 + order]] += 1
        else:
            markov_dictionary[element_tuple] = defaultdict(int)
            markov_dictionary[element_tuple][data[index1 + order]] += 1
    # Loop through all keys, turning numbers into probability
    for key1 in markov_dictionary.keys():
        markov_dictionary[key1] = dict(markov_dictionary[key1])
        total_value = 0
        for key2 in markov_dictionary[key1].keys():
            total_value += markov_dictionary[key1][key2]
        for key3 in markov_dictionary[key1].keys():
            markov_dictionary[key1][key3] = markov_dictionary[key1][key3] / float(total_value)
    return markov_dictionary

#print markov_chain([1, 2, 3, 1, 2, 4], 2)

def compare(dictionary):
    '''
    Randomly return a key in dictionary, the probability of any
    key appearing equals to its value
    '''
    new_list = []
    number = 0
    random_number = random()
    # Turn the dictionary into list
    for key in dictionary.keys():
        new_list.append(tuple([dictionary[key], key]))
        number += 1
    number = 0
    record = 0
    # Check which segment is the random number in
    while True:
        if record >= random_number:
            return new_list[number - 1][1]
        elif number < len(new_list):
            record += new_list[number][0]
            number += 1
        else:
            break
    return 'Error'

#print compare({1:0.2, 3:0.4, 5:0.6, 7:0.8, 9:0.8, 10:0.2})

### Predict

def predict(model, last, num):
    """
    Predict the next num values given the model and the last values.
    """
    total_list = list(last)
    start_number = 0 - len(last)
    time = 0
#    print start_number
#    print total_list
#    print total_list[start_number:]
    # For num times, repeatedly try to predict next state with
    # model
    while time < num:
        time += 1
#        print 'This time, total_list is', total_list
        element_tuple = tuple(total_list[start_number:])
#        print 'This time, element_tuple is', element_tuple
        if element_tuple in model.keys():
#            print 'In dictionary'
#            print 'The number added is', compare(model[element_tuple])
            total_list.append(compare(model[element_tuple]))
        else:
#            print 'Not in dictionary, random number generated'
            total_list.append(randrange(0, 4))
#    print 'In the end, total_list is', total_list
    return_number = 0 - num
    return total_list[return_number:]


#print predict(markov_chain([1, 2, 3, 1, 2, 4], 3), [1, 2, 3], 12)



### Error

def mse(result, expected):
    """
    Calculate the mean squared error between the sequences
    result and expected.
    """
    total_square_sum = 0
    for index1 in range(0, len(result)):
        total_square_sum += (result[index1] - expected[index1]) ** 2
    return total_square_sum / float(len(result))

#print mse([1, 2, 3], [2, 3, 5])


### Experiment

def run_experiment(train, order, test, future, actual, trials):
    """
    Run an experiment to predict the future of the test
    data given the training data.  Returns the average
    mean squared error over the number of trials.

    train  - training data
    order  - order of the markov model to use
    test   - "order" days of testing data
    future - number of days to predict
    actual - actual results for next "future" days
    trials - number of trials to run
    """
    total_mse = 0
    time = 0
    while time < trials:
        time += 1
        total_mse += mse(predict(markov_chain(train, order), test, future), actual)
    return total_mse / float(trials)

#print run_experiment([1, 2, 3, 1, 2, 4, 1, 3, 4, 3, 1, 2, 4, 3], 3, [1, 2, 3], 5, [1, 3, 2, 4, 3], 10)
