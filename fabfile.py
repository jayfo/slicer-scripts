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
    # Things explode if you have a carriage return in the file, so we dos2unix just in case
    fabric.api.put('init/etc/default/docker', '/etc/default/docker', use_sudo=True)
    fabric.api.sudo('dos2unix /etc/default/docker')

    # Install Docker
    fabric.api.sudo('curl -sSL https://get.docker.com/ | sh')

    # Install Compose
    fabric.api.sudo('curl -L https://github.com/docker/compose/releases/download/1.5.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose')
    fabric.api.sudo('chmod +x /usr/local/bin/docker-compose')


def purge_config():
    # Clear out any existing config
    fabric.api.run('rm -rf docker-compose')
    fabric.api.run('rm -rf scratch/config')


def purge_secrets():
    # Clear out any existing secrets
    fabric.api.run('rm -rf scratch/secrets')


def purge_repository(name):
    # Remove a directory we have previously pulled
    #
    # e.g. fab slicer purge_repository:pyramidwork

    fabric.api.run('rm -rf docker-compose/{name}'.format(name=name))


def pull_repository(name, git, branch='master'):
    # Pull a repository, generally because we want to use it for development testing
    #
    # e.g. fab slicer pull_repository:pyramidwork,https://github.com/jayfo/docker-tractdb-pyramid.git,useractions

    # We'll always clone from scratch, to be safe
    fabric.api.run('rm -rf docker-compose/{name}'.format(name=name))

    fabric.api.run('git clone {git} docker-compose/{name}'.format(name=name, git=git))
    fabric.api.run('cd docker-compose/{name} && git checkout {branch}'.format(name=name, branch=branch))


def push_config():
    # Upload our compose file
    fabric.api.run('mkdir -p docker-compose/')
    fabric.api.put('docker-compose/docker-compose.yml', 'docker-compose')

    # Upload our config files
    fabric.api.run('mkdir -p scratch/config/')
    fabric.api.put('scratch/config', 'scratch')


def push_secrets():
    # Upload our secrets
    fabric.api.run('mkdir -p scratch/secrets/')
    fabric.api.put('scratch/secrets', 'scratch')


def start(service=None):
    # Start a service, restarting if necessary.
    #
    # e.g. fab slicer start
    # e.g. fab slicer start:tractdbpyramid

    if service is None:
        # Rebuild everything
        fabric.api.sudo('docker-compose -f ~/docker-compose/docker-compose.yml build')
        # And run everything
        fabric.api.sudo('docker-compose -f ~/docker-compose/docker-compose.yml up -d')
    else:
        # Rebuild just this one service
        fabric.api.sudo('docker-compose -f ~/docker-compose/docker-compose.yml build {}'.format(service))
        # And run just this one service
        fabric.api.sudo('docker-compose -f ~/docker-compose/docker-compose.yml up -d --no-deps {}'.format(service))


def stop(service=None):
    if service is None:
        # Stop everything
        fabric.api.sudo('docker-compose -f ~/docker-compose/docker-compose.yml stop')
    else:
        # Stop this service
        fabric.api.sudo('docker-compose -f ~/docker-compose/docker-compose.yml stop {}'.format(service))
