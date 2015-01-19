import fabric
import fabric.api


def slicer():
    fabric.api.env.hosts = ['slicer@slicer.cs.washington.edu']


def init():
    # Update packages
    fabric.api.sudo('apt-get -q -y update')
    fabric.api.sudo('apt-get -q -y dist-upgrade')

    # Install Docker
    fabric.api.sudo('curl -sSL https://get.docker.com/ubuntu/ | sh')

    # Install Fig
    fabric.api.sudo('curl -L https://github.com/docker/fig/releases/download/1.0.1/fig-`uname -s`-`uname -m` > /usr/local/bin/fig; chmod +x /usr/local/bin/fig')


def start():
    # Ensure we have our config data uploaded, starting from a clean slate
    fabric.api.run('mkdir -p fig/')
    fabric.api.run('rm -rf fig/*')

    # The fig
    fabric.api.put('fig/fig.yml', 'fig')

    # Everything for tractdbcouch
    fabric.api.run('mkdir -p fig/tractdbcouch')
    fabric.api.put('fig/tractdbcouch/applyadmin.py', 'fig/tractdbcouch')
    fabric.api.put('fig/tractdbcouch/Dockerfile', 'fig/tractdbcouch')
    fabric.api.put('fig/tractdbcouch/local.ini', 'fig/tractdbcouch')
    fabric.api.put('fig/tractdbcouch/requirements3.txt', 'fig/tractdbcouch')
    fabric.api.put('fig/tractdbcouch/tractdbcouch.yml', 'fig/tractdbcouch')

    # Rebuild the fig
    fabric.api.sudo('fig -f ~/fig/fig.yml build')

    # And run it
    fabric.api.sudo('fig -f ~/fig/fig.yml up -d')
