from framework.server import PipelineServer

from config import DevConfig
from modules.demo import DemoConfig, DemoInterceptor


def main() -> None:
    server = PipelineServer(DevConfig)
    server.register_module(DemoConfig, DemoInterceptor)
    server.start()

if __name__ == "__main__":
    main()
