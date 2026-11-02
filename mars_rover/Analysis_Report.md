# Mars Rover Sample Collection: PDDL Analysis Report

## 0. A note on the tools I used

I wrote the PDDL files in VS Code and tested them on the online solver at editor.planning.domains. The online solver only returns a plan, though. It doesn't report expansion counts or timings, and it doesn't let me choose between greedy best-first search, BFS and A*. So for the comparison in Task 3, I used a small STRIPS planner and a separate validator that I wrote in Python. They live in the `planner/` folder and read the `.pddl` files directly, so nothing about the problem is hard-coded.

- `search.py` does the grounding and runs Greedy Best-First Search (with the h_add heuristic), BFS, and a generic A* with the admissible h_max heuristic.
- `astar_fast.py` is a bitmask-based A* with a problem-specific admissible heuristic. I needed it because in the 7-rock scenario my generic h_max A* and BFS ran out of memory.
- `validate.py` replays a plan on the lifted domain, checks every precondition at every step and prints each state. It does the same job VAL would do.

Because the expansion counts and timings come from my own code, they won't match what Fast Downward would report. The plan lengths for the optimal configurations are true optima, though.

One limitation to be upfront about: in the extended scenario, BFS did not finish (it ran out of memory), so the optimal result there comes from A* only.

## 1. Modelling (Tasks 1 and 2)

**Domain.pddl** uses only `:strips` and `:typing`. The types are `location`, `rover`, `bay`, `drill` and `rock`. The actions are `move`, `pick-drill`, `collect-soft`, `collect-hard` (which needs `has-drill`) and `deposit`.

Since negative preconditions aren't allowed, I handled two things with positive facts instead:
- Whether a rock is soft or hard is a static predicate, and there are two separate collect actions, one per type.
- An empty bay is its own fact, `bay-empty`, rather than "not holding anything".

Routes are directed `connected` facts. A two-way route is written as two facts, and the steep slope SiteC to SiteD has just one.

**Problem_extended.pddl** adds Rock6 (soft, at SiteE) and Rock7 (hard, at SiteF). Both `connected` facts for Base and SiteB are removed to model the dust storm. The goal is Rock1 to Rock7 at Base, both bays empty, and the rover at Base.

## 2. Results (Task 3)

| Scenario | Configuration | Plan length | Expanded | Generated | Time (s) |
|---|---|---|---|---|---|
| Original | GBFS (h_add), satisficing | 34 | 78 | 220 | 0.1642 |
| Original | BFS, optimal | 25 | 332,520 | 337,037 | 6.5657 |
| Original | A* (generic h_max), optimal | 25 | 171,880 | 249,252 | 145.5084 |
| Original | A* (problem-specific h), optimal | 25 | 6,275 | 13,417 | 0.1937 |
| Extended | GBFS (h_add), satisficing | 61 | 722 | 1,651 | 0.9584 |
| Extended | A* (problem-specific h), optimal | 40 | 1,575,606 | 2,958,057 | 65.0467 |

The plan length and the total number of actions are the same thing here, since each plan is just a list of actions.

### Plans

The BFS plan for the original problem is also 25 actions long but is a different plan from the A* one. It's saved in `output/original_bfs.txt`.

**Original, satisficing (GBFS), 34 actions**
```
 1. (move curiosity base sitea)
 2. (collect-soft curiosity rock1 sitea bay1)
 3. (move curiosity sitea base)
 4. (deposit curiosity rock1 base bay1)
 5. (move curiosity base siteb)
 6. (collect-soft curiosity rock2 siteb bay1)
 7. (move curiosity siteb base)
 8. (deposit curiosity rock2 base bay1)
 9. (move curiosity base sitea)
10. (move curiosity sitea sitec)
11. (move curiosity sitec sited)
12. (collect-soft curiosity rock4 sited bay1)
13. (move curiosity sited siteb)
14. (move curiosity siteb base)
15. (deposit curiosity rock4 base bay1)
16. (move curiosity base sitea)
17. (move curiosity sitea sitec)
18. (move curiosity sitec sitee)
19. (pick-drill curiosity drill1 sitee)
20. (move curiosity sitee sitec)
21. (collect-hard curiosity rock3 sitec bay1 drill1)
22. (move curiosity sitec sitea)
23. (move curiosity sitea base)
24. (deposit curiosity rock3 base bay1)
25. (move curiosity base sitea)
26. (move curiosity sitea sitec)
27. (move curiosity sitec sitee)
28. (move curiosity sitee sitef)
29. (collect-hard curiosity rock5 sitef bay1 drill1)
30. (move curiosity sitef sitee)
31. (move curiosity sitee sitec)
32. (move curiosity sitec sitea)
33. (move curiosity sitea base)
34. (deposit curiosity rock5 base bay1)
```

