import fabric
import fabric.api
import fabric.contrib.files
import os.path
import yaml


def slicer():
    fabric.api.env.hosts = ['slicer@slicer.cs.washington.edu']


def init():
    # Update packages
    fabric.api.sudo('apt-get -q -y update')
    fabric.api.sudo('apt-get -q -y dist-upgrade')

    # Docker images can quickly fill a small disk, ensure they are on our big disk
    if not fabric.contrib.files.exists('dockerlib'):
        fabric.api.sudo('mkdir dockerlib')
    fabric.api.put('defaultdocker', '/etc/default/docker', use_sudo=True)

    # Install Docker
    fabric.api.sudo('curl -sSL https://get.docker.com/ubuntu/ | sh')

    # Install Fig
    fabric.api.sudo('curl -L https://github.com/docker/fig/releases/download/1.0.1/fig-`uname -s`-`uname -m` > /usr/local/bin/fig; chmod +x /usr/local/bin/fig')


def pull():
    # Parse our YAML
    with open('fig/git.yml') as f:
        gityml = yaml.load(f)

    # Pull any services that have a git directory
    for service in gityml:
        if 'git' in gityml[service]:
            # The build directory is where we clone to
            dir_clone = gityml[service]['workdir']
            if fabric.contrib.files.exists(dir_clone):
                # Already exists, just pull it
                fabric.api.run('(cd {} && git pull)'.format(dir_clone))
            else:
                # Need to clone it, put the git directory out of the way
                url_git = gityml[service]['git']
                dir_git = gityml[service]['gitdir']
                fabric.api.run('mkdir -p {}'.format(os.path.dirname(dir_git)))
                fabric.api.run('git clone --separate-git-dir {} {} {}'.format(dir_git, url_git, dir_clone))


def start():
    # # Ensure we have our config data uploaded, starting from a clean slate
    # fabric.api.run('mkdir -p fig/')
    # fabric.api.run('rm -rf fig/*')
    #
    # # The fig
    fabric.api.put('fig/fig.yml', 'fig')
    #
    # # Everything for tractdbcouch
    # fabric.api.run('mkdir -p fig/tractdbcouch')
    # fabric.api.put('fig/tractdbcouch/applyadmin.py', 'fig/tractdbcouch')
    # fabric.api.put('fig/tractdbcouch/Dockerfile', 'fig/tractdbcouch')
    # fabric.api.put('fig/tractdbcouch/local.ini', 'fig/tractdbcouch')
    # fabric.api.put('fig/tractdbcouch/requirements3.txt', 'fig/tractdbcouch')
    # fabric.api.put('fig/tractdbcouch/tractdbcouch.yml', 'fig/tractdbcouch')

    if fabric.contrib.files.exists('~/fig'):
        # Rebuild the fig
        fabric.api.sudo('fig -f ~/fig/fig.yml build')

        # And run it
        fabric.api.sudo('fig -f ~/fig/fig.yml up -d')


def test_jekyll():
    # # The fig
    fabric.api.put('fig/fig.yml', 'fig')
    # # The fig
    fabric.api.put('fig/git.yml', 'fig')

    # fabric.api.run('mkdir -p fig/testjekyll')
    # fabric.api.put('fig/tractdbcouch/applyadmin.py', 'fig/tractdbcouch')
    # fabric.api.put('fig/testjekyll/Dockerfile', 'fig/testjekyll')
    # fabric.api.put('fig/tractdbcouch/local.ini', 'fig/tractdbcouch')
    # fabric.api.put('fig/tractdbcouch/requirements3.txt', 'fig/tractdbcouch')
    # fabric.api.put('fig/tractdbcouch/tractdbcouch.yml', 'fig/tractdbcouch')
    # Rebuild the fig
    fabric.api.sudo('fig -f ~/fig/fig.yml build')
