from flask import Flask
from flask import request, jsonify
import json
from werkzeug.routing import BaseConverter
from basedao import Basedao


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
def usual_query_method(query_url):
    (flag, params) = check_json_format(request.data)

    urls = query_url.split('/')
    url_len = len(urls)
    ps = {}
    if url_len > 0:
        table = urls[0]
    if url_len == 1 and (request.method == 'POST' or request.method == 'GET'):
        pass
    elif url_len == 2:
        ps['id'] = urls[1]
    elif url_len > 2 and (request.method == 'GET' or request.method == 'DELETE') and url_len % 2 == 1:
        for i, al in enumerate(urls):
            if i == 0:
                continue
            if i % 2 == 1:
                tmp = al
            else:
                ps[tmp] = al
    else:
        return "The params is wrong."

    if (request.method == 'POST' or request.method == 'PUT') and ps.get('id'):
        params = dict(params, **{'id': ps.get('id')})
    if request.method == 'GET' or request.method == 'DELETE':
        params = ps

    rs = Basedao(table).retrieve(params, [], {})
    return jsonify(rs)
