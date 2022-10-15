# abonus.py

# template for Bonus Assignment, Artificial Intelligence Survey, CMPT 310 D200
# Spring 2021, Simon Fraser University

# author: Jens Classen (jclassen@sfu.ca)

from learning import *

def generate_restaurant_dataset(size=100):
    """
    Generate a data set for the restaurant scenario, using a numerical
    representation that can be used for neural networks. Examples will
    be newly created at random from the "real" restaurant decision
    tree.
    :param size: number of examples to be included
    """

    numeric_examples = None

    ### YOUR CODE HERE ###
    
    return DataSet(name='restaurant_numeric',
                   target='Wait',
                   examples=numeric_examples,
                   attr_names='Alternate Bar Fri/Sat Hungry Patrons Price Raining Reservation Burger French Italian Thai WaitEstimate Wait')

def nn_cross_validation(dataset, hidden_units, epochs=100, k=10):
    """
    Perform k-fold cross-validation. In each round, train a
    feed-forward neural network with one hidden layer. Returns the
    error ratio averaged over all rounds.
    :param dataset:      the data set to be used
    :param hidden_units: the number of hidden units (one layer) of the neural nets to be created
    :param epochs:       the maximal number of epochs to be performed in a single round of training
    :param k:            k-parameter for cross-validation 
                         (do k many rounds, use a different 1/k of data for testing in each round) 
    """
    
    error = 0

    ### YOUR CODE HERE ###
    
    return error


N          = 100   # number of examples to be used in experiments
k          =   5   # k parameter
epochs     = 100   # maximal number of epochs to be used in each training round
size_limit =  15   # maximal number of hidden units to be considered

# generate a new, random data set
# use the same data set for all following experiments
dataset = generate_restaurant_dataset(N)

# try out possible numbers of hidden units
for hidden_units in range(1,size_limit+1):
    # do cross-validation
    error = nn_cross_validation(dataset=dataset,
                                hidden_units=hidden_units,
                                epochs=epochs,
                                k=k)
    # report size and error ratio
    print("Size " + str(hidden_units) + ":", error)
