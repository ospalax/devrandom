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
import itertools

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
        print("\n-- Sorted data:\n")
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

    def __init__(self, filename, weight):
        super().__init__(filename, weight)
        self._all_candidates = {}

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

    def find_all(self, descent_limit=None):
        def add_candidate(new_candidate):
            key = tuple(new_candidate['list'])
            if key not in self._all_candidates:
                self._all_candidates[key] = new_candidate

        def get_next(last_candidate, last_sorted):
            for s in generate_sorted(last_candidate, last_sorted):
                if not s:
                    break
                new_candidate = self.get_candidate(s)
                add_candidate(new_candidate)
                #print("New sorted: ", end="");
                #print(s)
                #print("New candidate: ", end="");
                #print(new_candidate)
                get_next(new_candidate, s)

        def get_exclusion_list(candidate):
            """
            This will return all subsets of the candidate list which
            we then can extract from 'sorted' and look for new
            candidates - this could be optimalized by reordering the
            subsets to match candidate list and by going from back
            we can skip first items in the sorted list...

            I am using itertools.combinations for simplicity and
            I will not be optimizing this further.
            """
            result = []

            for i in range(1, len(candidate['list']) + 1):
                result.extend(itertools.combinations(candidate['list'], i))

            return result

        def generate_sorted(candidate, sorted):
            """
            Generator for new sorted list where candidate items
            are removed
            """
            exclusions = get_exclusion_list(candidate)

            for excluded in exclusions:
                new_sorted = [x for x in sorted if x not in excluded]
                yield new_sorted


        self._all_candidates = {}
        self._descent = 0

        # adding the best candidate first
        first = self.get_candidate()
        add_candidate(first)

        # now descent to find every other
        get_next(first, self.sorted)

    def get_top_ten(self):
        if not self._all_candidates:
            self.find_all()

        topten = []
        control = {}
        for i in range(10):
            maxkey = None
            maxvalue = 0
            for key, candidate in self._all_candidates.items():
                if key in control:
                    continue

                if candidate['value'] >= maxvalue:
                    maxkey = key
                    maxvalue = candidate['value']

            control[maxkey] = maxvalue
            topten.append(self._all_candidates[maxkey])

        return topten



    def print_all(self):
        if not self._all_candidates:
            self.find_all()

        print("\n-- All candidates:\n")
        for i in self._all_candidates:
            pp(i)

    def print_top_ten(self):
        if not self._all_candidates:
            self.find_all()

        print("\n-- Top ten candidates:\n")
        for i in self.get_top_ten():
            pp(i)



#
# main
#

def main():
    knapsack = DirectSolver('data.csv', 50)

    # TODO: just to make things faster and easier while deving
    knapsack.sorted = knapsack.sorted[:15]

    knapsack.print_sorted()
    knapsack.print_all()
    knapsack.print_top_ten()
    return 0

if __name__ == "__main__":
    sys.exit(main())
