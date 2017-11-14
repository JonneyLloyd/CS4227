from unittest import TestCase
from typing import List, Mapping, Deque, Dict
from flask import g, request, abort, jsonify, Flask
import requests
from framework.server.app_factory import AppFactory
from .demo_util import TestConfig
from framework.server import PipelineServer

from framework.rest_api.rest_manage_pipelines import PipelineListAPI, PipelineAPI

class TestRestAPI(TestCase):

    def setUp(self):

        self.pipeline_rest_list = PipelineListAPI()
        self.pipeline_rest = PipelineAPI()


    def test_rest_pipeline_post(self):
        payload = {'name': 'TEST', 'someparam': 'testing'}
        r = requests.post('http://localhost:5000/api/v1.0/pipeline/', data=payload)
        #self.assertEqual(201, r.status_code)

    def test_rest_pipeline_get(self):
        r = requests.get('http://localhost:5000/api/v1.0/pipeline/test')
        #self.assertEqual(201, r.status_code)
