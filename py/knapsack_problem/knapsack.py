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
import random

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


    def print_candidate(self, candidate):
        print("\n-- Candidate:\n")
        pp(candidate)


class DirectSolver(Knapsack):
    """
    My initial intuitive and direct solver of the problem.

    (to mostly play with the problem)
    """

    def __init__(self, filename, weight, descent_limit=None):
        super().__init__(filename, weight)
        self.descent_limit = descent_limit
        self._all_candidates = {}
        self._seen_candidates = {}

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

            return key

        def get_next(last_candidate, last_sorted, descent_counter):
            if descent_counter is not None:
                if descent_counter <= 0:
                    return False;
                else:
                    descent_counter -= 1

            for s in generate_sorted(last_candidate, last_sorted):
                if not s:
                    break
                new_candidate = self.get_candidate(s)

                c_key = add_candidate(new_candidate)
                s_key = tuple(s)
                seen = (c_key, s_key)
                if seen in self._seen_candidates:
                    # we already did this combo
                    continue

                self._seen_candidates[seen] = True

                if not get_next(new_candidate, s, descent_counter):
                    break

            return True

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
        self._seen_candidates = {}

        if descent_limit:
            self._descent = descent_limit
        else:
            self._descent = self.descent_limit

        # adding the best candidate first
        first = self.get_candidate()
        add_candidate(first)

        # now descent to find every other
        get_next(first, self.sorted, self._descent)

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

            if maxkey is None:
                break

            control[maxkey] = maxvalue
            topten.append(self._all_candidates[maxkey])

        return topten

    def print_all(self):
        if not self._all_candidates:
            self.find_all()

        print("\n-- All candidates:\n")
        for i in self._all_candidates:
            print(i)

    def print_top_ten(self):
        if not self._all_candidates:
            self.find_all()

        print("\n-- Top ten candidates:\n")
        for i in self.get_top_ten():
            print(i)


class BetterSolver(DirectSolver):
    """
    While writing docstring on GeneticSolver I realized that I can fully
    utilize itertools to give me all combinations at once (for 20 items it is
    quite quick) and then just evaluate them and get the top ten again much
    simply....

    Because we can have exactly 0 or 1 of the particular item then the
    biggest candidate can be at most length of the all items.

    So for 20 items we can have: 20 long (all items), 19 long, 18 long etc.

    We will use itertools to get all combinations and we weed out those
    which are violating the weight limit.

    Then we just evaluate each valid candidate and get the highest...
    """

    def __init__(self, filename, weight):
        super().__init__(filename, weight)

    def find_all(self):
        def calc_values(item_list):
            value = 0
            weight = 0

            for i in item_list:
                value += self.data[i]['value']
                weight += self.data[i]['weight']

            ratio = value / weight

            return value, weight, ratio

        def return_all_subsets():
            all_items = []
            for key in self.sorted:
                all_items.append(key)

            all_sets = set()
            for i in range(1, len(all_items) + 1):
                for subset in itertools.combinations(all_items, i):
                    all_sets.add(subset)

            for group in all_sets:
                value, weight, ratio = calc_values(group)
                if weight > self.maxweight:
                    continue

                candidate = {}
                candidate['list'] = group
                candidate['weight'] = weight
                candidate['value'] = value
                candidate['ratio'] = value / weight
                self._all_candidates[tuple(group)] = candidate

        return_all_subsets()

