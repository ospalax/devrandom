# Knapsack Problem

**This is 0/1 variant of knapsack problem.**

There are items in the `data.csv` each with value and weight. The problem is to
put as much items as possible without crossing the limit - a maximum weight of
the knapsack (parameter of the problem).

We are looking for a set of items which has the highest sum of their values
while being under the constraint of the maximum weight.

## Usage

Run the `knapsack.py` like below and pick the solver you want:

```
% python3 knapsack.py
[#] Knapsack Problem Solver [#]
 1. DirectSolver
 2. BetterSolver
 3. GeneticSolver
#> Select Knapsack solver (1-3): 1
#> What is the maximum weight (integer): 150
#> What is the iteration limit (integer): 5
```

**NOTE**: for `DirectSolver` use low iteration number (<10) or you might need
to wait few minutes (cca 4-5 mins)...

## DirectSolver

Firstly I made the obvious, intuitive and straightforward solution to the
problem using the recursion and traversing all possible variants.

Data are sorted by ratio - (value/weight) - this way we get the best chance to
find the best candidate or its approximation very quickly.

We start with the obvious first candidate and then we create all possible
subsets of the candidate list which we then remove from the sorted list and we
look for an alternative.

*(There is room for improvement by skipping some comparisons - but for this toy
problem I decided to keep it simple as possible...)*

This we do for all possible combinations.

With the provided data we get the top ten candidates on **my machine** under 4
minutes:

```
-- Sorted data:

S: {'ratio': 812.5, 'value': 26000, 'weight': 32}
A: {'ratio': 500.0, 'value': 2500, 'weight': 5}
P: {'ratio': 464.2857142857143, 'value': 6500, 'weight': 14}
N: {'ratio': 431.8181818181818, 'value': 9500, 'weight': 22}
J: {'ratio': 350.0, 'value': 3500, 'weight': 10}
K: {'ratio': 333.3333333333333, 'value': 15000, 'weight': 45}
E: {'ratio': 300.0, 'value': 4500, 'weight': 15}
D: {'ratio': 271.42857142857144, 'value': 9500, 'weight': 35}
B: {'ratio': 266.6666666666667, 'value': 3200, 'weight': 12}
G: {'ratio': 220.0, 'value': 5500, 'weight': 25}
T: {'ratio': 211.11111111111111, 'value': 3800, 'weight': 18}
F: {'ratio': 200.0, 'value': 2000, 'weight': 10}
Q: {'ratio': 156.25, 'value': 1250, 'weight': 8}
R: {'ratio': 150.0, 'value': 4200, 'weight': 28}
O: {'ratio': 150.0, 'value': 4500, 'weight': 30}
C: {'ratio': 137.5, 'value': 1100, 'weight': 8}
L: {'ratio': 123.07692307692308, 'value': 3200, 'weight': 26}
I: {'ratio': 109.0909090909091, 'value': 1200, 'weight': 11}
H: {'ratio': 94.44444444444444, 'value': 850, 'weight': 9}
M: {'ratio': 78.57142857142857, 'value': 1100, 'weight': 14}

-- Top ten candidates:

{'list': ['S', 'A', 'P', 'N', 'J', 'K', 'B', 'F'], 'weight': 150, 'value': 68200}
{'list': ['S', 'P', 'N', 'J', 'K', 'E', 'B'], 'weight': 150, 'value': 68200}
{'list': ['S', 'A', 'P', 'N', 'J', 'K', 'E'], 'weight': 143, 'value': 67500}
{'list': ['S', 'A', 'P', 'N', 'J', 'K', 'B', 'Q'], 'weight': 148, 'value': 67450}
{'list': ['S', 'A', 'P', 'N', 'J', 'K', 'B', 'C'], 'weight': 148, 'value': 67300}
{'list': ['S', 'A', 'P', 'N', 'K', 'E', 'B'], 'weight': 145, 'value': 67200}
{'list': ['S', 'A', 'P', 'N', 'J', 'K', 'B', 'H'], 'weight': 149, 'value': 67050}
{'list': ['S', 'P', 'N', 'J', 'K', 'E', 'F'], 'weight': 148, 'value': 67000}
{'list': ['S', 'A', 'P', 'N', 'J', 'K', 'T'], 'weight': 146, 'value': 66800}
{'list': ['S', 'P', 'N', 'K', 'E', 'B', 'F'], 'weight': 150, 'value': 66700}

real	3m27.380s
user	3m26.543s
sys	0m0.185s
```

