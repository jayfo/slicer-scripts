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
    fabric.api.run('mkdir -p backup')
    fabric.api.run('mkdir -p scratch')
    fabric.api.run('mkdir -p scratch/secrets')

    # Docker images can quickly fill a small disk, ensure they are on our big disk
    fabric.api.run('mkdir -p scratch/docker')
    # This points docker storage at the given directory
    # Things explode if you have a carriage return in the file, so we dos2unix just in case
    fabric.api.put('init/etc/default/docker', '/etc/default/docker', use_sudo=True)
    fabric.api.sudo('dos2unix /etc/default/docker')

    # Install Docker
    fabric.api.sudo('curl -sSL https://get.docker.com/ | sh')

    # Install Compose
    fabric.api.sudo('curl -L https://github.com/docker/compose/releases/download/1.8.0-rc1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose')
    fabric.api.sudo('chmod +x /usr/local/bin/docker-compose')


def purge_config():
    # Clear out any existing config
    fabric.api.run('rm -rf docker-compose')
    fabric.api.run('rm -rf scratch/config')


def purge_secrets():
    # Clear out any existing secrets
    fabric.api.run('rm -rf scratch/secrets')


def push_config():
    # Upload our compose file
    fabric.api.run('mkdir -p docker-compose/')
    fabric.api.put('docker-compose/docker-compose.yml', 'docker-compose')

    # Upload our config files
    fabric.api.run('mkdir -p scratch/config/')
    fabric.api.put('scratch/config', 'scratch')


def push_data():
    # Upload our data files
    fabric.api.run('mkdir -p scratch/data/')
    fabric.api.put('scratch/data', 'scratch')


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
        fabric.api.sudo('docker-compose -f ~/docker-compose/docker-compose.yml up --force-recreate -d')
    else:
        # Rebuild just this one service
        fabric.api.sudo('docker-compose -f ~/docker-compose/docker-compose.yml build {}'.format(service))
        # And run just this one service
        fabric.api.sudo('docker-compose -f ~/docker-compose/docker-compose.yml up --no-deps --force-recreate -d {}'.format(service))


def stop(service=None):
    if service is None:
        # Stop everything
        fabric.api.sudo('docker-compose -f ~/docker-compose/docker-compose.yml stop')
    else:
        # Stop this service
        fabric.api.sudo('docker-compose -f ~/docker-compose/docker-compose.yml stop {}'.format(service))
