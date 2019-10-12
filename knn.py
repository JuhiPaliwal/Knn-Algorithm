from math import sqrt
import operator
from collections import Counter
N = int(input())
with open('trainset.txt', 'w') as tr:
    for _ in range(N): tr.write(f'{input()[1:-1]}\n')
T = int(input())
with open('testset.txt', 'w') as ts:
    for _ in range(T): ts.write(f'{input()[1:-1]}\n')
RESULT_PATH = 'result.text'
# ###################################################


TRAINSET_PATH = 'trainset.txt'
TESTSET_PATH = 'testset.txt'



# ############################


def load_trainset(path):
    """
    :param path: a string which is the path to a text file which contains trainset data.
                 The lines in trainset data are employment information from a number of employees
                 and each line should be in the following format:

                 agi,age,stt,cat

                 Where agi is annual gross income, age is age, stt is the state in which the employee resides,
                 and cat is either 0, 1, or 2, where 0 means developer, 1 means scientist, and 2 means manager.

                 example: 110000,22,11,0
                          is the data for a developer who has 22 years and resides in state 11, and earns 110000
                          each year.

    :return :   read lines in trainset file and extract (agi,age,stt) from each line as a tuple of integers and append
                them to a list called train_points and append cat as an integer to another list called train_cats.
                return train_points, train_cats
    """

    train_points = []
    train_cats = []
    with open('trainset.txt') as tr:
        for line in tr:
            splitted = line.split(',')
            train_points.append((int(splitted[0]), int(splitted[1]), int(splitted[2])))
            train_cats.append(int(splitted[3]))
    return train_points, train_cats


def load_testset(path):
    """
    :param path: a string which is the path to a text file which contains testset data.
                 The lines in testset data are employment information from a number of employees that we do not know
                 to what category they belong and each line should be in the following format:

                 agi,age,stt,k

                 Where agi is annual gross income, age is age, stt is the state in which the employee resides,
                 and k is an integer that we want to set as KNN algorithm parameter.

                 example: 110000,22,11,4
                          is the data for an employee who has 22 years and resides in state 11, and earns 110000
                          each year, and we want to run KNN with k=4 to predict his category.

    :return :   read lines in testset file and extract (agi,age,stt) from each line as a tuple of integers and append
                them to a list called test_points and append k as an integer to another list called Ks.
                return test_points, Ks
    """

    test_points = []
    K = []

    with open('testset.txt') as ts:
        for line in ts:
            splitted = line.split(',')
            test_points.append((int(splitted[0]), int(splitted[1]), int(splitted[2])))
            K.append(int(splitted[3]))
    return test_points,K


def knn(train_points, train_cats, test_points, Ks):
    """
    :param train_points: a list of tuples of integers, which are feature values for a number of training observations.

    :param train_cats  : a list of integers with the same size as train_points. train_cats[i] is the category
                         of the i'th training observation.

    :param test_points : a list of tuples of integers, which are feature values for a number of test observations.

    :param Ks          : a list of integers. For the i'th test observation KNN algorithm will be executed with k = Ks[i].

    :return            : a list of integers where each integer is either 0, 1, or 2. The i'th integer in this list is
                         the predicted category for the i'th test observation.
    """

    pass  # TO DO... Remove this line when you implement this function
    predictions = []
    dist = get_distances_with_categories(train_points, train_cats, test_points)
    neighbors = get_nearest_neighbors(dist, Ks)

    return predictions
    

def get_distances_with_categories(train_points, train_cats, test_point,Ks):
    """
    :param train_points: a list of tuples of integers, which are feature values for a number of training observations.

    :param train_cats  : a list of integers with the same size as train_points. train_cats[i] is the category
                         of the i'th training observation.

    :param test_point  : a tuple of integers, which is feature values for one test observation.

    :return            : a list of pairs called distances, where the i'th pair is a tuple like (d, c) where
                         d is the euclidean distance between train_points[i] and the given test_point, and
                         c is the category of the i'th observation which is train_cats[i].
    """
    result_categories = []
    for i, t in enumerate(test_point):
        distances = []
        k = Ks[i]
        for j, p in enumerate(train_points):
            d = euclidean_distance(t, p)
            distances.append( (d, train_cats[j]) )
        neighbors = get_nearest_neighbors(distances, k)
        max_cat = get_category_frequencies(neighbors)
        result_categories.append(max_cat)
    return result_categories

def euclidean_distance(p, t):
    """
    :param p1: a n-dimensional point.

    :param p2: a n-dimensional point.

    :return  : the euclidean distance between the two given points.
    """
    d = sqrt((p[0]-t[0])**2+(p[1]-t[1])**2+(p[2]-t[2])**2)
    return d

def get_nearest_neighbors(distances, k):
    """
    :param distances: a list of pairs of numbers like (d,c).

    :param k        : the number of nearest neighbors that this function returns.

    :return         : first sort the given distances based on d in (d,c), then return
                      the first k elements in it.
    """
    
    distances.sort()
    neighbors = distances[:k]
    
    #print(neighbors)
    return neighbors

def get_category_frequencies(neighbors):
    """
    :param neighbors: a list of pairs where each pair is a tuple like (d, c), where d is a measured distance,
                      and c is a category which can have any immutable type!

    :return         : a dictionary where keys are the categories that have appreared in neighbors list,
                      and values are their frequency in that list.
    """
    new_dict = {}
    counts = [0, 0, 0]
    for n in neighbors:
        counts[n[1]] += 1
        max_count, max_cat = -1, -1
        #max_cat = find_most_frequent_category(new_dict)
        for i, count in enumerate(counts):
            new_dict[i] = count
            max_cat = find_most_frequent_category(new_dict)
            
    return max_cat

def find_most_frequent_category(freqs):
    """
    :param freqs: a dictionary between categories and their frequencies.

    :return     : the key which is associated with the max value in the given dictionary.
                  if there are more than one key with max value, return that key which has
                  the least order.
    """
    mx = max(freqs.values())
    for key in sorted(freqs.keys()):
        if freqs[key] == mx:
            return key


def write_results(path, result_list):
    """
    write each element in the result_list on one line of the file which has the given path.

    :param path       : a path to the file that we want to write the results in.

    :param result_list: a list of elements where each element represents a category.

    :return           : Nothing
    """

    with open(path, 'w') as res:
        for cat in result_list:
            res.write(f'{cat}\n')


if __name__ == "__main__":
    train_points, train_cats = load_trainset(TRAINSET_PATH)
    test_points, Ks = load_testset(TESTSET_PATH)

    result_list = get_distances_with_categories(train_points, train_cats, test_points, Ks)

    write_results(RESULT_PATH, result_list)
    
    with open(RESULT_PATH) as res:
        for line in res: print(line.strip())

