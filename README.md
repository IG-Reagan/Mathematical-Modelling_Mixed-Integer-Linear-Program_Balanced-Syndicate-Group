# Mathematical Modelling — Balanced Syndicate Group Optimisation

**Project Description:**  
Project optimises student group formation to maximise diversity using Mixed Integer Linear Programming, balancing gender and quantitative background along with cultural and nationality diversity across teams, based on data from `balanced_syndicate_dataset.xlsx`.

---

## Project Overview
This project formulates a **Mixed Integer Linear Programming (MILP)** model that automatically allocates students into balanced syndicate groups for collaborative academic work. The optimisation ensures each group is diverse, inclusive, and balanced across multiple demographic and academic attributes.

The dataset used is `balanced_syndicate_dataset.xlsx`, containing each student’s:
- Gender  
- Quantitative background  
- Nationality  
- Cultural background  

The model outputs the optimal group assignment and detailed summaries of diversity balance per group.

---

## Context and Motivation
Academic and corporate teams perform best when diverse perspectives are balanced with complementary skills.  
This project replicates a Balanced Syndicate Group allocation exercise from the **Decision Models coursework**, using real-world constraints to achieve:
- Equitable participation by gender and academic background  
- Cross-cultural collaboration by pairing international students by nationality or culture  
- Diversity maximisation across all groups  

---

## Model Type and Approach

| Objective | Model Type | Technique |
|------------|-------------|-----------|
| Allocate 45 students into balanced groups | **Mixed Integer Linear Programming (MILP)** | Solved with PuLP (CBC Solver) |

Each student is assigned to exactly one group of five.  
The model enforces:
- 2–3 females per group  
- 2–3 students with quantitative backgrounds  
- Maximum nationality and cultural pairing scores  

---

## Tools and Dependencies
- **Language:** Python 3.11  
- **Libraries:** PuLP, Pandas, OpenPyXL  
- **Solver:** CBC (default in PuLP)

To install dependencies:
```bash
pip install pulp pandas openpyxl
