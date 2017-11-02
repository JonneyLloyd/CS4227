from typing import Any, Optional, Dict


class ConfigMemento():
    """
    Stores a JSON serialization friendly structure representing subclasses of :class:`.ConfigModel`.
    """

    @property
    def config(self) -> Optional[Dict[str, Any]]:
        return self._config or None

    @config.setter
    def config(self, value: Dict[str, Any]) -> None:
        self._config = value
