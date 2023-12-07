#!/usr/bin/python3
"""this creates and distributes the archive across servers"""
from datetime import datetime
from fabric.api import *
import os.path

env.user = 'ubuntu'
env.hosts = ["54.197.123.187", "18.210.17.238"]
env.key_filename = "~/Documents/ALX/credentials/alx_ubuntu_server"


def deploy():
    """ this distributes an archive to my web servers """
    archive_path = do_pack()
    if not archive_path:
        return None
    status = do_deploy(archive_path)
    return status


def do_deploy(archive_path):
    """ this distributes an archive to my web servers """
    if not os.path.exists(archive_path):
        print(f"{archive_path}: does not exist")
        return False
    try:
        arc = archive_path.split("/")
        base = arc[1].strip('.tgz')
        put(archive_path, remote_path='/tmp/')
        print("we got here")
        print(f"mkdir -p /data/web_static/releases/{base}")
        sudo(f"mkdir -p /data/web_static/releases/{base}")
        main = f"/data/web_static/releases/{base}"
        print(f"tar -xzf /tmp/{arc[1]} -C {main}/")
        sudo(f"tar -xzf /tmp/{arc[1]} -C {main}/")
        sudo(f"rm /tmp/{arc[1]}")
        sudo(f"mv {main}/web_static/* {main}/")
        sudo("rm -rf /data/web_static/current")
        sudo(f"ln -sf {main}/ /data/web_static/current")
        return True
    except Exception:
        return False


def do_pack():
    """ this function creates a tar gzipped archive"""
    dt = datetime.utcnow()
    file = f"versions/web_static_{dt.year}" + \
        f"{dt.month}{dt.day}{dt.hour}{dt.minute}{dt.second}.tgz"
    if not os.path.isdir("versions"):
        if local("mkdir -p versions").failed:
            return None
    if local(f"tar -cvzf {file} web_static").failed:
        return None
    return file
