from datetime import datetime
from json import dumps

from flask import Flask, render_template, redirect, request

from graph import parse_query, generate_graph, generate_table
from logger import logger
from readers.Zabbix import Zabbix

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

    start = datetime.now()

    if query is not None:
        logger.debug('QUERY: ' + query)

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
    host_arg = request.args.get('host', None)
    group_arg = request.args.get('group', None)
    metric_arg = request.args.get('metric', None)

    logger.debug('  HOST: ' + str(host_arg))
    logger.debug(' GROUP: ' + str(group_arg))
    logger.debug('METRIC: ' + str(metric_arg))

    table_data = []

    if host_arg is not None or group_arg is not None or metric_arg is not None:
        table_data = zabbix.filter_metrics(host_arg, group_arg, metric_arg)
    else:
        host_arg = group_arg = metric_arg = ''

    return render('explore.html', 'Explore', host=host_arg, group=group_arg, metric=metric_arg, table_data=dumps(table_data))


#
# API endpoints
#
@app.route('/api/hosts')
def api_hosts():
    hosts = zabbix.get_hosts(attr='host')

    return dumps(hosts)

@app.route('/api/groups')
def api_groups():
    groups = zabbix.get_hosts(attr='group')

    return dumps(groups)

@app.route('/api/items')
def api_items():
    items = zabbix.get_items(attr='name')

    return dumps(items)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

