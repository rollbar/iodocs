import getpass
import os
import sys

from fabric.api import run, local, cd, env, roles, execute
import requests

CODE_DIR = '/home/deploy/www/iodocs'

env.roledefs = {
    'web': ['web4', 'web8'],
}


def deploy():
    # pre-roll checks
    check_user()

    # do a local git pull, so the revision # when we record the deploy is correct
    local("git pull")

    # do the roll.
    # execute() will call the passed-in function, honoring host/role decorators.
    execute(update_and_restart)


@roles('web')
def update_and_restart():
    with cd(CODE_DIR):
        run("git pull")
        run("npm install")
        run("supervisorctl restart iodocs")


def check_user():
    if getpass.getuser() != 'deploy':
        print "This command should be run as deploy. Run like: sudo -u deploy fab deploy"
        sys.exit(1)
