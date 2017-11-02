from framework.pipeline.pipeline import Pipeline
from modules.demo import DemoInterceptor, DemoConfig

def main() -> None:
    pipeline = Pipeline()

    # Please add new interceptors
    d = DemoConfig('4')
    interceptor = DemoInterceptor()
    interceptor.config = d

    dispatcher = pipeline.source_dispatcher
    dispatcher.register(interceptor)

    pipeline.execute()


if __name__ == '__main__':
    main()
