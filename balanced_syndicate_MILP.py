"""
Balanced Syndicate Group Optimisation
Author: Giwa Iziomo

Purpose:
Assign students into balanced syndicate groups to maximise diversity 
while maintaining fairness by gender and quantitative background.

Input:
 - balanced_syndicate_dataset.xlsx
Outputs:
 - balanced_groups_output.csv
 - balanced_groups_summary.xlsx
"""

import pandas as pd
import pulp

# ------------------------------------------------------------
# 1. Load dataset
# ------------------------------------------------------------
file_name = "balanced_syndicate_dataset.xlsx"
df = pd.read_excel(file_name)

# Expected columns:
# StudentID | Nationality | Cultural Background | Gender | Quantitative Background
df["StudentID"] = df["StudentID"].astype(str)
df["Gender"] = df["Gender"].astype(str).str.strip().str.upper().map({"M": 0, "F": 1})
df["Quantitative Background"] = df["Quantitative Background"].astype(int)
df["International"] = (df["Nationality"].astype(str).str.lower() != "british").astype(int)

print(f"Loaded {len(df)} students from {file_name}")

# ------------------------------------------------------------
# 2. Define sets and parameters
# ------------------------------------------------------------
students = df["StudentID"].tolist()
n_students = len(students)
n_groups = n_students // 5
groups = [f"G{i+1}" for i in range(n_groups)]

gender = df.set_index("StudentID")["Gender"].to_dict()
quant = df.set_index("StudentID")["Quantitative Background"].to_dict()
intl = df.set_index("StudentID")["International"].to_dict()
nat = df.set_index("StudentID")["Nationality"].to_dict()
cult = df.set_index("StudentID")["Cultural Background"].to_dict()

nat_values = sorted({nat[s] for s in students if intl[s] == 1})
cult_values = sorted({cult[s] for s in students if intl[s] == 1})

# ------------------------------------------------------------
# 3. Build MILP Model
# ------------------------------------------------------------
model = pulp.LpProblem("Balanced_Syndicate_Groups", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", (students, groups), 0, 1, cat="Binary")
F = pulp.LpVariable.dicts("Females", groups, lowBound=0)
Q = pulp.LpVariable.dicts("Quant", groups, lowBound=0)
T_nat = {(n,g): pulp.LpVariable(f"T_nat[{n},{g}]", lowBound=0) for n in nat_values for g in groups}
P_nat = {(n,g): pulp.LpVariable(f"P_nat[{n},{g}]", lowBound=0) for n in nat_values for g in groups}
T_cul = {(c,g): pulp.LpVariable(f"T_cul[{c},{g}]", lowBound=0) for c in cult_values for g in groups}
P_cul = {(c,g): pulp.LpVariable(f"P_cul[{c},{g}]", lowBound=0) for c in cult_values for g in groups}

# Objective: maximise nationality pairing (100) + cultural pairing (10)
model += (
    100 * pulp.lpSum(P_nat[n,g] for n in nat_values for g in groups) +
     10 * pulp.lpSum(P_cul[c,g] for c in cult_values for g in groups)
)

# ------------------------------------------------------------
# 4. Constraints
# ------------------------------------------------------------
# Each student assigned to exactly one group
for s in students:
    model += pulp.lpSum(x[s][g] for g in groups) == 1

# Group size = 5
for g in groups:
    model += pulp.lpSum(x[s][g] for s in students) == 5

    # Gender balance (2–3 females per group)
    model += F[g] == pulp.lpSum(gender[s]*x[s][g] for s in students)
    model += F[g] >= 2
    model += F[g] <= 3

    # Quantitative background balance (2–3 per group)
    model += Q[g] == pulp.lpSum(quant[s]*x[s][g] for s in students)
    model += Q[g] >= 2
    model += Q[g] <= 3

# Nationality pairing
for n in nat_values:
    same_nat = [s for s in students if intl[s] == 1 and nat[s] == n]
    for g in groups:
        model += T_nat[n,g] == pulp.lpSum(x[s][g] for s in same_nat)
        model += P_nat[n,g] <= 0.5 * T_nat[n,g]

# Cultural pairing
for c in cult_values:
    same_cul = [s for s in students if intl[s] == 1 and cult[s] == c]
    for g in groups:
        model += T_cul[c,g] == pulp.lpSum(x[s][g] for s in same_cul)
        model += P_cul[c,g] <= 0.5 * T_cul[c,g]

# ------------------------------------------------------------
# 5. Solve
# ------------------------------------------------------------
model.solve(pulp.PULP_CBC_CMD(msg=False))

print(f"\nSolver Status: {pulp.LpStatus[model.status]}")
print(f"Objective Value (pairing score): {pulp.value(model.objective):,.2f}")

# ------------------------------------------------------------
# 6. Export Results
# ------------------------------------------------------------
assignments = []
for g in groups:
    for s in students:
        if x[s][g].value() > 0.5:
            assignments.append((s, g))

df_out = pd.DataFrame(assignments, columns=["StudentID", "Group"]).sort_values(["Group", "StudentID"])
df_out = df_out.merge(df, on="StudentID", how="left")

# Group summaries
summaries = []
for g in groups:
    members = df_out[df_out["Group"] == g]
    summaries.append({
        "Group": g,
        "Members": ", ".join(members["StudentID"].tolist()),
        "Females": members["Gender"].sum(),
        "Quant": members["Quantitative Background"].sum(),
        "Nationalities": members["Nationality"].value_counts().to_dict(),
        "Cultures": members["Cultural Background"].value_counts().to_dict()
    })

summary_df = pd.DataFrame(summaries)
df_out.to_csv("balanced_groups_output.csv", index=False)
summary_df.to_excel("balanced_groups_summary.xlsx", index=False)

print("\nResults exported:")
print(" - balanced_groups_output.csv")
print(" - balanced_groups_summary.xlsx\n")
