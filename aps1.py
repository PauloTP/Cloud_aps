

"""Alternative version of the ToDo RESTful server implemented using the
Flask-RESTful extension."""

from flask import Flask, jsonify, abort, make_response,request
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
import boto3
import random

app = Flask(__name__,)
api = Api(app)

global current_ip
current_ip = ""

tasks = [
    {
        'id': 1,
        'title': random.randint(1,101),
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': random.randint(1,101),
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')
}

class TaskListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
        super(TaskListAPI, self).__init__()

    def get(self):
        return {'tasks': [marshal(task, task_fields) for task in tasks]}

    def post(self):
        args = self.reqparse.parse_args()
        task = {
            'id': tasks[-1]['id'] + 1,
            'title': args['title'],
            'description': args['description'],
            'done': False
        }
        tasks.append(task)
        return {'task': marshal(task, task_fields)}, 201


class TaskAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        return {'task': marshal(task[0], task_fields)}

    def put(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                task[k] = v
        return {'task': marshal(task, task_fields)}

    def delete(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        tasks.remove(task[0])
        return {'result': True}

class Check(Resource):

    def __init__(self):
        super(Check, self).__init__()

    def get(self):
        return 200


api.add_resource(TaskListAPI, '/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/tasks/<int:id>', endpoint='task')
api.add_resource(Check, '/healthcheck', endpoint='healthcheck')


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port = 5000)