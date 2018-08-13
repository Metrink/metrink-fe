import yaml

from logger import logger
from os.path import abspath

class Configuration(object):
    """
    Reads the configuration file and allows access to properties
    """
    def __init__(self, file='./configuration.yml'):
        with open(file, 'r') as ymlfile:
            self.config = yaml.load(ymlfile)

    def get(self, property):
        """
        Given a dot separated list of properties, fetch it from the config
        :param property: the property to fetch
        :return: the config, or None if not found
        """
        cur = self.config

        for prop in property.split('.'):
            if prop not in cur:
                logger.warning("Config property %s not found" % property)
                return None

            cur = cur[prop]

        return cur