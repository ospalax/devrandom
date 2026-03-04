#!/usr/bin/python3

__all__ = [
    "__title__",
    "__summary__",
    "__version__",
    "__author__",
]

__title__ = "knapsack"
__summary__ = "Solution for 0/1 Knapsack Problem"
__version__ = "1.0.0"
__author__ = "Petr Ospalý"

import sys
import csv
from pprint import pprint as pp

class Knapsack:
    """
    Parent class to handle csv and data
    """

    def __init__(self, filename, weight):
        self.data = self.read_data(filename)
        self.sorted = self.create_sorted_list()
        self.maxweight = weight

    def read_data(self, filename):
        """
        Read csv file and store it in a dict while also calculating
        ratios (value/weight):
            data['A'] = {
                'value': 2500,
                'weight': 5,
                'ratio': 500.0
                }

        """

        data = {}
        with open(filename, mode='r', newline='') as f:
            csvdata = csv.reader(f, delimiter=',')
            for item in csvdata:
                if item[0].lower() == 'item':
                    continue
                data[item[0]] = {}
                data[item[0]]['weight'] = int(item[1])
                data[item[0]]['value'] = int(item[2])
                data[item[0]]['ratio'] = data[item[0]]['value'] \
                        / data[item[0]]['weight']

        return data

    def create_sorted_list(self):
        """
        Straightforward sorting function for ratios
        """

        sorted = []
        for key, item in self.data.items():
            i = 0
            inplace = False
            for index, placed in enumerate(sorted):
                i = index
                if item['ratio'] >= self.data[placed]['ratio']:
                    inplace = True
                    break

            if inplace:
                sorted.insert(i, key)
            else:
                sorted.append(key)

        return sorted

    def print_sorted(self):
        for i, key in enumerate(self.sorted):
            print(f"{key}: ", end='')
            pp(self.data[self.sorted[i]])


    def print_candidate(self,candidate):
        pp(candidate)


class DirectSolver(Knapsack):
    """
    My initial intuitive and direct solver of the problem.

    (to mostly play with the problem)
    """

    def get_candidate(self, sorted=None):
        """
        Utilizing the sorted ratios - we pick the best ratioed items until we
        hit limit
        """

        if not sorted:
            sorted = self.sorted

        i = 0
        length = len(sorted)

        candidate = {}
        candidate['list'] = []
        candidate['weight'] = 0
        candidate['value'] = 0
        while (candidate['weight'] < self.maxweight) and (i < length):
            if (candidate['weight'] + self.data[sorted[i]]['weight']) > self.maxweight:
                    i += 1
                    continue
            candidate['weight'] += self.data[sorted[i]]['weight']
            candidate['value'] += self.data[sorted[i]]['value']
            candidate['list'].append(sorted[i])
            i += 1

        return candidate

   #def

#
# main
#

def main():
    knapsack = DirectSolver('data.csv', 50)

    knapsack.print_sorted()
    knapsack.print_candidate(knapsack.get_candidate())
    return 0

if __name__ == "__main__":
    sys.exit(main())
