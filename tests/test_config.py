import os
import sys
import unittest
from flask import current_app
from flask_testing import TestCase

# Add project dir to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import api


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        os.environ['FLASK_APP'] = 'api'
        os.environ['FLASK_ENV'] = 'development'
        return api.create_app(self)

    def test_app_development_config(self):
        self.assertTrue(self.app.config['DEBUG'] == True)


# class TestTestingConfig(TestCase):
#     def test_app_testing_config(self):
#         self.assertTrue(app.config['DEBUG'] == True)


# class TestDevelopmentConfig(TestCase):
#     def test_app_production_config(self):
#         self.assertTrue(app.config['DEBUG'] == True)


if __name__ == "__main__":
    unittest.main()
