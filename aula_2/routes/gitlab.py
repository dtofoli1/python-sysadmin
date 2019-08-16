#DSywR2EWMKACytNPED5T

import flask
import requests
from services.login_required import login_required

blueprint = flask.Blueprint('gitlab', __name__)

@blueprint.route('/gitlab', methods=['GET', 'POST'])
@login_required

def gitlab():
	
	users = requests.get('http://localhost:8000/api/v4/users', headers = { 'Private-Token': 'tvivjqsWcJbsezuRzozU' })
	projects = requests.get('http://localhost:8000/api/v4/projects', headers = { 'Private-Token': 'tvivjqsWcJbsezuRzozU' })

	context = {
		'title': 'Python | SysAdmin',
		'users': users.json() if users.status_code == 200 else [],
		'projects': projects.json() if projects.status_code == 200 else []
	}
	return flask.render_template('gitlab.html', context=context)

@blueprint.route('/gitlab/<projectid>', methods=[ 'GET', 'POST'])
@login_required

def gitlab_commit(projectid):

	URL = 'http://localhost:8000/api/v4/projects/{}/repository/commits/'.format(projectid)
	commits = requests.get(URL, headers={'Private-Token': 'tvivjqsWcJbsezuRzozU' })

	context = {
		'title': 'Python | Sysadmin',
		'commits': commits.json() if commits.status_code == 200 else []
	}

	return flask.render_template('gitlab_commits.html', context=context)