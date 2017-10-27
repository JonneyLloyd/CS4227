from .context_object import ContextObject

class Context(ContextObject):


    def set_value(self, value: int) -> None:
        self.value = value

    def get_value(self) -> None:
        print (self.value)

    def consume_service(self) -> None:
        print("consume_service() called")
