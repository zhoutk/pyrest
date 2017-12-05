from flask import Flask
from flask import request, jsonify
import json
from werkzeug.routing import BaseConverter


def check_json_format(raw_msg):
    try:
        js = json.loads(raw_msg, encoding='utf-8')
    except ValueError:
        return False, {}
    return True, js


class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter


@app.route('/rs/<regex(".*"):query_url>', methods=['PUT', 'DELETE', 'POST', 'GET'])
def rs(query_url):
    (flag, params) = check_json_format(request.data)

    urls = query_url.split('/')
    url_len = len(urls)
    if url_len < 1 or url_len > 2 and url_len % 2 == 1:
        return "The params is wrong."

    ps = {}
    for i, al in enumerate(urls):
        if i == 0:
            table = al
        elif i == 1:
            idd = al
        elif i > 1 and i % 2 == 0:
            tmp = al
        else:
            ps[tmp] = al

    ps['table'] = table
    if url_len > 1:
        ps['id'] = idd
    if request.method == 'POST' or request.method == 'PUT':
        params = dict(params, **{'table': ps.get('table'), 'id': ps.get('id')})
    if request.method == 'GET' or request.method == 'DELETE':
        params = ps
    return jsonify(params)
