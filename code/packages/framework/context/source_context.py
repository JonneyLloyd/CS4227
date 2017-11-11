class SourceContext:

    def __init__(self, pipeline: 'PipelineBase') -> None:
        self._pipeline = pipeline
        self._state = {}

    def set_state(self, state: dict):
        self._state = state

    def get_state(self) -> dict:
        return self._state

