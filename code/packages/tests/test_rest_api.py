from unittest import TestCase
from typing import List, Mapping, Deque, Dict
from flask import g, request, abort, jsonify
import requests
from framework.server.app_factory import AppFactory
from .demo_util import TestConfig
from framework.server import PipelineServer

from framework.rest_api.rest_manage_pipelines import PipelineListAPI

class TestRestAPI(TestCase):

    def setUp(self):
        self.pipeline_rest = PipelineListAPI()
        config = TestConfig()
        app = AppFactory.create_app(config)


    def test_rest_pipeline(self):
        payload = {'name': 'TEST', 'someparam': 'testing'}
        r = requests.post('http://127.0.0.1:5000/api/v1.0/pipeline/', data=payload)

        self.assertEqual(201, r.status_code)
