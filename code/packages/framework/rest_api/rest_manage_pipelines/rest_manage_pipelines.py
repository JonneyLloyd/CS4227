from ...pipeline import Pipeline
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
        # pipeline = self.pipeline_manager.create_pipeline(data.name)
        return {'pipeline': data.name,
                'Location': url_for('get_pipeline', name = data.name, _external = True)}, 201


@api.route('/api/v1.0/pipeline/<str:title>')
class PipelineAPI(Resource):
    def get(self, title):
        '''
        Retrieve a pipeline
        '''
        pass

    def put(self, title):
        '''
        Update an existing pipeline
        '''
        pass

    def delete(self, title):
        '''
        Delete an existing pipeline
        '''
        pass

@api.route('/api/v1.0/queue/pipeline/<str:title>')
class PipelineQueue:
    def get(self, title):
        """
        And return the state
        """

    def post(self, title):
        """
        start the pipeline
        pipeline = self.pipeline_manager.create_pipeline(title)
        """
