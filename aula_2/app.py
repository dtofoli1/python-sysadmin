
import sys
import os

import flask


app = flask.Flask(__name__)

@app.route('/')
def index():
	context = {
		'title': 'Python | SysAdmin'
	}
	return flask.render_template('index.html', context = context)

if __name__ == "__main__":

	root_module = os.path.abspath(os.path.curdir)
	sys.path.append(root_module)

	app.run(host='0.0.0.0')