from fabric.api import local, run, env, settings

env.hosts = ['it@ssuns.org']

def less():
	local("lessc static/css/mcmun.less -x > static/css/mcmun.css")

def deploy():
	less()
	with settings(warn_only=True):
		local("git add mcmun/static/css/mcmun.css")
		local("git commit -m 'Update compiled CSS'")
	local('git push')
	run('cd mcmun.org && git pull origin master')
	run('python mcmun.org/manage.py collectstatic --noinput')
	run('python mcmun.org/manage.py syncdb')
	# Kill the process and start it again
	run('touch ~/mcmun.org/tmp/restart.txt && pkill python')

def up():
	local("python manage.py runserver")

def dump():
	local("python manage.py dumpdata cms --indent=4 > cms/fixtures/initial_data.json")
	local("python manage.py dumpdata committees --indent=4 > committees/fixtures/initial_data.json")

def reset():
    local("rm db.sqlite")
    local("python manage.py syncdb")

def restart():
    local("sudo kill -HUP `cat /srv/ssuns.mcmun.org/gunicorn.pid`")

def nginx():
    local("sudo kill -HUP `cat /var/run/nginx.pid`")

def static():
    local("python manage.py collectstatic --noinput")
