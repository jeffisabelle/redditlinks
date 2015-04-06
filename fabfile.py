from fabric.api import run, env, cd


CODE_DIR = '/home/django/redditlinks'
env.user = 'root'
env.hosts = ['redditcool']
env.use_ssh_config = True
env.forward_agent = True


def stop_gunicorn():
    run('service gunicorn stop')


def start_gunicorn():
    run('service gunicorn start')


def release():
    with cd(CODE_DIR):
        stop_gunicorn()
        run('git fetch')
        run('git pull -u origin master')
        start_gunicorn()
