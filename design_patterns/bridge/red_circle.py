from .draw_api import DrawAPI


class RedCircle(DrawAPI):

    def draw_circle(self, radius: int, x: int, y: int) -> None:
        print("Drawing Circle[ color: red, radius: {0}, x: {1}, y: {2}]".format(radius, x, y))
