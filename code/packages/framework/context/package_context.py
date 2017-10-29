from ..pipeline import PipelineBase


class PackageContext:

    def __init__(self, pipeline: PipelineBase) -> None:
        self._pipeline = pipeline