**Original, optimal (A*), 25 actions**
```
 1. (move curiosity base siteb)
 2. (collect-soft curiosity rock2 siteb bay1)
 3. (move curiosity siteb sited)
 4. (collect-soft curiosity rock4 sited bay2)
 5. (move curiosity sited siteb)
 6. (move curiosity siteb base)
 7. (deposit curiosity rock2 base bay1)
 8. (deposit curiosity rock4 base bay2)
 9. (move curiosity base sitea)
10. (move curiosity sitea sitec)
11. (move curiosity sitec sitee)
12. (pick-drill curiosity drill1 sitee)
13. (move curiosity sitee sitef)
14. (collect-hard curiosity rock5 sitef bay1 drill1)
15. (move curiosity sitef sitee)
16. (move curiosity sitee sitec)
17. (collect-hard curiosity rock3 sitec bay2 drill1)
18. (move curiosity sitec sitea)
19. (move curiosity sitea base)
20. (deposit curiosity rock3 base bay2)
21. (move curiosity base sitea)
22. (collect-soft curiosity rock1 sitea bay2)
23. (move curiosity sitea base)
24. (deposit curiosity rock1 base bay2)
25. (deposit curiosity rock5 base bay1)
```

**Extended, satisficing (GBFS), 61 actions**
```
 1. (move curiosity base sitea)
 2. (collect-soft curiosity rock1 sitea bay1)
 3. (move curiosity sitea base)
 4. (deposit curiosity rock1 base bay1)
 5. (move curiosity base sitea)
 6. (move curiosity sitea sitec)
 7. (move curiosity sitec sitee)
 8. (pick-drill curiosity drill1 sitee)
 9. (move curiosity sitee sitec)
10. (collect-hard curiosity rock3 sitec bay1 drill1)
11. (move curiosity sitec sitea)
12. (move curiosity sitea base)
13. (deposit curiosity rock3 base bay1)
14. (move curiosity base sitea)
15. (move curiosity sitea sitec)
16. (move curiosity sitec sitee)
17. (collect-soft curiosity rock6 sitee bay1)
18. (move curiosity sitee sitec)
19. (move curiosity sitec sitea)
20. (move curiosity sitea base)
21. (deposit curiosity rock6 base bay1)
22. (move curiosity base sitea)
23. (move curiosity sitea sitec)
24. (move curiosity sitec sited)
25. (collect-soft curiosity rock4 sited bay1)
26. (move curiosity sited sitee)
27. (move curiosity sitee sitec)
28. (move curiosity sitec sitea)
29. (move curiosity sitea base)
30. (deposit curiosity rock4 base bay1)
31. (move curiosity base sitea)
32. (move curiosity sitea sitec)
33. (move curiosity sitec sitee)
34. (move curiosity sitee sitef)
35. (collect-hard curiosity rock5 sitef bay1 drill1)
36. (move curiosity sitef sitee)
37. (move curiosity sitee sitec)
38. (move curiosity sitec sitea)
39. (move curiosity sitea base)
40. (deposit curiosity rock5 base bay1)
41. (move curiosity base sitea)
42. (move curiosity sitea sitec)
43. (move curiosity sitec sitee)
44. (move curiosity sitee sitef)
45. (collect-hard curiosity rock7 sitef bay1 drill1)
46. (move curiosity sitef sitee)
47. (move curiosity sitee sitec)
48. (move curiosity sitec sitea)
49. (move curiosity sitea base)
50. (deposit curiosity rock7 base bay1)
51. (move curiosity base sitea)
52. (move curiosity sitea sitec)
53. (move curiosity sitec sited)
54. (move curiosity sited siteb)
55. (collect-soft curiosity rock2 siteb bay1)
56. (move curiosity siteb sited)
57. (move curiosity sited sitee)
58. (move curiosity sitee sitec)
59. (move curiosity sitec sitea)
60. (move curiosity sitea base)
61. (deposit curiosity rock2 base bay1)
```

