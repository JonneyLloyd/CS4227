from .draw_api import DrawAPI


class GreenCircle(DrawAPI):

    def draw_circle(self, radius: int, x: int, y: int) -> None:
        print("Drawing Circle[ color: green, radius: {0}, x: {1}, y: {2}]".format(radius, x, y))
