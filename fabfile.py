import fabric
import fabric.api
import fabric.contrib.files


def slicer():
    fabric.api.env.hosts = ['slicer@slicer.cs.washington.edu']


def init():
    # Update packages
    fabric.api.sudo('apt-get -q -y update')
    fabric.api.sudo('apt-get -q -y dist-upgrade')

    # Ensure some packages we need
    fabric.api.sudo('apt-get install dos2unix')

    # Clean up
    fabric.api.sudo('apt-get clean')

    # Create our backup/scratch directory structure
    if not fabric.contrib.files.exists('backup'):
        fabric.api.run('mkdir backup')
    if not fabric.contrib.files.exists('scratch'):
        fabric.api.run('mkdir scratch')
    if not fabric.contrib.files.exists('scratch/secrets'):
        fabric.api.run('mkdir scratch/secrets')

    # Docker images can quickly fill a small disk, ensure they are on our big disk
    fabric.api.run('mkdir -p scratch/docker')
    # This points docker storage at the given directory
    # Believe it or not, things totally explode if you have a carriage return in the file
    fabric.api.put('init/etc/default/docker', '/etc/default/docker', use_sudo=True)
    fabric.api.sudo('dos2unix /etc/default/docker')

    # Install Docker
    fabric.api.sudo('curl -sSL https://get.docker.com/ubuntu/ | sh')

    # Install Fig
    fabric.api.sudo('curl -L https://github.com/docker/fig/releases/download/1.0.1/fig-`uname -s`-`uname -m` > /usr/local/bin/fig; chmod +x /usr/local/bin/fig')


def purge_config():
    # Clear out any existing config
    fabric.api.run('rm -rf fig')
    fabric.api.run('rm -rf scratch/config')


def purge_secrets():
    # Clear out any existing secrets
    fabric.api.run('rm -rf scratch/secrets')


def push_config():
    # Upload our fig file
    fabric.api.run('mkdir -p fig/')
    fabric.api.put('fig/fig.yml', 'fig')

    # Upload our config files
    fabric.api.run('mkdir -p scratch/config/')
    fabric.api.put('scratch/config', 'scratch')


def push_secrets():
    # Upload our secrets
    fabric.api.run('mkdir -p scratch/secrets/')
    fabric.api.put('scratch/secrets', 'scratch')


def start():
    # Rebuild the fig
    fabric.api.sudo('fig -f ~/fig/fig.yml build')

    # And run it
    fabric.api.sudo('fig -f ~/fig/fig.yml up -d')


def stop():
    # Stop everything
    fabric.api.sudo('fig -f ~/fig/fig.yml stop')
