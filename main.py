from datetime import datetime
from json import dumps

from flask import Flask, render_template, redirect, request

from graph import parse_query, generate_graph, generate_table
from logger import logger
from readers.Zabbix import Zabbix
from explorers.Elasticsearch import Elasticsearch

app = Flask(__name__)
app.secret_key = '9CwkXojJdwUMk0Fn6CfN'

zabbix = None

# def public_route(function):
#     function.is_public = True
#     return function


def render(template, title, **kwargs):
    return render_template(template, page_title=title, **kwargs)


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico', mimetype='image/vnd.microsoft.icon')

def before_first_request():
    zabbix = Zabbix()

@app.route('/')
def root():
    return redirect('/graph')


@app.route('/graph', methods=['GET'])
def graph():
    query = request.args.get('q', None)
    logger.debug('QUERY: ' + query)

    start = datetime.now()

    if query is not None:
        start, end, expressions, data_frame = parse_query(query)

        if expressions[0]._name == 'metric':
            chart = generate_graph(query, start, end, data_frame)
            table = ''
        elif expressions[0]._name == 'log':
            chart = '{}'
            table = generate_table(start, end, data_frame)
        else:
            logger.error("Unknown expression type: %s" % str(type(expressions[0])))
            chart = '{}'
            table = ''
    else:
        chart = "{}"
        table = ''
        query = ''

    end = datetime.now()

    logger.debug('Took %ds to process this request' % (end-start).total_seconds())

    return render('graph.html', 'Graph', chart=chart, table=table, q=query)


@app.route('/explore')
def explore():
    ee = Elasticsearch()

    indexes = ee.get_indexes()

    return render(ee.get_template(), 'Explore', table_data=dumps(indexes))


#
# API endpoints
#
# @app.route('/api/indexes')
# def api_hosts():
#     ee = Elasticsearch()
#
#     indexes = ee.get_indexes()
#
#     return dumps(indexes)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

