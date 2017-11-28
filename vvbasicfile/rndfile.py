from basicfile import BasicFormat
from rnd_schema import rnd_structures


class RndFormat(BasicFormat):
    def __init__(self, data=None, packeddata=None):
        BasicFormat.__init__(self, data=data, packeddata=packeddata, format_attrs=rnd_structures)

    # Data helper methods

    def add_render_frame(self, commands):
        self.data.append(commands)
