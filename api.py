import jealous_husbands_a_star
import jealous_husbands_bfs
import jealous_husbands_dfs
import missionary_cannibal_a_star
import missionary_cannibal_solver_bfs
import missionary_cannibal_solver_dfs

from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/")
def test():
    return "Server running"


@app.route("/missionary-cannibal")
def missionary_cannibal():
    parameters = json.loads(request.data)
    print(parameters)
    M_total = parameters["M_total"]
    C_total = parameters["C_total"]
    M_left = parameters["M_left"]
    C_left = parameters["C_left"]
    M_right = parameters["M_right"]
    C_right = parameters["C_right"]
    boat_position = parameters["boat_position"]
    solver = parameters["solver"]
    if solver == "bfs":
        return json.dumps(missionary_cannibal_solver_bfs.solve_missionaries_cannibals(M_total, C_total, M_left, C_left, M_right, C_right, boat_position))
    if solver == "dfs":
        return json.dumps(missionary_cannibal_solver_dfs.solve_missionaries_cannibals(M_total, C_total, M_left, C_left, M_right, C_right, boat_position))
    if solver == "a_star":
        return json.dumps(missionary_cannibal_a_star.solve_missionaries_cannibals(M_total, C_total, M_left, C_left, M_right, C_right, boat_position))
    

    
if __name__ == "__main__":
    app.run(debug=True)
