
import flask

blueprint = flask.Blueprint('docker', __name__)

@blueprint.route('/docker', methods=['GET', 'POST'])
def docker():
	context = {
		'title': 'Python | SysAdmin'
	}
	return flask.render_template('docker.html', context=context)