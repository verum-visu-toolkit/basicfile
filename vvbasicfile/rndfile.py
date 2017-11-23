from basicfile import BasicFormat
from rnd_schema import rnd_schema, get_blank_rnd


class RndFormat(BasicFormat):
    def __init__(self, data=None):
        BasicFormat.__init__(self, rnd_schema, get_blank_rnd, data=data)

    # Data helper methods

    def add_render_frame(self, commands):
        self.data().append(commands)
