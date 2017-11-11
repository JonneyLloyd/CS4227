from ..config import ConfigMapper
from flask import g, request, abort, jsonify, get_flashed_messages
from flask_restful import Resource
from extension import api
class RestManageConfig:
    ...

@api.route('/api/v1.0/pipeline/<str:title>/config_model/')
class ConfigListAPI(Resource):
    def get(self):
        '''
        Retrieve a config from pipeline
        When getting the list, need to get position(index)
        '''
        pass

    def post(self):
        '''
        Create new config on pipeline
        User needs to supply the index & document name
        '''
        pass

@api.route('/api/v1.0/pipeline/<str:title>/config_model/<int:index>')
class ConfigAPI(Resource):
    def get(self, index):
        '''
        Retrieve a config from pipeline
        module also passed in
        '''
        pass

    def put(self, index):
        '''
        Update an existing config from pipeline
        '''
        pass

    def delete(self, index):
        '''
        Delete an existing config from pipeline
        '''
        pass
