#!/bin/bash
# Reproduce everything (Python 3.10+, no external packages)
set -e
cd "$(dirname "$0")/planner"
mkdir -p ../output

D=../pddl/Domain.pddl
P=../pddl/Problem.pddl
E=../pddl/Problem_extended.pddl
O=../output

# Original scenario
python3 search.py $D $P gbfs  $O/original_gbfs.txt
python3 search.py $D $P bfs   $O/original_bfs.txt
python3 search.py $D $P astar $O/original_astar_hmax.txt   # generic h_max, slow (a few minutes)
python3 astar_fast.py $D $P   $O/original_astar.txt

# Extended scenario
python3 search.py $D $E gbfs  $O/extended_gbfs.txt
python3 astar_fast.py $D $E   $O/extended_astar.txt        # ~1 min

# Validation (step-by-step goal check)
for s in gbfs bfs astar astar_hmax; do
  python3 validate.py $D $P $O/original_$s.txt $O/validation_original_$s.txt
done
for s in gbfs astar; do
  python3 validate.py $D $E $O/extended_$s.txt $O/validation_extended_$s.txt
done