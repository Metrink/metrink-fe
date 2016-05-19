from logger import logger
from flask import Flask, render_template, g, redirect, request
from json import dumps

from graph import generate_graph
from zabbix import get_hosts

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

    if query is not None:
        logger.debug('QUERY: ' + query)

        chart = generate_graph(query)
    else:
        chart = "{}"

    return render('graph.html', 'Graph', chart=chart, q=query)

@app.route('/explore')
def explore():

    return render('explore.html', 'Explore')


#
# API endpoints
#
@app.route('/api/hosts')
def api_hosts():
    hosts = get_hosts(attr='host')

    return dumps(hosts)

if __name__ == '__main__':
    app.run(debug=True)

