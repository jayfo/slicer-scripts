import configparser
import yaml

if __name__ == '__main__':
    local = configparser.ConfigParser()
    local.read('local.ini')

    with open('tractdbcouch.yml') as f:
        tractdbcouch = yaml.load(f)

    user = tractdbcouch['admin']['user']
    password = tractdbcouch['admin']['password']

    local['admins'] = {}
    local['admins'][user] = password

    with open('localwithsecrets.ini', 'w') as f:
        local.write(f)
