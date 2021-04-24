from webapp.init import app

import flask

@app.errorhandler(404)
def page_not_found(e):
  return flask.render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
  return flask.render_template('errors/500.html'), 500