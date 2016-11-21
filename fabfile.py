import getpass
import os
import sys
import consulate

from fabric.api import run, local, cd, env, roles, execute
import requests

CODE_DIR = '/home/deploy/www/iodocs'

env.forward_agent = True

consul = consulate.Session()

def group_map():

    ansible_group_list = consul.kv.find('ansible/groups')

    ansible_group_map = {}

    for path, groups in ansible_group_list.iteritems():
        host = os.path.basename(path)
        for group in groups.split(','):
            if group in ansible_group_map:
                ansible_group_map[group].append(host)
            else:
                ansible_group_map[group] = [host]

    return ansible_group_map

env.roledefs = group_map()


def deploy():
    # pre-roll checks
    check_user()

    # do a local git pull, so the revision # when we record the deploy is correct
    local("git pull")

    # do the roll.
    # execute() will call the passed-in function, honoring host/role decorators.
    execute(update_and_restart)


@roles('apps-web')
def update_and_restart():
    with cd(CODE_DIR):
        run("git pull")
        run("npm install")
        run("supervisorctl restart iodocs")


def check_user():
    if getpass.getuser() != 'deploy':
        print "This command should be run as deploy. Run like: sudo -u deploy fab deploy"
        sys.exit(1)
