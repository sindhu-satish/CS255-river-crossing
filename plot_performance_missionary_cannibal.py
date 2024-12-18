import requests
import time
import matplotlib.pyplot as plt

url = "http://127.0.0.1:5000/missionary-cannibal"

N_values = range(3, 11)
solvers = ["bfs", "dfs", "a_star"]

number_of_states_results = {solver: [] for solver in solvers}
output_size_results = {solver: [] for solver in solvers}

for N in N_values:
    base_payload = {
        "M_total": N,
        "C_total": N,
        "M_left": N,
        "C_left": N,
        "M_right": 0,
        "C_right": 0,
        "boat_position": "left",
        "boat_capacity": 4
    }
    
    for solver in solvers:
        payload = dict(base_payload)
        payload["solver"] = solver

        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            num_states = data.get("number_of_states", None)
            output_dict = data.get("output", {})
            output_size = len(output_dict)
            
            number_of_states_results[solver].append(num_states)
            output_size_results[solver].append(output_size)
        else:
            print(f"Error: N={N}, solver={solver}, status={response.status_code}")
            number_of_states_results[solver].append(None)
            output_size_results[solver].append(None)

plt.figure()
for solver in solvers:
    print(number_of_states_results[solver])
    plt.plot(list(N_values), number_of_states_results[solver], marker='o', label=solver.upper())
plt.xlabel("N (Missionaries = Cannibals)")
plt.ylabel("Number of States Traversed")
plt.title("N vs Number of States Traversed for Missionary-Cannibal")
plt.grid(True)
plt.legend()
plt.savefig("n_vs_number_of_states_all_solvers_mc.png")

plt.figure()
for solver in solvers:
    print(output_size_results[solver])
    plt.plot(list(N_values), output_size_results[solver], marker='o', label=solver.upper())
plt.xlabel("N (Missionaries = Cannibals)")
plt.ylabel("Number of steps in output")
plt.title("N vs number of steps in output for Missionary-Cannibal")
plt.grid(True)
plt.legend()
plt.savefig("n_vs_output_size_all_solvers_mc.png")
