import requests
import json
import time
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:5000/jealous-husband"
n_values = list(range(3, 10))

solvers = ["bfs", "dfs", "a_star"]

number_of_states_results = {solver: [] for solver in solvers}
output_size_results = {solver: [] for solver in solvers}
time_taken_results = {solver: [] for solver in solvers}

for N in n_values:
    stage = {
        "left_bank": [("H", i+1) for i in range(N)] + [("W", i+1) for i in range(N)],
        "right_bank": [],
        "boat_position": "L"
    }

    for solver in solvers:
        payload = {
            "num_of_couples": N,
            "boat_capacity": 4,
            "solver": solver,
            "stage": stage
        }

        print("*"*10)
        print(payload)

        start_time = time.time()
        response = requests.post(API_URL, json=payload)
        end_time = time.time()

        if response.status_code == 200:
            data = response.json()
            num_states = data.get("number_of_states", None)
            
            output_dict = data.get("output", {})
            output_size = len(output_dict)

            number_of_states_results[solver].append(num_states)
            output_size_results[solver].append(output_size)
            time_taken_results[solver].append(end_time - start_time)
        else:
            number_of_states_results[solver].append(None)
            output_size_results[solver].append(None)
            time_taken_results[solver].append(None)
            print(f"Error with N={N}, solver={solver}: {response.status_code} - {response.text}")

plt.figure()
for solver in solvers:
    plt.plot(n_values, number_of_states_results[solver], marker='o', alpha=0.6, label=solver.upper())
plt.xlabel("Number of Couples (N)")
plt.ylabel("Number of States Traversed")
plt.title("N vs Number of States Traversed - Jealous Husbands")
plt.grid(True)
plt.legend()
plt.savefig("n_vs_number_of_states_all_solvers_jh.png")

plt.figure()
for solver in solvers:
    print(output_size_results[solver])
    plt.plot(n_values, output_size_results[solver], marker='o', alpha=0.7, label=solver.upper())
plt.xlabel("Number of couples (N)")
plt.ylabel("Number of steps in the solution (len(output))")
plt.title("N vs Number of steps in the solution - Jealous Husbands")
plt.grid(True)
plt.legend()
plt.savefig("n_vs_output_size_all_solvers_jh.png")
