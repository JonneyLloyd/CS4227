from ...pipeline import Pipeline
from ...api.manage_pipelines import ManagePipelines
from flask import g, request, abort, jsonify
from flask_restful import Resource

from framework.server.extensions import api



class ManagePipelines(object):
    ...

@api.route('/api/v1.0/pipeline/')
class PipelineListAPI(Resource):
    def get(self):
        '''
        Retrieve a pipeline
        Needs to return how to start it.
        '''
        pass

    def post(self):
        #Create new pipeline
        data = request.get_json()
        pipeline = ManagePipeLines.create_pipeline(data.name)
        return {'Location': api.url_for (PipelineAPI, title=data.name)}, 201


@api.route('/api/v1.0/pipeline/<str:title>')
class PipelineAPI(Resource):
    def get(self, title):
        pipeline = ManagePipeLines.get_pipeline(title)
        return {'Location': api.url_for(PipelineAPI, title= title)}, 201

    def put(self, title):
        '''
        Update an existing pipeline
        '''
        pass

    def delete(self, title):
        ManagePipeLines.delete_pipeline(title)
        return 201

@api.route('/api/v1.0/queue/pipeline/<str:title>')
class PipelineQueue:
    def get(self, title):
        """
        And return the state
        """

    def post(self, title):
        ManagePipeLines.execute_pipeline(title)
        return 201
