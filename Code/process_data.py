import numpy as np
import csv
from random import shuffle
from scipy.misc import imread, imsave

import constants as c

def test_train_split(data_file, test_file, train_file, num_test):
    """
    Split data into random train and test sets.

    @param data_file: The filepath to the unsplit data.
    @param test_file: The filepath to which to write the test data.
    @param train_file: The filepath to which to write the train data.
    @param num_test: The desired size of the test set. The train set will be the total number of
                     data points, minus num_test. num_test must be < total number of data points.
    """
    # get random indices for tests
    test_indices = np.random.choice(c.NUM_DATA, num_test, replace=False)

    test = []
    train = []

    w_test = csv.writer(open(test_file, 'wb'))
    w_train = csv.writer(open(train_file, 'wb'))

    with open(data_file, 'r') as f:
        reader = csv.reader(f)
        reader.next()
        for i, row in enumerate(reader):
            if i in test_indices:
                test.append(row)
            else:
                train.append(row)

            print i

    shuffle(test)
    shuffle(train)

    w_test.writerows(test)
    w_train.writerows(train)

# def img_to_grayscale():


def main():
    test_train_split('../Data/index', '../Data/test.csv', '../Data/train.csv', 1000)



if __name__ == '__main__':
    main()
