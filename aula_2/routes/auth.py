
import flask


blueprint = flask.Blueprint('auth', __name__)

@blueprint.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
	context = {
		'title': 'Python | SysAdmin'
	}

	if flask.request.method == 'POST':
		form = flask.request.form
		print(form)
	return flask.render_template('sign-in.html', context=context)