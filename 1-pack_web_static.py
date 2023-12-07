#!/usr/bin/python3
#  this is a fabfile that generates a .tgz archive from
# the contents of web_static folder
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """ this function creates a tar gzipped archive"""
    dt = datetime.utcnow()
    file = f"versions/web_static_{dt.year}"
    f"{dt.month}{dt.day}{dt.hour}{dt.minute}{dt.second}.tgz"
    if not os.path.isdir("versions"):
        if local("mkdir -p versions").failed:
            return None
    if local(f"tar -cvzf {file} web_static").failed:
        return None
    return file
