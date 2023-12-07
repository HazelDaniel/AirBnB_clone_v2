#!/usr/bin/python3
"""this deploys a static file using fabric"""
from fabric.api import *
import os.path

env.user = 'ubuntu'
env.hosts = ["54.197.123.187", "18.210.17.238"]
env.key_filename = "~/Documents/ALX/credentials/alx_ubuntu_server"


def do_deploy(archive_path):
    """ this distributes an archive to my web servers """
    if not os.path.exists(archive_path):
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
