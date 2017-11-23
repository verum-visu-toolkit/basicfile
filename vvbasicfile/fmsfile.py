from basicfile import BasicFormat
from fms_schema import fms_schema, get_blank_fms


class FmsFormat(BasicFormat):
    def __init__(self, data=None):
        BasicFormat.__init__(self, fms_schema, get_blank_fms, data=data)

    # Data helper methods

    # Not 'get_channel' and 'get_frame' since they return the references,
    # not just the values, so that manipulating the data does not need
    # separate methods

    def channel(self, channel_num):
        return self.data()['channel{:d}'.format(channel_num)]

    def add_frame(self, frame, channel_num=0):
        channel = self.channel(channel_num)
        channel.append(frame)

    def update_num_frames(self, num_frames, default_val=None, channel_num=0):
        channel = self.channel(channel_num)
        num_frames_to_add = num_frames - len(channel)

        for _ in range(num_frames_to_add):
            channel.append(default_val.copy())

    def frame(self, frame_num, channel_num=0):
        channel = self.channel(channel_num)
        frame = channel[frame_num]
        return frame

