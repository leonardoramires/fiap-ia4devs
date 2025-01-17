def allocate_tasks(operators, tasks):
    # Sort operators by level (descending) and availability (ascending)
    operators.sort(key=lambda op: (-op['level'], op['availability']))
    # Sort tasks by complexity (descending)
    tasks.sort(key=lambda task: -task['complexity'])

    allocation = {}
    for task in tasks:
        for operator in operators:
            if operator['availability'] > 0:
                if operator['name'] not in allocation:
                    allocation[operator['name']] = []
                allocation[operator['name']].append(task['id'])
                operator['availability'] -= 1
                break

    return allocation

# Example usage
if __name__ == "__main__":
    operators = [
        {"name": "Alice", "level": 5, "availability": 3},
        {"name": "Bob", "level": 3, "availability": 2},
        {"name": "Charlie", "level": 4, "availability": 1}
    ]

    tasks = [
        {"id": 1, "complexity": 10},
        {"id": 2, "complexity": 5},
        {"id": 3, "complexity": 8},
        {"id": 4, "complexity": 7}
    ]

    allocation = allocate_tasks(operators, tasks)
    for operator, tasks in allocation.items():
        print(f"Operator {operator} is allocated tasks: {tasks}")
