from ..config import ConfigMapper
from ..api.manage_configs import ManageConfigs

from flask import g, request, abort, jsonify, get_flashed_messages
from flask_restful import Resource
from extension import api

class RestManageConfig:
    ...

@api.route('/api/v1.0/pipeline/<str:title>/config_model/')
class ConfigListAPI(Resource):
    def get(self, title):
        return {ManageConfigs.get_all_configs(title)}, 201

    def post(self):
        #Create new config on pipeline
        data = request.get_json()
        ManageConfigs.create_config_model(data.name)
        return {'Location': api.url_for (ConfigAPI, title=data.name)}, 201

@api.route('/api/v1.0/pipeline/<str:title>/config_model/<int:index>')
class ConfigAPI(Resource):
    def get(self, title, index):
        config = ManageConfigs.get_config(title, index)
        return {'Location': api.url_for (ConfigAPI, title=index)}, 201

    def put(self, title, index):
        '''
        Update an existing config from pipeline
        '''
        pass

    def delete(self, title, index):
        ManageConfigs.delete_config(title, index)
        return 201
