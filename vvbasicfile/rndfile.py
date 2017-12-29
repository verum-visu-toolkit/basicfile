from ujson import dumps as to_minjson
from utils import map_list_to_keys, map_dict_to_indices
from basicfile import BasicFormatReader, BasicFrameMaker, BasicFormatWriter

_RND_COMMAND_KEYS = ['type', 'basicargs', 'args', 'name', 'hide']
_RND_COMMAND_BASIC_ARGS = ['xy', 'lx', 'ly', 'fill']


class RndFormatReader(BasicFormatReader):
    data_location = 'data'

    def unpack_frame(self, packed_frame):
        unpacked_frame = []
        pkd_frame = packed_frame[:]
        for packed_command in pkd_frame:
            # unpack each command (a list) into a dict
            unpacked_command = map_list_to_keys(packed_command, _RND_COMMAND_KEYS)

            if 'basicargs' in unpacked_command:
                # unpack each command's basicargs and args lists into an args dict
                unpacked_basicargs = map_list_to_keys(unpacked_command['basicargs'],
                                                      _RND_COMMAND_BASIC_ARGS)
                if 'args' in unpacked_command:
                    unpacked_command['args'].update(unpacked_basicargs)
                else:
                    unpacked_command['args'] = unpacked_basicargs

                del unpacked_command['basicargs']

            unpacked_frame.append(unpacked_command)
        return unpacked_frame


class RndFrameMaker(BasicFrameMaker):
    # fms is probably a generator for frames
    def __init__(self, fms, make_frame=None, rnd_config=None):
        self.fms_frame_gen = fms
        BasicFrameMaker.__init__(self, fms, make_frame=make_frame, config=rnd_config)

    # overrides FrameMaker._gen; arg 2 is a generator (fms) rather than static data (like spts)
    def _gen(self):
        for frame in self.fms_frame_gen:
            yield self.make_frame(frame)


class RndFormatWriter(BasicFormatWriter):
    def __init__(self, frame_maker, config=None):
        header_data = {
            'config': config,
        }
        BasicFormatWriter.__init__(self, frame_maker, header_data=header_data)

    @staticmethod
    def create_stream_wrapper_parts(header_data):
        """
        Each subclass of BasicFormatWriter must include this function
        """
        config_dict = {
            'config': header_data['config'],
        }
        beginning = to_minjson(config_dict)[:-1] + ',"data":['
        ending = ']}'
        return beginning, ending

    def pack_frame(self, unpacked_frame):
        packed_frame = []

        args_packed_frame = unpacked_frame[:]
        for pkd_cmd in args_packed_frame:
            # map the args dict to a basicargs list and an args dict with the rest of the args
            (pkd_cmd['basicargs'], pkd_cmd['args']) = \
                map_dict_to_indices(pkd_cmd['args'], _RND_COMMAND_BASIC_ARGS, leftovers=True)

            if len(pkd_cmd['args']) is 0:
                pkd_cmd['args'] = None

            # pack the command into a list
            packed_frame.append(map_dict_to_indices(pkd_cmd, _RND_COMMAND_KEYS))

        return packed_frame

        # inherit before_write_frames and after_write_frames from BasicFormatWriter