**Extended, optimal (A*), 40 actions**
```
 1. (move curiosity base sitea)
 2. (move curiosity sitea sitec)
 3. (move curiosity sitec sited)
 4. (collect-soft curiosity rock4 sited bay1)
 5. (move curiosity sited siteb)
 6. (collect-soft curiosity rock2 siteb bay2)
 7. (move curiosity siteb sited)
 8. (move curiosity sited sitee)
 9. (pick-drill curiosity drill1 sitee)
10. (move curiosity sitee sitec)
11. (move curiosity sitec sitea)
12. (move curiosity sitea base)
13. (deposit curiosity rock2 base bay2)
14. (deposit curiosity rock4 base bay1)
15. (move curiosity base sitea)
16. (move curiosity sitea sitec)
17. (move curiosity sitec sitee)
18. (move curiosity sitee sitef)
19. (collect-hard curiosity rock5 sitef bay1 drill1)
20. (collect-hard curiosity rock7 sitef bay2 drill1)
21. (move curiosity sitef sitee)
22. (move curiosity sitee sitec)
23. (move curiosity sitec sitea)
24. (move curiosity sitea base)
25. (deposit curiosity rock5 base bay1)
26. (deposit curiosity rock7 base bay2)
27. (move curiosity base sitea)
28. (move curiosity sitea sitec)
29. (move curiosity sitec sitee)
30. (collect-soft curiosity rock6 sitee bay1)
31. (move curiosity sitee sitec)
32. (collect-hard curiosity rock3 sitec bay2 drill1)
33. (move curiosity sitec sitea)
34. (move curiosity sitea base)
35. (deposit curiosity rock3 base bay2)
36. (move curiosity base sitea)
37. (collect-soft curiosity rock1 sitea bay2)
38. (move curiosity sitea base)
39. (deposit curiosity rock1 base bay2)
40. (deposit curiosity rock6 base bay1)
```

### Independent cross-check with an online solver

Since I wrote my own planner, I also wanted an outside check that my PDDL files are correct. I ran the same `Domain.pddl`, `Problem.pddl` and `Problem_extended.pddl` on the online solver at editor.planning.domains (solver used: [solver name]). It found valid plans for both scenarios:

| Scenario | Online solver plan length | My optimal (A*) |
|---|---|---|
| Original | 31 | 25 |
| Extended | 57 | 40 |

Both plans are longer than the optimum, which is what I'd expect, since that solver is satisficing and doesn't promise the shortest plan. They fall between my GBFS and A* results (34 and 25 for the original, 61 and 40 for the extended one). I checked both plans step by step against the domain and they are valid: all routes exist, the one-way slope is only used from SiteC to SiteD, the drill is picked up before any hard rock, and everything ends at Base with both bays empty.

One thing I noticed in the extended plan: the solver drops Rock5 at SiteA (step 11), goes to Base, comes back to SiteA, and picks it up again before carrying it home. That's allowed, since a rock can be deposited anywhere the rover is, but it wastes four actions. It's a good example of why satisficing plans end up longer than optimal ones.

The plans are saved in `output/online_solver_original.txt` and `output/online_solver_extended.txt`. I did not use them for the results table or the analysis below, because the online solver doesn't report expansion counts or timings in the form Task 3 asks for.

## 3. Goal verification (Task 4)

I simulated every plan in `output/` step by step, checking all preconditions at each step. The logs are in `output/validation_*.txt`, and all six plans came out valid.

