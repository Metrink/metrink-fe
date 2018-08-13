import os

from datetime import datetime
from flask import Flask, render_template, redirect, request

from logger import logger
from configuration import Configuration
from graph import parse_query, generate_graph, generate_table
from explorers.ElasticsearchExplorer import ElasticsearchExplorer
from explorers.MetricsExplorer import MetricsExplorer

app = Flask(__name__)
app.secret_key = '9CwkXojJdwUMk0Fn6CfN'

config = Configuration(os.path.join(app.root_path, 'configuration.yml'))


# def public_route(function):
#     function.is_public = True
#     return function


def render(template, title, **kwargs):
    return render_template(template, page_title=title, **kwargs)


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico', mimetype='image/vnd.microsoft.icon')

# def before_first_request():

@app.route('/')
def root():
    return redirect('/graph')


@app.route('/graph', methods=['GET'])
def graph():
    query = request.args.get('q', None)
    _render = request.args.get('render', 'True')
    _render = False if _render == 'False' else True

    logger.debug('QUERY: ' + query)

    start_timer = datetime.now()

    if query is not None and _render:
        start, end, expressions, data_frame = parse_query(query)

        if expressions[0].name == 'metric':
            chart = generate_graph(query, start, end, data_frame)
            table = ''
        elif expressions[0].name == 'log':
            chart = '{}'
            table = generate_table(start, end, data_frame)
        else:
            logger.error("Unknown expression type: %s" % str(type(expressions[0])))
            chart = '{}'
            table = ''
    else:
        chart = "{}"
        table = ''
        # query = ''

    end_timer = datetime.now()

    logger.debug('Took %0.02fs to process this request' % (end_timer-start_timer).total_seconds())

    return render('graph.html', 'Graph', chart=chart, table=table, q=query)


@app.route('/explore')
def explore():
    type = request.args.get('type', 'metrics')

    start_timer = datetime.now()

    if type == 'logs':
        explorer = ElasticsearchExplorer()
    else:
        explorer = MetricsExplorer(config)

    table_data = explorer.get_table_data()

    end_timer = datetime.now()
    logger.debug('Took %0.02fs to process this request' % (end_timer-start_timer).total_seconds())

    return render(explorer.get_template(), 'Explore', table_data=table_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