class GeneticSolver(Knapsack):
    """
    NOTE: genetic algorithm on this problem is very forced - if I create all
    combinations of possible valid candidates from the start then I can just
    directly calculate and sort them to get the answer...

    So I must create subpar solver to simulate need for a genetic algorithm.

    ...

    This solver will work in iterations by maintaining healthy population
    of valid candidates with a goal to raise their individual value every
    time.

    It will not exhaustively explore solution space... just by the fact
    how genetic algorithms work - they are non-deterministic, inefficient
    and they will not cover every possible variation as previous solvers
    would.

    The solver works as so:

     1. make initial population:

        (I cannot create all combinations of the items here because there would
        be no longer any point to do any kind of genetic iteration...)

        Start with singletons.

        Put all valid singletons in reserve - we will reach here from time to
        time to not lose some items over iterations.

     2. evaluation:

        Calculate value and weight for each specimen and sort them.

        We might have high value specimen which will be over weight limit, that
        specimen will not count towards the threshold.

        Here we set some threshold to end the iterations.

     3. select the next population:

        This is a phase where it seems good to weed out overweight specimen
        but I am guessing that with that approach we would never get close to
        optimal candidate. Because any tiny amount over limit would remove it
        from population... and we would get stuck only with subpar candidates.

        Therefore we will keep overweight specimen and only try to fix them
        in crossover and mutation stages...

        But to not just get heavier and heavier specimens - we will select
        overweight limit - that will be the weight of the most heavy item.

        Weed out anything heavier than that.

        Lastly select top half of the population (highest values).

     4. crossover:

        If specimen weight is less than half of limit then just pair it with
        another specimen of similar weight.

        Otherwise find two specimen which cannot be paired and only crossover
        half of their items e.g.:

            Specimen 1: A P N J K B -> A P N.....J K B
            Specimen 2: S A P N Q   -> S A P.....N Q

            watch out for duplicates...use set:

            Child 1: A P N Q
            Child 2: S A P J K B

        To increase population at this stage we introduce sibling for each
        offspring - this way population multiply until it reaches certain
        threshold when it will be culled (halfed) and cycle will repeat.

     5. mutation:

        If some item is missing in the population then put them to random
        specimen as singletons from reserve.

    Go back to point 2.

    """

    def __init__(self, filename, weight, iteration_limit=1000, threshold=None):
        super().__init__(filename, weight)
        self.iteration_limit = iteration_limit
        self.threshold = threshold
        self._current_population = {}
        self._last_population = {}
        self._max_overweight = 0
        self._current_sorted = []
        self._iteration = 0
        self._max_populous = 30 # we will half the population if reached

    def initial_population(self):
        for key, item in self.data.items():
            if item['weight'] > self.maxweight:
                # this item is already disqualified
                continue

            if item['weight'] > self._max_overweight:
                # we look for heaviest item
                self._max_overweight = item['weight']

            specimen = {}
            specimen['list'] = list(key)
            specimen['value'] = item['value']
            specimen['weight'] = item['weight']
            self._current_population[tuple(key)] = specimen

    def sort_population(self, population):
        sorted = []
        for key, specimen in population.items():
            i = 0
            inplace = False
            for index, placed in enumerate(sorted):
                i = index
                if specimen['value'] >= population[placed]['value']:
                    inplace = True
                    break

            if inplace:
                sorted.insert(i, key)
            else:
                sorted.append(key)

        return sorted

    def evaluate(self):
        terminate = False

        self._current_sorted = self.sort_population(self._current_population)

        candidate = None
        for key in self._current_sorted:
            # find highest valid candidate
            if self._current_population[key]['weight'] <= self.maxweight:
                candidate = self._current_population[key]
                break

        if candidate and self.threshold and (candidate['value'] >= self.threshold):
            terminate = True

        if self._iteration >= self.iteration_limit:
            terminate = True

        return terminate, candidate

    def select(self):
        # weed out too overweight specimen
        cleaned = []
        for key in self._current_sorted:
            # save only healthy specimen
            if self._current_population[key]['weight'] <= self.maxweight + self._max_overweight:
                cleaned.append(key)

        # prepare for next generation
        self._current_sorted = []
        self._last_population = self._current_population
        self._current_population = {}

        # we will pass to next generation only top half of current population
        # if we reach specific population number
        size_of_population = len(cleaned)
        if size_of_population > self._max_populous:
            size_of_population //= 2

        # drop low performing specimen - at least one
        for i in range(size_of_population - 1):
            self._current_sorted.append(cleaned[i])
            self._current_population[cleaned[i]] = self._last_population[cleaned[i]]

    def calc_values(self, item_list):
        value = 0
        weight = 0

        for i in item_list:
            value += self.data[i]['value']
            weight += self.data[i]['weight']

        ratio = value / weight

        return value, weight, ratio

    def crossover(self):
        def splice(key1, key2):
            nextspec = {}

            spec1 = self._current_population[key1]
            spec2 = self._current_population[key2]

            new_list = list(set(spec1['list'] + spec2['list']))
            nextspec['list'] = new_list

            value, weight, ratio = self.calc_values(new_list)
            nextspec['value'] = value
            nextspec['weight'] = weight
            nextspec['ratio'] = ratio

            return nextspec

        def breed(key1, key2):
            spec1 = {}
            spec2 = {}

            # split "chromosomes"
            key1_delim = len(key1) // 2
            key1_p1 = key1[:key1_delim]
            key1_p2 = key1[key1_delim:]

            key2_delim = len(key2) // 2
            key2_p1 = key2[:key2_delim]
            key2_p2 = key2[key2_delim:]

            # flip and assemble new "chromosomes"
            new_list1 = list(set(key1_p1 + key2_p2))
            new_list2 = list(set(key2_p1 + key1_p2))
            spec1['list'] = new_list1
            spec2['list'] = new_list2

            # recalculate
            value, weight, ratio = self.calc_values(new_list1)
            spec1['value'] = value
            spec1['weight'] = weight
            spec1['ratio'] = ratio

            value, weight, ratio = self.calc_values(new_list2)
            spec2['value'] = value
            spec2['weight'] = weight
            spec2['ratio'] = ratio

            return spec1, spec2

        def multiply(key):
            # crossover step does not increase population so here we introduce
            # new random specimen twins

            target_genom = random.randint(0, len(key) - 1)
            source_genom = random.randint(0, len(self.data) - 1)

            for genom, item in self.data.items():
                if source_genom <= 0:
                    key[target_genom] = genom
                    break
                source_genom -= 1

            twin = {}
            twin['list'] = list(set(key))
            value, weight, ratio = self.calc_values(twin['list'])
            twin['value'] = value
            twin['weight'] = weight
            twin['ratio'] = value / weight

            return twin

        # break up specimen into two categories:
        # - collect specimen with less than half of maximum weight
        # - the rest will be crossovered
        small = []
        big = []
        for key in self._current_sorted:
            if self._current_population[key]['weight'] <= self.maxweight // 2:
                small.append(key)
            else:
                big.append(key)

        # we don't need to update sorted list, just population
        new_batch = {}

        while small:
            key1 = small.pop()
            if small:
                key2 = small.pop()
            else:
                # we don't have second specimen for splicing so just add the
                # first one unchanged to the new_batch
                new_batch[key1] = self._current_population[key1]
                break

            specimen = splice(key1, key2)
            new_batch[tuple(specimen['list'])] = specimen

        while big:
            key1 = big.pop()
            if big:
                key2 = big.pop()
            else:
                # we don't have second specimen for crossover so just add the
                # first one unchanged to the new_batch
                new_batch[key1] = self._current_population[key1]
                break

            spec1, spec2 = breed(key1, key2)
            new_batch[tuple(spec1['list'])] = spec1
            new_batch[tuple(spec2['list'])] = spec2

            # duplicate every offspring
            twin1 = multiply(spec1['list'])
            twin2 = multiply(spec2['list'])
            new_batch[tuple(twin1['list'])] = twin1
            new_batch[tuple(twin2['list'])] = twin2

        # replace current population with crossovered one
        self._current_population = new_batch

    def mutate(self):
        # collect all genoms in population
        seen = set()
        for key in self._current_population:
            seen.update(key)

        # work out the missing genoms
        missing = set()
        for i in self.data:
            if i not in seen:
                missing.add(i)

        # need this for next step
        keys = []
        for key in self._current_population:
            keys.append(key)

        # reintroduce one or more missing "genoms" back into population as
        # "mutation"
        singleton = None
        for key in keys:
            # no genom left
            if not missing:
                break

            # pick another genom only if we did not utilized the previous
            if not singleton:
                singleton = missing.pop()

            # skip this specimen if it has this genom already
            if singleton in key:
                continue

            # extend the specimen with new genom
            mutated = self._current_population[key]
            mutated['list'].append(singleton)
            mutated['value'] += self.data[singleton]['value']
            mutated['weight'] += self.data[singleton]['weight']
            mutated['ratio'] = mutated['value'] / mutated['weight']

            # add it to population and delete the old one
            newkey = tuple(mutated['list'])
            self._current_population[newkey] = mutated
            del self._current_population[key]
            singleton = None

    def print_population(self):
        print(f"\n-- Current population (iteration: {self._iteration}/{self.iteration_limit}):\n")
        for key in self._current_population:
            print(self._current_population[key])

    def print_termination(self):
        print(f"\n-- Terminating condition met:")
        print(  f"   iterations: {self._iteration}/{self.iteration_limit}")
        print(  f"   threshold:  {self.threshold}")


    def iterate_generations(self, printing=True, iterations=None):
        if not iterations:
            iterations = self.iteration_limit

        self.initial_population()
        self.print_population()

        while True:
            terminate, candidate = self.evaluate()

            if terminate or (self._iteration >= iterations):
                self.print_termination()
                if candidate:
                    self.print_candidate(candidate)
                break

            self._iteration += 1
            self.select()
            self.crossover()
            self.mutate()

            if printing:
                self.print_population()

