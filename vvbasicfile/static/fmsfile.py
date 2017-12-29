from basicfile import BasicFormat
from fms_schema import fms_structures


# unpacked: self.config, self.data, self.props; self.data has full dicts for each frame property
# packed: self._packeddata; self._packeddata has lists for each frame property associating with
# the embedded 'props' list (has embedded: 'config', 'data', 'props')

class FmsFormat(BasicFormat):
    def __init__(self, data=None, packeddata=None):
        # Although these are declared in BasicFormat, included here for type detection... dumb
        self.data = {}
        self.config = {}

        self.props = []
        BasicFormat.__init__(self, data=data, packeddata=packeddata, format_attrs=fms_structures)

    # Data helper methods

    # Returns the reference to the channel in the data
    def channel(self, channel_num):
        return self.data['channel{:d}'.format(channel_num)]

    # Returns the reference to the frame in the data
    def frame(self, frame_num, channel_num=0):
        if frame_num < 0:
            frame_num = 0

        channel = self.channel(channel_num)
        frame = channel[frame_num]
        return frame

    def expand_frames_to_len(self, num_frames, blank_frame=None, channel_num=0):
        if blank_frame is None:
            blank_frame = dict()

        channel = self.channel(channel_num)
        num_frames_to_add = num_frames - len(channel)
        if num_frames_to_add > 0:
            channel += [blank_frame.copy() for _ in range(num_frames_to_add)]

    def add_prop_to_frame(self, frame_num, channel_num=0, propname=None, val=None):
        if propname is None or val is None:
            raise ValueError('propname and val cannot be None')

        if type(propname) is str:
            propkey = propname
        elif type(propname) is list:
            propkey = '_'.join(propname)
        else:
            raise TypeError('propname must be a string or list')

        frame = self.frame(frame_num, channel_num=channel_num)
        frame[propkey] = val

        if propkey not in self.props:
            self.props.append(propkey)

    # Packing/Unpacking

    # Overrides BasicFormat._pack
    def _pack(self):
        self._packeddata = {
            'config': self.config.copy(),
            'data': {},
            'props': self.props[:],
        }

        for channel_key, channel in self.data.items():
            packedchannel = [self._listifyframeprops(propsdict) for propsdict in channel]
            self._packeddata['data'][channel_key] = packedchannel

    def _listifyframeprops(self, propsdict):
        propslist = [None] * len(self.props)
        for propkey, val in propsdict.items():
            propindex = self.props.index(propkey)
            propslist[propindex] = val
        return propslist

    # Overrides BasicFormat._unpack
    # called in BasicFormat.__init__ when it receives packeddata option
    def _unpack(self):
        self.config = self._packeddata['config'].copy()
        self.data = {}
        self.props = self._packeddata['props'][:]

        for channel_key, channel in self._packeddata['data'].items():
            unpackedchannel = [self._dictifyframeprops(propslist) for propslist in channel]
            self.data[channel_key] = unpackedchannel

    def _dictifyframeprops(self, propslist):
        propsdict = dict()
        for propindex, val in enumerate(propslist):
            propkey = self.props[propindex]
            propsdict[propkey] = val
        return propsdict
