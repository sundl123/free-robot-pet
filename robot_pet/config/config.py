import yaml

with open('conf/config.yaml', 'r') as file:
    config = yaml.safe_load(file)
print(f'config is {config}')


def get_config():
    return config
