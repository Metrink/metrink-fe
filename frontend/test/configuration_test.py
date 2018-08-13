import unittest

from configuration import Configuration

class MetrinkParserTest(unittest.TestCase):
    def test_get(self):
        config = Configuration('../configuration.yml')

        print(config.get('redis.host'))
