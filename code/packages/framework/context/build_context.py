from ..pipeline import PipelineBase


class BuildContext:

    def __init__(self, pipeline: PipelineBase) -> None:
        self._pipeline = pipeline
