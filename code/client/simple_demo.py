from framework.pipeline.pipeline import Pipeline
from modules.demo import DemoInterceptor

pipeline = Pipeline()
interceptor = DemoInterceptor()

dispatcher = pipeline.source_dispatcher
dispatcher.register(interceptor)

pipeline.execute()
