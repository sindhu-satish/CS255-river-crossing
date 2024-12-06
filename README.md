# CS255-river-crossing

## SETUP
```cmd
pip install -r requirements.txt
```

```cmd
python api.py
```

## API Call
### Missionary Cannibal
```cmd
curl -X GET \
  -H "Content-Type: application/json" \
  -d '{"num_of_couples": 3, "solver": "my_solver"}' \
  http://localhost:5000/jealous-husband
```

### Jealous Husbands
```cmd
curl -X GET \
  -H "Content-Type: application/json" \
  -d '{
    "M_total": 3,
    "C_total": 3,
    "M_left": 3,
    "C_left": 3,
    "M_right": 0,
    "C_right": 0,
    "boat_position": "left",
    "solver": "bfs"
  }' \
  http://localhost:5000/missionary-cannibal
```

## Output format
### Missionary Cannibal
```json
{
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
    "4": {
        "M_left": 3,
        "C_left": 1,
        "M_right": 0,
        "C_right": 2,
        "boat_position": "left"
    },
    "5": {
        "M_left": 1,
        "C_left": 1,
        "M_right": 2,
        "C_right": 2,
        "boat_position": "right"
    },
    "6": {
        "M_left": 2,
        "C_left": 2,
        "M_right": 1,
        "C_right": 1,
        "boat_position": "left"
    },
    "7": {
        "M_left": 0,
        "C_left": 2,
        "M_right": 3,
        "C_right": 1,
        "boat_position": "right"
    },
    "8": {
        "M_left": 0,
        "C_left": 3,
        "M_right": 3,
        "C_right": 0,
        "boat_position": "left"
    },
    "9": {
        "M_left": 0,
        "C_left": 1,
        "M_right": 3,
        "C_right": 2,
        "boat_position": "right"
    },
    "10": {
        "M_left": 1,
        "C_left": 1,
        "M_right": 2,
        "C_right": 2,
        "boat_position": "left"
    },
    "11": {
        "M_left": 0,
        "C_left": 0,
        "M_right": 3,
        "C_right": 3,
        "boat_position": "right"
    }
}
```

### Jealous Husbands
```json
{
    "0": 
        {"left_bank": [["H", 1], ["H", 2], ["H", 3], ["W", 1], ["W", 2], ["W", 3]], 
        "right_bank": [], 
        "boat_position": "L"}, 
    "1": 
        {"left_bank": [["H", 1], ["H", 2], ["H", 3], ["W", 1]], 
        "right_bank": [["W", 2], ["W", 3]], 
        "boat_position": "R"}, 
    "2": 
        {"left_bank": [["H", 1], ["H", 2], ["H", 3], ["W", 1], ["W", 3]], 
        "right_bank": [["W", 2]], 
        "boat_position": "L"}, 
    "3": 
        {"left_bank": [["H", 1], ["H", 2], ["H", 3]], 
        "right_bank": [["W", 1], ["W", 2], ["W", 3]], 
        "boat_position": "R"}, 
    "4": 
        {"left_bank": [["H", 1], ["H", 2], ["H", 3], ["W", 3]], 
        "right_bank": [["W", 1], ["W", 2]], 
        "boat_position": "L"},
    "5": 
        {"left_bank": [["H", 3], ["W", 3]], 
        "right_bank": [["H", 1], ["H", 2], ["W", 1], ["W", 2]], 
        "boat_position": "R"}
}
```