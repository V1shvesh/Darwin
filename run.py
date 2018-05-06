from flask import request, url_for, jsonify
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)


tasks = {
    "firsttask": {
        "category": "social",
        "effort": 1,
        "duration": 10,
        "importance": 1
    },
    "secondtask": {
        "category": "social",
        "effort": 12,
        "duration": 11,
        "importance": 21
    },
    "thirdtask": {
        "category": "health",
        "effort": 12,
        "duration": 11,
        "importance": 21
    }
}

def task_repr(key):
    return jsonify(tasks[key])


@app.route("/", methods=['GET', 'POST'])
def tasks_list():
    """
    List or create tasks.
    """
    if request.method == 'POST':
        newtask = request.get_json(force=True)
        newkey = newtask['task_name']
        del newtask['task_name']
        tasks[newkey] = newtask
        return task_repr(newkey), status.HTTP_201_CREATED

    # request.method == 'GET'
    return jsonify(tasks)


@app.route("/<string:key>", methods=['GET', 'DELETE'])
def tasks_detail(key):
    """
    Retrieve, update or delete note instances.
    """
    if request.method == 'DELETE':
        tasks.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    if key not in tasks:
        raise exceptions.NotFound()
    return task_repr(key)


@app.route("/piechart", methods = ['GET'])
def send_weights():
    social = prod = health = 0
    for value in tasks.values():
        if value['category'] == 'social':
            social += 1
        elif value['category'] == 'productivity':
            prod += 1
        else:
            health += 1
    ans = {'social': social, 'health': health, 'productivity': prod}
    return jsonify(ans)


if __name__ == "__main__":
    app.run(debug=True)
