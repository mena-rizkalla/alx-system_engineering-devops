#!/usr/bin/python3
import sys
import requests
import csv
"""Export data in CSV file"""

def write_todos_to_csv(todos_of_user,filename="{}.csv".format(sys.argv[1])):
    """Writes the given todos to a CSV file, handling flattening and headers."""

    flattened_todos = []
    for todo in todos_of_user:
        # Flatten using loop (alternative: recursive flattening for deeper nesting)
        flattened_todo = {}
        for key1, value1 in todo.items():
            if isinstance(value1, dict):
                for key2, value2 in value1.items():
                    flattened_todo[key2] = value2
            else:
                flattened_todo[key1] = value1

        # Alternatively, flatten using chain.from_iterable (requires collections module):
        # flattened_todo = {key: value for key, value in chain.from_iterable((todo.items(), *[item.items() for item in todo.values() if isinstance(item, dict)]))}

        flattened_todos.append(flattened_todo)

    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=flattened_todos[0].keys(), quoting=csv.QUOTE_ALL)
        writer.writerows(flattened_todos)

if __name__ == '__main__':
    url = "https://jsonplaceholder.typicode.com/"
    user = requests.get(url + "users/{}".format(sys.argv[1])).json()
    todos = requests.get(url + "todos").json()

    todos_of_user = []
    for todo in todos:
        arr = {}
        if todo.get('userId') == user["id"]:
            arr["USER_ID"] = user["id"]
            arr["USERNAME"] = user['username']
            arr["TASK_COMPLETED_STATUS"] = todo["completed"]
            arr["TASK_TITLE"] = todo["title"]
            todos_of_user.append(arr)

    write_todos_to_csv(todos_of_user)










