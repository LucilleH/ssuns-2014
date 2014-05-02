from fabric.api import local, run, env, settings
from fabric.context_managers import lcd


def less():
    local("lessc static/css/mcmun.less -x > static/css/mcmun.css")

def up():
    local("python /srv/ssuns.org/bin/gunicorn -c /srv/ssuns.org/gunicorn_config.py ssuns_2014.wsgi > ./tmp/gunicorn.log 2>&1 & echo $! > ./tmp/gunicorn.pid &")

def dump():
    local("python manage.py dumpdata --indent=4 > backup.json")

def static():
    local("python manage.py collectstatic --noinput")

def restart():
    local('kill -HUP `cat ./tmp/gunicorn.pid`')

def stats():
    local('python manage.py get_registration_stats')

def celery():
    local('python manage.py celeryd --concurrency=1 > ./tmp/celery.log 2>&1 & echo $! > ./tmp/celery.pid &')

def sh():
    local('python manage.py shell')

def awards():
    local('python manage.py generate_awards_slideshow awards.svg')
    local('inkscapeslide updated_awards.svg')

def check():
    local('python manage.py check_assignments')

def badges():
    local('python manage.py get_badge_names')
    local('cp badges.csv badges')

    # Generate additions and deletions since last commit
    with lcd('badges'):
        local('git diff | grep "^-" > deleted.csv')
        local('git diff | grep "^+" > added.csv')
