import flask

app = flask.Flask('app')

import testing.dot.routes
import testing.iwaroz.api

import webapp.static
import webapp.api
import webapp.routes
import webapp.devtools
import webapp.errors

app.run(debug=True, host='0.0.0.0', port=8080)