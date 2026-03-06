# Knapsack Problem

**This is 0/1 variant of knapsack problem.**

There are items in the `data.csv` each with value and weight. The problem is to
put as much items as possible without crossing the limit - a maximum weight of
the knapsack (parameter of the problem).

We are looking for a set of items which has the highest sum of their values
while being under the constraint of the maximum weight.

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
% time python3 knapsack.py

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

## GeneticSolver

Without writing a single line of code: I am judging that **this is not good
match**.

*The previous brute exhaustive approach is better - it will find the right
answer and it will be more efficient and faster.*

With that said...

Here is a sample of first five iterations (generations):

```
% time python3 knapsack.py

-- Current population (iteration: 0/100):

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

-- Current population (iteration: 1/100):

{'list': ['Q', 'I'], 'value': 2450, 'weight': 19, 'ratio': 128.94736842105263}
{'list': ['F', 'A'], 'value': 4500, 'weight': 15, 'ratio': 300.0}
{'list': ['L', 'B'], 'value': 6400, 'weight': 38, 'ratio': 168.42105263157896}
{'list': ['J', 'T'], 'value': 7300, 'weight': 28, 'ratio': 260.7142857142857}
{'list': ['R', 'E'], 'value': 8700, 'weight': 43, 'ratio': 202.32558139534885}
{'list': ['G', 'O'], 'value': 10000, 'weight': 55, 'ratio': 181.8181818181818}
{'list': ['D', 'P'], 'value': 16000, 'weight': 49, 'ratio': 326.53061224489795}
{'list': ['K', 'N'], 'value': 24500, 'weight': 67, 'ratio': 365.67164179104475}
{'list': ['S'], 'value': 26000, 'weight': 32}
{'list': ['C', 'M', 'H'], 'value': 3050, 'weight': 31, 'ratio': 98.38709677419355}

-- Current population (iteration: 2/100):

{'list': ['R', 'E', 'G', 'O'], 'value': 18700, 'weight': 98, 'ratio': 190.81632653061226}
{'list': ['K', 'N', 'D', 'P'], 'value': 40500, 'weight': 116, 'ratio': 349.13793103448273}
{'list': ['S'], 'value': 26000, 'weight': 32}
{'list': ['A', 'F', 'H', 'C', 'M', 'Q'], 'value': 8800, 'weight': 54, 'ratio': 162.96296296296296}
{'list': ['J', 'L', 'T', 'B', 'I'], 'value': 14900, 'weight': 77, 'ratio': 193.5064935064935}

-- Current population (iteration: 3/100):

{'list': ['S', 'A'], 'value': 28500, 'weight': 37, 'ratio': 770.2702702702703}
{'list': ['J', 'N', 'G', 'O', 'F'], 'value': 18700, 'weight': 101, 'ratio': 185.14851485148515}
{'list': ['T', 'P', 'B', 'R', 'E', 'Q'], 'value': 18150, 'weight': 92, 'ratio': 197.2826086956522}
{'list': ['J', 'N', 'G', 'O', 'H'], 'value': 23850, 'weight': 96, 'ratio': 248.4375}
{'list': ['T', 'B', 'R', 'E', 'P', 'C'], 'value': 23300, 'weight': 95, 'ratio': 245.26315789473685}
{'list': ['K', 'N', 'D', 'P', 'M'], 'value': 41600, 'weight': 130, 'ratio': 320.0}

-- Current population (iteration: 4/100):

{'list': ['N', 'D', 'C', 'E', 'P'], 'value': 31100, 'weight': 94, 'ratio': 330.8510638297872}
{'list': ['T', 'O', 'G', 'F', 'R'], 'value': 20000, 'weight': 111, 'ratio': 180.18018018018017}
{'list': ['J', 'N', 'D', 'P', 'N'], 'value': 30100, 'weight': 95, 'ratio': 316.8421052631579}
{'list': ['O', 'S', 'G', 'H', 'K'], 'value': 35350, 'weight': 131, 'ratio': 269.8473282442748}
{'list': ['J', 'N', 'D', 'P'], 'value': 29000, 'weight': 81, 'ratio': 358.0246913580247}
{'list': ['O', 'S', 'G', 'H', 'K'], 'value': 51850, 'weight': 141, 'ratio': 367.7304964539007}
{'list': ['S', 'A', 'L'], 'value': 31700, 'weight': 63, 'ratio': 503.1746031746032}
{'list': ['D', 'N', 'C', 'E', 'P', 'Q'], 'value': 26350, 'weight': 77, 'ratio': 342.2077922077922}
{'list': ['T', 'O', 'G', 'R', 'F', 'R', 'I'], 'value': 24400, 'weight': 134, 'ratio': 182.08955223880596}

-- Current population (iteration: 5/100):

{'list': ['S', 'A', 'L'], 'value': 31700, 'weight': 63, 'ratio': 503.1746031746032}
{'list': ['T', 'O', 'G', 'B', 'E', 'P'], 'value': 26050, 'weight': 110, 'ratio': 236.8181818181818}
{'list': ['I', 'N', 'F', 'D', 'E', 'C'], 'value': 27500, 'weight': 114, 'ratio': 241.2280701754386}
{'list': ['T', 'O', 'G', 'B', 'E', 'P'], 'value': 28000, 'weight': 114, 'ratio': 245.6140350877193}
{'list': ['I', 'N', 'F', 'D', 'C', 'E'], 'value': 27800, 'weight': 101, 'ratio': 275.2475247524753}
{'list': ['J', 'N', 'D', 'P', 'R'], 'value': 30100, 'weight': 95, 'ratio': 316.8421052631579}
{'list': ['J', 'N', 'D', 'A'], 'value': 29000, 'weight': 81, 'ratio': 358.0246913580247}
{'list': ['J', 'N', 'D', 'R', 'P'], 'value': 33200, 'weight': 109, 'ratio': 304.58715596330273}
{'list': ['J', 'N', 'A', 'D'], 'value': 25000, 'weight': 72, 'ratio': 347.22222222222223}
{'list': ['N', 'P', 'D', 'H', 'K'], 'value': 40350, 'weight': 136, 'ratio': 296.69117647058823}
{'list': ['O', 'N', 'C', 'E', 'P'], 'value': 26100, 'weight': 89, 'ratio': 293.2584269662921}
{'list': ['N', 'D', 'H', 'K', 'P'], 'value': 41350, 'weight': 125, 'ratio': 330.8}
{'list': ['O', 'S', 'G', 'H', 'K'], 'value': 51850, 'weight': 141, 'ratio': 367.7304964539007}

-- Terminating condition met:
   iterations: 5/100
   threshold:  None

-- Candidate:

{'list': ['O', 'S', 'G', 'H', 'K'],
 'ratio': 367.7304964539007,
 'value': 51850,
 'weight': 141}

real	0m0.032s
user	0m0.025s
sys	0m0.007s
```

