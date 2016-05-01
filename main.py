"""`main` is the top level module for your Flask application."""

import logger


from flask import Flask

app = Flask(__name__)
app.secret_key = 'VeihrjKFjqxJ78bEc0fJ' # change for production use


@app.route('/')
def root():
    return 'hello world'


#
# Error handlers
#
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500


#
# Special request routers for images
#
@app.route('/<any(css, img, font):folder>/<path:filename>')
def toplevel_static(folder, filename):
    filename = safe_join(folder, filename)
    cache_timeout = app.get_send_file_max_age(filename)

    return send_from_directory(app.static_folder, filename, cache_timeout=cache_timeout)

if __name__ == '__main__':
    app.run(debug=True)
