from fabric.api import local, run, env, settings

env.hosts = ['it@ssuns.org']

def less():
	local("lessc static/css/mcmun.less -x > static/css/mcmun.css")

def static():
	local("cp -sR /srv/ssuns.org/ssuns_2014/static/ /srv/ssuns.org/static/")

def up():
	local("python manage.py runserver")