If we utilize **descent limit** (let's say 5) then we get the same result but
in a fraction of a second on the same machine:

```
-- Top ten candidates:

{'list': ['S', 'A', 'P', 'N', 'J', 'K', 'B', 'F'], 'weight': 150, 'value': 68200}
{'list': ['S', 'P', 'N', 'J', 'K', 'E', 'B'], 'weight': 150, 'value': 68200}
{'list': ['S', 'A', 'P', 'N', 'J', 'K', 'E'], 'weight': 143, 'value': 67500}
{'list': ['S', 'A', 'P', 'N', 'J', 'K', 'B', 'Q'], 'weight': 148, 'value': 67450}
{'list': ['S', 'A', 'P', 'N', 'J', 'K', 'B', 'C'], 'weight': 148, 'value': 67300}
{'list': ['S', 'A', 'P', 'N', 'K', 'E', 'B'], 'weight': 145, 'value': 67200}
{'list': ['S', 'A', 'P', 'N', 'J', 'K', 'B', 'H'], 'weight': 149, 'value': 67050}
{'list': ['S', 'P', 'N', 'J', 'K', 'E', 'F'], 'weight': 148, 'value': 67000}
{'list': ['S', 'A', 'P', 'N', 'J', 'K', 'T'], 'weight': 146, 'value': 66800}
{'list': ['S', 'P', 'N', 'K', 'E', 'B', 'F'], 'weight': 150, 'value': 66700}

real	0m0.248s
user	0m0.232s
sys	0m0.015s
```

**NOTE**: I did not extensively tested or verified the result - so there might
be an isssue with my algorithm and the best solution is missed but so far:
**LGTM** :)

---

## BetterSolver

While writing docstring on **GeneticSolver** I realized that I can fully
utilize itertools to give me all combinations at once (for 20 items it is quite
quick) and then just evaluate them and get the top ten again much simply....

Because we can have exactly 0 or 1 of the particular item then the
biggest candidate can be at most length of the all items.

So for 20 items we can have: 20 long (all items), 19 long, 18 long etc.

We will use itertools to get all combinations and we weed out those
which are violating the weight limit.

Then we just evaluate each valid candidate and get the highest...

```
% time python3 knapsack.py
[#] Knapsack Problem Solver [#]
 1. DirectSolver
 2. BetterSolver
 3. GeneticSolver
#> Select Knapsack solver (1-3): 2
#> What is the maximum weight (integer): 150

-- Top ten candidates:

{'list': ('S', 'A', 'P', 'N', 'J', 'K', 'B', 'F'), 'weight': 150, 'value': 68200, 'ratio': 454.6666666666667}
{'list': ('S', 'P', 'N', 'J', 'K', 'E', 'B'), 'weight': 150, 'value': 68200, 'ratio': 454.6666666666667}
{'list': ('S', 'A', 'P', 'N', 'J', 'K', 'E'), 'weight': 143, 'value': 67500, 'ratio': 472.02797202797206}
{'list': ('S', 'A', 'P', 'N', 'J', 'K', 'B', 'Q'), 'weight': 148, 'value': 67450, 'ratio': 455.7432432432432}
{'list': ('S', 'A', 'P', 'N', 'J', 'K', 'B', 'C'), 'weight': 148, 'value': 67300, 'ratio': 454.72972972972974}
{'list': ('S', 'A', 'P', 'N', 'K', 'E', 'B'), 'weight': 145, 'value': 67200, 'ratio': 463.44827586206895}
{'list': ('S', 'A', 'P', 'N', 'J', 'K', 'B', 'H'), 'weight': 149, 'value': 67050, 'ratio': 450.0}
{'list': ('S', 'P', 'N', 'J', 'K', 'E', 'F'), 'weight': 148, 'value': 67000, 'ratio': 452.7027027027027}
{'list': ('S', 'A', 'P', 'N', 'J', 'K', 'T'), 'weight': 146, 'value': 66800, 'ratio': 457.5342465753425}
{'list': ('S', 'P', 'N', 'K', 'E', 'B', 'F'), 'weight': 150, 'value': 66700, 'ratio': 444.6666666666667}

real	0m5.013s
user	0m1.963s
sys	0m0.141s
```

