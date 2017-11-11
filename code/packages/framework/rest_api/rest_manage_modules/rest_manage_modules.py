from ..config import ConfigMapper
from flask import g, request, abort, jsonify, get_flashed_messages
from flask_restful import Resource
from extension import api

class RestManageModules:
    ...

@api.route('/api/v1.0/module')
class ModuleListAPI(Resource):
    def get(self):
        '''
        Retrieve a config from pipeline

        '''
        pass

@api.route('/api/v1.0/module/<str:name>')
class ModuleAPI(Resource):
    def get(self, name):
        '''
        Small change needed here
        '''
        pass
