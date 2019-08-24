"""
Fabric 100-clean_web_static.py file to web servers
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir
env.hosts = ['104.196.127.61', '35.229.87.105']

@runs_once
def clean_local(number=0):
    """
    remove local versions step clean_server
    number: files to keep
    """
    # change directory and list files
    os.chdir("versions/")
    res = local("ls -1t", capture=True).split("\n")
    if number == 0:
        number += 1
    if len(res) > number:
        for f in res[number:]:
            local("rm -f {}".format(f))


def clean_server(number=0):
    """
    remove versions step clean_server
    number: files to keep
    """
    path = "/data/web_static/releases"
    with cd(path):
        res = sudo("ls -1t").split("\r\n")
    res = [f for f in res if "web_static" in f]
    if number == 0:
        number += 1
    if len(res) > number:
        res = res[number:]
        with cd(path):
            for f in res:
                sudo("rm -rf {}".format(f))


def do_clean(number=0):
    """
    remove old version step do_clean
    number: files to keep
    """
    number = int(number)
    clean_local(number)
    clean_server(number)
