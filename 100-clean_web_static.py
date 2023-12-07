#!/usr/bin/python3
""" this fabric file cleans up old archives in the web servers """
from datetime import datetime
from fabric.api import local, put, run, env, cd, lcd, sudo
import os

env.user = 'ubuntu'
env.hosts = ['35.227.35.75', '100.24.37.33']


def do_pack():
    """
    Targging project directory into a packages as .tgz
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    local('sudo mkdir -p ./versions')
    path = './versions/web_static_{}'.format(now)
    local('sudo tar -czvf {}.tgz web_static'.format(path))
    name = '{}.tgz'.format(path)
    if name:
        return name
    else:
        return None


def do_deploy(archive_path):
    """ this distributes an archive to my web servers """
    if not os.path.exists(archive_path):
        print(f"{archive_path}: does not exist")
        return False
    try:
        arc = archive_path.split("/")
        base = arc[1].strip('.tgz')
        put(archive_path, remote_path='/tmp/')
        sudo(f"mkdir -p /data/web_static/releases/{base}")
        main = f"/data/web_static/releases/{base}"
        sudo(f"tar -xzf /tmp/{arc[1]} -C {main}/")
        sudo(f"rm /tmp/{arc[1]}")
        sudo(f"mv {main}/web_static/* {main}/")
        sudo("rm -rf /data/web_static/current")
        sudo(f"ln -sf {main}/ /data/web_static/current")
        return True
    except Exception:
        return False


def deploy():
    """ this distributes an archive to my web servers """
    archive_path = do_pack()
    if not archive_path:
        return None
    status = do_deploy(archive_path)
    return status


def do_clean(number=0):
    """ this cleans the old archives leaving n amount of items behind"""
    if number in [0, 1]:
        with lcd('./versions/'):
            local("ls -lv | rev | cut -f 1 | rev | \
            head -n +1 | xargs -d '\n' rm -rf")
        with cd('/data/web_static/releases/'):
            run("sudo ls -lv | rev | cut -f 1 | \
            rev | head -n +1 | xargs -d '\n' rm -rf")
    else:
        with lcd('./versions/'):
            local("ls -lv | rev | cut -f 1 | rev |" +
                  f"head -n +{number} | xargs -d '\n' rm -rf")
        with cd('/data/web_static/releases/'):
            run("sudo ls -lv | rev | cut -f 1 |" +
                f"rev | head -n +{number} | xargs -d '\n' rm -rf")