---

## GeneticSolver

Without writing a single line of code: I am judging that **this is not good
match**.

*The previous brute exhaustive approach is better - it will find the right
answer and it will be more efficient and faster.*

With that said...

Here is a sample of first five iterations (generations):

```
% time python3 knapsack.py
[#] Knapsack Problem Solver [#]
 1. DirectSolver
 2. BetterSolver
 3. GeneticSolver
#> Select Knapsack solver (1-3): 3
#> What is the maximum weight (integer): 150
#> What is the iteration limit (integer): 5
#> What is the value threshold (integer): 0

-- Current population (iteration: 0/5):

{'list': ['A'], 'value': 2500, 'weight': 5}
{'list': ['B'], 'value': 3200, 'weight': 12}
{'list': ['C'], 'value': 1100, 'weight': 8}
{'list': ['D'], 'value': 9500, 'weight': 35}
{'list': ['E'], 'value': 4500, 'weight': 15}
{'list': ['F'], 'value': 2000, 'weight': 10}
{'list': ['G'], 'value': 5500, 'weight': 25}
{'list': ['H'], 'value': 850, 'weight': 9}
{'list': ['I'], 'value': 1200, 'weight': 11}
{'list': ['J'], 'value': 3500, 'weight': 10}
{'list': ['K'], 'value': 15000, 'weight': 45}
{'list': ['L'], 'value': 3200, 'weight': 26}
{'list': ['M'], 'value': 1100, 'weight': 14}
{'list': ['N'], 'value': 9500, 'weight': 22}
{'list': ['O'], 'value': 4500, 'weight': 30}
{'list': ['P'], 'value': 6500, 'weight': 14}
{'list': ['Q'], 'value': 1250, 'weight': 8}
{'list': ['R'], 'value': 4200, 'weight': 28}
{'list': ['S'], 'value': 26000, 'weight': 32}
{'list': ['T'], 'value': 3800, 'weight': 18}

-- Current population (iteration: 1/5):

{'list': ['Q', 'I'], 'value': 2450, 'weight': 19, 'ratio': 128.94736842105263}
{'list': ['A', 'F'], 'value': 4500, 'weight': 15, 'ratio': 300.0}
{'list': ['L', 'B'], 'value': 6400, 'weight': 38, 'ratio': 168.42105263157896}
{'list': ['J', 'T'], 'value': 7300, 'weight': 28, 'ratio': 260.7142857142857}
{'list': ['R', 'E'], 'value': 8700, 'weight': 43, 'ratio': 202.32558139534885}
{'list': ['O', 'G'], 'value': 10000, 'weight': 55, 'ratio': 181.8181818181818}
{'list': ['P', 'D'], 'value': 16000, 'weight': 49, 'ratio': 326.53061224489795}
{'list': ['N', 'K'], 'value': 24500, 'weight': 67, 'ratio': 365.67164179104475}
{'list': ['S'], 'value': 26000, 'weight': 32}
{'list': ['C', 'M', 'H'], 'value': 3050, 'weight': 31, 'ratio': 98.38709677419355}

-- Current population (iteration: 2/5):

{'list': ['R', 'E', 'O', 'G'], 'value': 18700, 'weight': 98, 'ratio': 190.81632653061226}
{'list': ['P', 'N', 'D', 'K'], 'value': 40500, 'weight': 116, 'ratio': 349.13793103448273}
{'list': ['S'], 'value': 26000, 'weight': 32}
{'list': ['M', 'A', 'F', 'H', 'C', 'Q'], 'value': 8800, 'weight': 54, 'ratio': 162.96296296296296}
{'list': ['L', 'B', 'J', 'T', 'I'], 'value': 14900, 'weight': 77, 'ratio': 193.5064935064935}

-- Current population (iteration: 3/5):

{'list': ['S', 'M'], 'value': 27100, 'weight': 46, 'ratio': 589.1304347826087}
{'list': ['L', 'B', 'L', 'G', 'A'], 'value': 18900, 'weight': 98, 'ratio': 192.85714285714286}
{'list': ['R', 'E', 'I', 'L', 'T', 'F'], 'value': 19200, 'weight': 92, 'ratio': 208.69565217391303}
{'list': ['L', 'B', 'G', 'Q'], 'value': 13150, 'weight': 71, 'ratio': 185.2112676056338}
{'list': ['R', 'E', 'I', 'L', 'T', 'H'], 'value': 17750, 'weight': 107, 'ratio': 165.88785046728972}
{'list': ['P', 'N', 'D', 'K', 'C'], 'value': 41600, 'weight': 124, 'ratio': 335.48387096774195}

-- Current population (iteration: 4/5):

{'list': ['R', 'E', 'I', 'L', 'G', 'S'], 'value': 44600, 'weight': 137, 'ratio': 325.54744525547443}
{'list': ['B', 'S', 'T', 'H'], 'value': 33850, 'weight': 71, 'ratio': 476.76056338028167}
{'list': ['R', 'E', 'K', 'I', 'C', 'I'], 'value': 35500, 'weight': 142, 'ratio': 250.0}
{'list': ['P', 'L', 'F', 'N', 'P'], 'value': 25000, 'weight': 90, 'ratio': 277.77777777777777}
{'list': ['R', 'E', 'K', 'I', 'C'], 'value': 26000, 'weight': 107, 'ratio': 242.99065420560748}
{'list': ['P', 'L', 'F', 'N'], 'value': 21200, 'weight': 72, 'ratio': 294.44444444444446}
{'list': ['S', 'M', 'J'], 'value': 30600, 'weight': 56, 'ratio': 546.4285714285714}
{'list': ['R', 'E', 'I', 'L', 'S', 'G', 'Q'], 'value': 22350, 'weight': 118, 'ratio': 189.40677966101694}
{'list': ['S', 'B', 'T', 'H', 'O'], 'value': 15550, 'weight': 95, 'ratio': 163.68421052631578}

-- Current population (iteration: 5/5):

{'list': ['R', 'K', 'I', 'F', 'N', 'T'], 'value': 25200, 'weight': 104, 'ratio': 242.30769230769232}
{'list': ['P', 'L', 'Q', 'G', 'B'], 'value': 42450, 'weight': 105, 'ratio': 404.2857142857143}
{'list': ['R', 'K', 'I', 'F', 'N', 'T'], 'value': 35700, 'weight': 134, 'ratio': 266.4179104477612}
{'list': ['P', 'L', 'Q', 'G', 'B'], 'value': 19650, 'weight': 85, 'ratio': 231.1764705882353}
{'list': ['R', 'P', 'I', 'C', 'D'], 'value': 20500, 'weight': 97, 'ratio': 211.340206185567}
{'list': ['R', 'E', 'K', 'I', 'C'], 'value': 26000, 'weight': 107, 'ratio': 242.99065420560748}
{'list': ['R', 'I', 'P', 'C', 'D'], 'value': 22500, 'weight': 96, 'ratio': 234.375}
{'list': ['R', 'E', 'I', 'L', 'G', 'S'], 'value': 44600, 'weight': 137, 'ratio': 325.54744525547443}
{'list': ['M', 'P', 'L', 'F', 'J', 'N', 'S', 'A'], 'value': 54300, 'weight': 133, 'ratio': 408.2706766917293}
{'list': ['B', 'S', 'T', 'H', 'O'], 'value': 38350, 'weight': 101, 'ratio': 379.7029702970297}

-- Terminating condition met:
   iterations: 5/5
   threshold:  None

-- Candidate:

{'list': ['M', 'P', 'L', 'F', 'J', 'N', 'S', 'A'],
 'ratio': 408.2706766917293,
 'value': 54300,
 'weight': 133}

real	0m11.143s
user	0m0.022s
sys	0m0.010s
```

This solver will work in iterations by maintaining healthy population
of valid candidates with a goal to raise their individual value every
time.

It will not exhaustively explore solution space... just by the fact how genetic
algorithms work - they are non-deterministic, inefficient and they will not
cover every possible variation as previous solvers would.

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

