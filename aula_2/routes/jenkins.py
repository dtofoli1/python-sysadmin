import flask
import jenkins
from services.login_required import login_required

blueprint = flask.Blueprint('jenkins', __name__)

@blueprint.route('/jenkins', methods=[ 'GET', 'POST' ])
@login_required

def get_jenkins():
	
	conn = jenkins.Jenkins('http://localhost:8081', 'admin', 'admin')
	
	jobs = [
		conn.get_job_info(j['fullname']) for j in conn.get_jobs()
	]

	context = {
		'title': 'Python | Sysadmin',
		'jobs': jobs
	}

	return flask.render_template('jenkins.html', context=context)

@blueprint.route('/jenkins/build/<jobname>', methods=[ 'GET' ])
@login_required

def build_jenkins_job(jobname):

	conn = jenkins.Jenkins('http://localhost:8081', 'admin', 'admin')
	
	conn.build_job(jobname)

	return flask.redirect('/jenkins')

@blueprint.route('/jenkins/<jobname>', methods=[ 'GET', 'POST' ])
@login_required

def jenkins_update(jobname):

	conn = jenkins.Jenkins('http://localhost:8081', 'admin', 'admin')

	if flask.request.method == 'POST':
		conn.reconfig_job(jobname, flask.request.form.get('xml').lstrip())

	job = conn.get_job_info(jobname)
	job['xml'] = conn.get_job_config(jobname)

	context = {
		'title': 'Python | Sysadmin',
		'job': job
	}
	
	return flask.render_template('jenkins_update.html', context=context)