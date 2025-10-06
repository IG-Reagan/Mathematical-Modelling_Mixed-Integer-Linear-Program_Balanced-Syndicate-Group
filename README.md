# Balanced Syndicate Group Optimisation (MILP)

A scalable Python implementation using **Mixed-Integer Linear Programming (MILP)** to automatically allocate students into highly balanced syndicate groups. The model's objective is to **maximise the average quantitative background** within groups while ensuring **diversity and balance** across gender and cultural categories.

This project was initially solved using OpenSolver in MS Excel but has been redeveloped in Python for increased versatility and scalability.

-----

## 1\. The Challenge: Creating "Balanced Groups"

Aston Business School's diverse student population presents an opportunity for enriched learning experiences, especially during group work. The goal is to form **"balanced groups"** that maximise internal diversity while minimising performance differences between groups. Manually creating these groups for a large class (45 students) is time-consuming and inefficient.

This project provides an automated system to produce optimal group allocations that satisfy specific balancing criteria derived from research on cultural diversity in learning environments.

-----

## 2\. Optimisation Goal and Approach

The core problem is formulated as a **Mixed-Integer Linear Program (MILP)** using the **PuLP** library in Python.

### Objective Function

In the design of this solution, the primary objective is to **Maximise the sum of quantitative backgrounds (Q) across all groups**. This acts as a proxy for balancing, as the constraints ensure that each group's average Q is as close as possible to the overall class mean.

Maximise: $\sum_{s} \sum_{g} x_{s, g} \cdot Q_s$

### Key Constraints

The model ensures the groups meet specific balance requirements:

1.  **Group Size**
      * **Total Students:** 45.
      * **Group Size:** Exactly **5** members per group.
      * **Total Groups:** **9**.
2.  **Gender Balance (G)**
      * The class has 24 Females and 21 Males.
      * **Constraint:** Each group must have between **2 and 3** members of each gender.
3.  **Quantitative Background Balance (Q)**
      * The overall class mean Q is **6.9756**.
      * **Constraint:** The average of Q scores in each group must be close to the group target average (6.9756).
4.  **Cultural/Nationality Balance (C/N)**
      * **Minimum British Students:** Ensures **at least 1 British student per group**.
      * **Distribution:** Constraints manage the distribution of six different cultural backgrounds across the 9 groups.
      * **Pairing:** The formulation is designed to encourage pairing non-British students of the same nationality (or cultural background) as a key diversity goal.

-----

## 3\. Data and Class Statistics

The model was applied to a dataset of **45 students**.

| Category | Group | Count | Target per Group (Avg.) |
| :--- | :--- | :--- | :--- |
| **Gender** | Female | **24** | **2.67** |
| | Male | **21** | **2.33** |
| **Cultural Background** | East Asia | **20** | **2.22** |
| | British | **9** | **1.00** |
| | Eastern Europe | **6** | **0.67** |
| | Middle East | **5** | **0.56** |
| | South Asia | **3** | **0.33** |
| | Western Europe | **2** | **0.22** |

-----

## 4\. Solution Metrics and Results

The MILP model successfully found an **Optimal Solution** with an Objective Value of **313.90**.

### Final Group Summary

| Group | Size | Females | Males | Avg\_Quant | East Asia | British | Eastern Europe | Middle East | South Asia | Western Europe |
|:--------|-------:|----------:|--------:|------------:|------------:|----------:|-----------------:|--------------:|-------------:|-----------------:|
| G1 | 5 | 2 | 3 | 7.04 | 2 | 1 | 1 | 1 | 0 | 0 |
| G2 | 5 | 3 | 2 | 7.04 | 2 | 1 | 1 | 1 | 0 | 0 |
| G3 | 5 | 3 | 2 | 7.12 | 3 | 1 | 0 | 0 | 0 | 1 |
| G4 | 5 | 2 | 3 | 6.96 | 2 | 1 | 0 | 1 | 1 | 0 |
| G5 | 5 | 2 | 3 | 6.78 | 2 | 1 | 1 | 1 | 0 | 0 |
| G6 | 5 | 3 | 2 | 7.04 | 2 | 1 | 2 | 0 | 0 | 0 |
| G7 | 5 | 3 | 2 | 6.76 | 3 | 1 | 0 | 0 | 1 | 0 |
| G8 | 5 | 3 | 2 | 6.78 | 2 | 1 | 0 | 1 | 0 | 1 |
| G9 | 5 | 3 | 2 | 7.26 | 2 | 1 | 1 | 0 | 1 | 0 |

-----

### Balance Metrics Summary

The constraints successfully ensured **perfect gender balance** and **minimal variance** in the Quantitative Background (Q) across all groups.

| Metric | Result |
| :--- | :--- |
| **Mean Group Average Q** | **6.9756** |
| **Standard Deviation** | **0.1624** |
| **Coefficient of Variation (CV)** | **2.33%** |

A low CV of **2.33%** demonstrates that the average Q for each group is only slightly deviated from the class mean, proving the groups are well balanced.

-----

## 5\. Usage and Setup

The solution is implemented in a Python Jupyter Notebook developed on Google Colab (`balanced_syndicate_group_MILP.ipynb`).

### Prerequisites

  * Python 3.x
  * **PuLP** for MILP solving.
  * **Pandas** and **NumPy** for data handling.

### Installation

The necessary libraries are installed automatically within the notebook:

```python
try:
    import pulp
except ImportError:
    # Installation logic for PuLP
    pass
```

### Run the Model

1.  Clone the repository.
2.  Ensure `balanced_syndicate_dataset.csv` is accessible.
3.  Run all cells in the Jupyter Notebook (`balanced_syndicate_group_MILP.ipynb`).

**Outputs:**
The script saves the results to two files:

  * `group_allocation.csv`: Detailed student assignments.
  * `group_statistics.csv`: Summary statistics for each of the 9 groups.

-----

## 6\. Initial OpenSolver (Excel) Solution

This Python implementation improves upon an initial solution I developed using **OpenSolver (see in this repository: Balanced Syndicate Group_OpenSolver.xlsx)** for MS Excel. The original Excel model had a Coefficient of Variation of **5.5%** for quantitative background. The Python/PuLP implementation provides a better result (CV of **2.33%**) and offers increased **versatility and scalability** that can be adopted for larger or more complex class structures.