#
# main
#

def ask_integer(prompt):
    r = None
    while r is None:
        try:
            r = int(input(prompt))
            if r < 0:
                r = None
        except:
            pass
    return r

def main():
    print("[#] Knapsack Problem Solver [#]")
    print(" 1. DirectSolver")
    print(" 2. BetterSolver")
    print(" 3. GeneticSolver")

    solver_num = 0
    while solver_num not in (1, 2, 3):
        try:
            solver_num = int(input("#> Select Knapsack solver (1-3): "))
        except:
            pass

    match solver_num:
        case 1:
            # DirectSolver
            maxweight = ask_integer("#> What is the maximum weight (integer): ")
            maxiter = ask_integer("#> What is the iteration limit (integer): ")

            if maxiter <= 0:
                knapsack = DirectSolver('data.csv', maxweight)
            else:
                knapsack = DirectSolver('data.csv', maxweight, maxiter)

            knapsack.print_sorted()
            #knapsack.print_all()
            knapsack.print_top_ten()
        case 2:
            # BetterSolver
            maxweight = ask_integer("#> What is the maximum weight (integer): ")
            knapsack = BetterSolver('data.csv', maxweight)
            #knapsack.sorted = knapsack.sorted[:5]
            knapsack.print_top_ten()
        case 3:
            # GeneticSolver
            maxweight = ask_integer("#> What is the maximum weight (integer): ")
            maxiter = ask_integer("#> What is the iteration limit (integer): ")
            maxthres = ask_integer("#> What is the value threshold (integer): ")

            if maxthres <= 0:
                maxthres = None

            if maxiter <= 0:
                knapsack = GeneticSolver('data.csv', maxweight, threshold=maxthres)
            else:
                knapsack = GeneticSolver('data.csv', maxweight, maxiter, threshold=maxthres)

            #knapsack.iterate_generations(printing=True, iterations=5)
            knapsack.iterate_generations(printing=True)

    return 0

if __name__ == "__main__":
    sys.exit(main())
