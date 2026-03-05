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


