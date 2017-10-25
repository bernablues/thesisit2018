import yaml


with open("station_config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

print cfg