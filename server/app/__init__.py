import yaml

from flask import Flask

app = Flask("covers-server")

# Initialized in run.py 
config = None

from server.app import routes

class Сonfig():
    def __init__(self, cfg_path):
        with open(cfg_path, "r") as config_fd:
            yaml_cfg = yaml.load(config_fd)
        self.segmentation_addr = yaml_cfg["segmentation"]
