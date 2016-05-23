from logger import logger
from flask import Flask, render_template, g, redirect, request
from json import dumps
from datetime import datetime

from graph import generate_graph
from zabbix import get_hosts, get_items, filter_metrics

app = Flask(__name__)
app.secret_key = '9CwkXojJdwUMk0Fn6CfN'


# def public_route(function):
#     function.is_public = True
#     return function


def render(template, title, **kwargs):
    return render_template(template, page_title=title, **kwargs)


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def root():
    return redirect('/graph')


@app.route('/graph', methods=['GET'])
def graph():
    query = request.args.get('q', None)

    start = datetime.now()

    if query is not None:
        logger.debug('QUERY: ' + query)

        chart = generate_graph(query)
    else:
        chart = "{}"
        query = ''

    end = datetime.now()

    logger.debug('Took %ds to process this request' % (end-start).total_seconds())

    return render('graph.html', 'Graph', chart=chart, q=query)


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
        table_data = filter_metrics(host_arg, group_arg, metric_arg)
    else:
        host_arg = group_arg = metric_arg = ''

    return render('explore.html', 'Explore', host=host_arg, group=group_arg, metric=metric_arg, table_data=dumps(table_data))


#
# API endpoints
#
@app.route('/api/hosts')
def api_hosts():
    hosts = get_hosts(attr='host')

    return dumps(hosts)

@app.route('/api/groups')
def api_groups():
    groups = get_hosts(attr='group')

    return dumps(groups)

@app.route('/api/items')
def api_items():
    items = get_items(attr='name')

    return dumps(items)

if __name__ == '__main__':
    app.run(debug=True)

