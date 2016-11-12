from fabric.api import run, env, cd

host = "aws"

if host == "aws":
    CODE_DIR = '/home/ubuntu/redditlinks'
    env.user = 'ubuntu'
    env.hosts = ['reddit-aws']
    env.use_ssh_config = True
    env.forward_agent = True
else:
    CODE_DIR = '/home/django/redditlinks'
    env.user = 'root'
    env.hosts = ['redditcool']
    env.use_ssh_config = True
    env.forward_agent = True


def stop_gunicorn():
    run('service gunicorn stop')


def start_gunicorn():
    run('service gunicorn start')


def install_dependencies():
    run('pip install -r requirements.txt')


def migrate():
    run('python manage.py migrate')


def release():
    with cd(CODE_DIR):
        stop_gunicorn()
        run('git fetch')
        run('git pull -u origin master')
        install_dependencies()
        migrate()
        start_gunicorn()
