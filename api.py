from flask import Flask, jsonify
from flask import request
import redis
import traceback


app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
flaskLists = 'flaskLists'


@app.errorhandler(Exception)
def handle_500(e=None):
    response = jsonify({'erorrs': traceback.format_exc()})
    response.status_code = 500
    return response


@app.route('/show_lists', methods=['GET'])
def get_lists():
    lists = []
    for i in range(0, r.llen(flaskLists)):
        lists.append(r.lindex(flaskLists, i).decode('utf-8'))
    response = jsonify({'lists': lists})
    response.status_code = 200
    return response 


@app.route('/add_new_list', methods=['POST'])
def create_lists():
    data = request.get_json() or {}
    if 'new_items' not in data:
        response = jsonify({'Status': 'Error'})
        response.status_code = 400
        return response
    new_items = data['new_items']
    # сохраняем все данные в один список в бд Redis
    r.rpush(flaskLists, new_items)
    response = jsonify({'Status': 'OK'})
    response.status_code = 201
    return response


if __name__ == '__main__':
    app.run(debug=True)

