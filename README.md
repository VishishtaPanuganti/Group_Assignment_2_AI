# Artificial Intelligence – Group Assignment 2

**Course:** Artificial Intelligence (AI)  
**Assignment:** Group Assignment 2  
**Institution:** Indian Institute of Technology Bhilai  
**Team Size:** 5 Members

### Team Members

| S. No. | Name | Roll Number |
|:---:|---|:---:|
| 1 | Panuganti Vishishta | B24DS021 |
| 2 | Nandyala Vaishnavi | B24DS020 |
| 3 | Namburi Veda Aishwarya | B24DS019 |
| 4 | Kollati Devi Chandrika | B24DS011 |
| 5 | Chaitrali Zode | B24EE013 |

**Repository:** [Group_Assignment_2_AI](https://github.com/VishishtaPanuganti/Group_Assignment_2_AI)

---

## 📌 Overview

This repository contains the implementation and analysis of problems from the Artificial Intelligence Group Assignment 2.

The assignment explores fundamental AI techniques, including search algorithms, adversarial search, state-space exploration, and automated planning.

The objective is to understand how different AI approaches represent problems, explore possible states, make decisions, and generate solutions.

## 📂 Repository Structure

```text
Group_Assignment_2_AI/
│
├── Problem_1/
│   └── BFS / DFS implementation and related files
│
├── PROBLEM 3/
│   └── Minimax / Alpha-Beta implementation and related files
│
├── mars_rover/
│   ├── planner/
│   ├── search/
│   ├── validation/
│   ├── outputs/
│   ├── Analysis_Report.md
│   ├── README.md
│   ├── PDDL domain and problem files
│   └── run_all.sh
│
├── .gitignore
│
└── README.md
```

## 🧠 Problems and Implementations

### 1. Problem 1 – Uninformed Search

**Algorithms: Breadth-First Search (BFS) and Depth-First Search (DFS)**

This problem explores uninformed search techniques for navigating a state space and finding a path from an initial state to a goal state.

**Concepts Covered:**
- State-space representation
- Initial and goal states
- Successor generation
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Path reconstruction
- Search performance comparison

**Learning Objectives:**
- Understand how search algorithms explore states.
- Compare BFS and DFS in terms of completeness and optimality.
- Analyze search performance using relevant metrics.

### 2. Problem 3 – Adversarial Search

**Algorithms: Minimax and Alpha-Beta Pruning**

This problem focuses on decision-making in competitive environments where two players have opposing objectives.

**Concepts Covered:**
- Game-state representation
- Game trees
- Player turns and legal moves
- Minimax algorithm
- Alpha-Beta pruning
- Evaluation functions
- Depth-limited search
- Search efficiency and pruning analysis

**Learning Objectives:**
- Understand optimal decision-making in two-player games.
- Explore game trees using Minimax.
- Improve search efficiency using Alpha-Beta pruning.
- Compare the performance of both approaches.

### 3. Mars Rover – Automated Planning

**Approach: PDDL-based Planning and Search**

This problem models a Mars Rover mission using Artificial Intelligence planning techniques.

The rover operates in a predefined environment and must perform mission-related actions while satisfying the specified initial conditions and goal conditions.

**Concepts Covered:**
- Planning Domain Definition Language (PDDL)
- Domain and problem representation
- Predicates and actions
- Preconditions and effects
- Initial-state representation
- Goal-state representation
- State-space planning
- Plan generation and validation

**Project Components:**

| Component | Purpose |
|---|---|
| PDDL Domain | Defines the planning environment and available actions |
| PDDL Problem | Defines objects, initial state, and goals |
| Planner | Handles planning and plan generation |
| Search | Supports state-space exploration |
| Validation | Checks generated plans |
| Outputs | Stores execution results |
| Analysis Report | Documents the problem and analysis |

A separate report is provided in `mars_rover/Analysis_Report.md`.

---

## 🛠️ Technologies and Tools

The project uses the following technologies and tools:

- **Python 3** – Algorithm implementation and supporting scripts.
- **PDDL** – Representation of planning domains and problems.
- **Bash** – Automation of execution workflows.
- **Git and GitHub** – Version control and collaborative development.

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/VishishtaPanuganti/Group_Assignment_2_AI.git
```

### 2. Navigate to the Project

```bash
cd Group_Assignment_2_AI
```

### 3. Run the Mars Rover Workflow

On Linux or Ubuntu/WSL:

```bash
cd mars_rover
chmod +x run_all.sh
./run_all.sh
```

This executes the workflow configured in the Mars Rover directory.

### 4. Run Other Problem Implementations

Navigate to the respective problem directory and follow the execution instructions and dependencies provided with its implementation.

---

## 📊 Learning Outcomes

Through this assignment, we explore:

1. **Uninformed Search:** Understanding BFS and DFS for systematic state-space exploration.
2. **Adversarial Search:** Applying Minimax and Alpha-Beta pruning to competitive decision-making.
3. **Automated Planning:** Representing real-world tasks through PDDL and generating valid plans.
4. **Algorithm Analysis:** Understanding search efficiency, state exploration, and solution quality.
5. **Collaborative Development:** Using Git and GitHub for team-based software development.

## 👥 Team Collaboration

This assignment is developed collaboratively by a team of five members.

The team uses Git and GitHub to:

- Maintain a shared project repository.
- Develop individual contributions in separate branches.
- Review and integrate changes.
- Maintain organized problem-specific directories.
- Track project progress through commits and merges.

Each member contributes to the assignment through implementation, testing, analysis, and documentation.

## 📚 References

- Artificial Intelligence course materials and lecture notes.
- Russell and Norvig, *Artificial Intelligence: A Modern Approach*.
- PDDL documentation and automated planning resources.
- Relevant algorithm and search literature.

---

## 📝 Conclusion

This assignment provides practical exposure to important Artificial Intelligence techniques, ranging from classical search algorithms to adversarial decision-making and automated planning.

By implementing and analyzing these approaches, the project demonstrates how AI algorithms can solve different categories of problems through state representation, systematic exploration, decision-making, and planning.

---

**Course:** Artificial Intelligence  
**Project:** Group Assignment 2  
**Institution:** IIT Bhilai  

[View Project Repository on GitHub](https://github.com/VishishtaPanuganti/Group_Assignment_2_AI)