For the optimal original plan, the final state is:
```
(rock-at rock1..rock5 base), (bay-empty bay1), (bay-empty bay2),
(rover-at curiosity base), (has-drill curiosity drill1)
```
All five rocks are at Base, both bays are empty, and the rover is at Base. The extended plans check out the same way, with Rock1 to Rock7 all at Base. (The rover still holds the drill at the end, but the goal doesn't ask for it to be dropped.)

## 4. Analysis (Task 6)

### Q1. How do the satisficing and optimal plan lengths compare?

| Scenario | GBFS | Optimal | Difference |
|---|---|---|---|
| Original | 34 | 25 | 9 more (about 36% longer) |
| Extended | 61 | 40 | 21 more (about 52% longer) |

Both configurations do exactly the same number of non-move actions: 11 in the original (5 collects, 5 deposits, 1 pick-drill) and 15 in the extended scenario (7 collects, 7 deposits, 1 pick-drill). So the entire gap comes from `move` actions: 23 versus 14 in the original, and 46 versus 25 in the extended one.

The reason is how GBFS works. It chases the h_add estimate greedily, so it grabs one rock, goes back to Base, deposits it, and heads out again. That's one round trip per rock, and it never touches Bay2 at all (zero uses in both GBFS plans). The plan is valid, just wasteful. A* and BFS can't settle for that, because they have to show that nothing shorter exists. That pushes them to carry two rocks per trip and to combine trips.

The trade-off is search effort. GBFS needed only 78 expansions for the original problem, compared with 6,275 for A* and 332,520 for BFS, but it gives no guarantee about plan length. The extended scenario makes the gap bigger, because every extra rock from the far end of the map (SiteF or SiteE) costs a full 8-move round trip.

### Q2. How does the optimal plan use the two bays, and when is the drill picked up?

The optimal original plan has 25 actions: 11 non-move actions and the minimum possible 14 moves.

- **Trip 1 (no drill needed).** Base to SiteB, collect Rock2 into Bay1. Then to SiteD, collect Rock4 into Bay2. Both bays are now full. Back through SiteB to Base, and deposit both (steps 1 to 8).
- **Trip 2 (the drill trip).** Base to SiteA to SiteC to SiteE, where the rover picks up the drill (step 12). Then to SiteF to collect hard Rock5 into Bay1, back to SiteC to collect hard Rock3 into Bay2, and home to Base to deposit Rock3, which frees Bay2 (step 20).
- **Last bit.** Base to SiteA, collect Rock1 into Bay2, back to Base, deposit Rock1, and finally deposit Rock5 (steps 21 to 25).

So Bay1 holds Rock5 from step 14 all the way to step 25, while Bay2 gets reused for Rock3 and then Rock1. The drill is picked up as late as possible, at SiteE, which is exactly where the rover first needs it on the way to the hard rocks. The first trip doesn't need it, so there's no reason to fetch it earlier.

The BFS plan is a different but equally short alternative. It does the drill trip first (drill picked up at step 4) and the SiteB/SiteD trip last. Every optimal plan for this problem has 14 moves.

### Q3. How does the rover reach SiteB and SiteD after the dust storm, and is the one-way route used?

The optimal extended plan has 40 actions.

- **SiteB** can now only be reached through SiteD, since SiteB and SiteD are connected both ways and there is no other route in.
- **SiteD** is reached from Base via SiteA and SiteC, then across the one-way slope from SiteC to SiteD. That's 3 moves. The alternative is to go around through SiteE and then to SiteD.
- **Yes, the one-way route is used.** The optimal plan uses it exactly once (step 3, SiteC to SiteD), in its allowed direction. After collecting at SiteB, the rover goes back to SiteD and then to SiteE (steps 7 and 8). It can't go from SiteD to SiteC, so it comes home via SiteE, SiteC, SiteA and Base, picking up the drill at SiteE on the way (step 9). Taking the slope saves one move compared with going A, C, E, D. The GBFS plan also uses SiteC to SiteD (steps 24 and 53) and never tries the forbidden direction.

Compared with the original optimum of 25 actions, the extended optimum of 40 has 4 more non-move actions (for the two extra rocks) and 11 more moves. The storm forces the long detour to SiteB and SiteD through SiteA and SiteC, and every rock has to be carried home via SiteA.