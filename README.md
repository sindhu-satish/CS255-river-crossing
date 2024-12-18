# CS255-river-crossing

## SETUP
```cmd
pip install -r requirements.txt
```

```cmd
python -m flask run
```

## API Call

### Missionary Cannibal
```cmd
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "M_total": 3,
    "C_total": 3,
    "M_left": 3,
    "C_left": 3,
    "M_right": 0,
    "C_right": 0,
    "boat_position": "left",
    "boat_capacity": 4,
    "solver": "bfs"
  }' \
  http://localhost:5000/missionary-cannibal
```

### Jealous Husbands
```cmd
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "num_of_couples": 4, 
    "solver": "a_star",
    "boat_capacity": 4,
    "stage": {
        "left_bank": [["H",1], ["W",1], ["H",2], ["W",2]],
        "right_bank": [["H",3], ["W",3], ["H",4], ["W",4]],
        "boat_position": "R"
    }
}' \
http://localhost:5000/jealous-husband
```

## Output format

### Missionary Cannibal
```json
{
  "output": {
    "0": {
      "M_left": 3,
      "C_left": 3,
      "M_right": 0,
      "C_right": 0,
      "boat_position": "left"
    },
    "1": {
      "M_left": 3,
      "C_left": 1,
      "M_right": 0,
      "C_right": 2,
      "boat_position": "right"
    },
    "2": {
      "M_left": 3,
      "C_left": 2,
      "M_right": 0,
      "C_right": 1,
      "boat_position": "left"
    },
    "3": {
      "M_left": 3,
      "C_left": 0,
      "M_right": 0,
      "C_right": 3,
      "boat_position": "right"
    },
    ...
    "11": {
      "M_left": 0,
      "C_left": 0,
      "M_right": 3,
      "C_right": 3,
      "boat_position": "right"
    }
  },
  "number_of_states": 15
}
```

### Jealous Husbands
```json
{
  "output": {
    "0": {
      "left_bank": [
        ["H", 1], ["H", 2], ["H", 3], ["H", 4], ["H", 5], ["H", 6], ["H", 7], ["H", 8], ["H", 9], ["H", 10], ["H", 11],
        ["W", 1], ["W", 2], ["W", 3], ["W", 4], ["W", 5], ["W", 6], ["W", 7], ["W", 8], ["W", 9], ["W", 10], ["W", 11]
      ],
      "right_bank": [],
      "boat_position": "L"
    },
    "1": {
      "left_bank": [
        ["H", 1], ["H", 2], ["H", 3], ["H", 4], ["H", 5], ["H", 6], ["H", 7], ["H", 8], ["H", 9], ["H", 10], ["H", 11],
        ["W", 1], ["W", 3], ["W", 5], ["W", 6], ["W", 7], ["W", 9], ["W", 10]
      ],
      "right_bank": [["W", 2], ["W", 4], ["W", 8], ["W", 11]],
      "boat_position": "R"
    },
    "2": {
      "left_bank": [
        ["H", 1], ["H", 2], ["H", 3], ["H", 4], ["H", 5], ["H", 6], ["H", 7], ["H", 8], ["H", 9], ["H", 10], ["H", 11],
        ["W", 1], ["W", 2], ["W", 3], ["W", 5], ["W", 6], ["W", 7], ["W", 8], ["W", 9], ["W", 10]
      ],
      "right_bank": [["W", 4], ["W", 11]],
      "boat_position": "L"
    },
    "3": {
      "left_bank": [
        ["H", 1], ["H", 2], ["H", 3], ["H", 4], ["H", 5], ["H", 6], ["H", 7], ["H", 8], ["H", 9], ["H", 10], ["H", 11],
        ["W", 2], ["W", 3], ["W", 7], ["W", 8], ["W", 9]
      ],
      "right_bank": [["W", 1], ["W", 4], ["W", 5], ["W", 6], ["W", 10], ["W", 11]],
      "boat_position": "R"
    },
    ...
    "19": {
      "left_bank": [],
      "right_bank": [
        ["H", 1], ["H", 2], ["H", 3], ["H", 4], ["H", 5], ["H", 6], ["H", 7], ["H", 8], ["H", 9], ["H", 10], ["H", 11],
        ["W", 1], ["W", 2], ["W", 3], ["W", 4], ["W", 5], ["W", 6], ["W", 7], ["W", 8], ["W", 9], ["W", 10], ["W", 11]
      ],
      "boat_position": "R"
    }
  },
  "number_of_states": 11179
}
```

### Performance Analysis

This repository also includes performance analysis scripts that benchmark the solvers for both the Missionary-Cannibal and Jealous Husbands problems. These scripts evaluate the algorithms based on key metrics, such as:

- **Number of States Traversed**: Total states explored by the solver to reach a solution.
- **Solution Length**: Number of steps in the solution path.

To run the performance analysis, execute the respective Python scripts:

```bash
python plot_performance_missionary_cannibal.py
python plot_performance_jh.py
```

The resulting plots will be saved in the working directory as PNG files:
- `n_vs_number_of_states_all_solvers_mc.png`
- `n_vs_output_size_all_solvers_mc.png`
- `n_vs_number_of_states_all_solvers_jh.png`
- `n_vs_output_size_all_solvers_jh.png` 

These visualizations provide insights into the computational complexity and efficiency of the solvers.
