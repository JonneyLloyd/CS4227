import types
from flask import g, request, abort, jsonify
from flask import current_app as app
from framework.server.extensions import api

def ApiRoute(self, *args, **kwargs):
    '''
    Class decorator for adding resources
    '''
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper

api.route = types.MethodType(ApiRoute, api)
