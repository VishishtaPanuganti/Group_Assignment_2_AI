# Mars Rover PDDL: deliverables

- `pddl/Domain.pddl`, `pddl/Problem.pddl`, `pddl/Problem_extended.pddl`: the domain and the two problem files (original and extended scenario).
- `output/`: planner output for both scenarios (`original_*.txt`, `extended_*.txt`) and the step-by-step goal verification for each plan (`validation_*.txt`).
- `output/online_solver_original.txt`, `output/online_solver_extended.txt`: plans from the online solver at editor.planning.domains, used as an independent cross-check of the PDDL files.
- `Analysis_Report.md`: the full analysis (Tasks 3 to 6).
- `planner/`: the Python planner and validator used to generate the search results and the validation logs (see section 0 of the report).

The PDDL files were written in VS Code and also tested on the online editor at editor.planning.domains.