from ujson import dumps as to_minjson
from utils import load_basicfile_field, map_list_to_keys, map_dict_to_indices
from basicfile import BasicFormatReader, BasicFrameMaker, BasicFormatWriter


class FmsFormatReader(BasicFormatReader):
    data_location = 'data.channel0'
    # to support mult channels, have data_location change after __next__ reaches the end of frames

    def __init__(self, fms_readpath):
        BasicFormatReader.__init__(self, fms_readpath)
        self.props = None

    def onenter(self):
        self.props = [str(propname) for propname in load_basicfile_field(self.readpath, 'props')]

    def unpack_frame(self, packed_frame):
        return map_list_to_keys(packed_frame, self.props)


class FmsFrameMaker(BasicFrameMaker):
    def __init__(self, spts, make_frame=None, fms_config=None):

        def make_frame__wrapper(sample_num, data):
            spectra_for_sample = self.get_spectra_for_sample_pos(data, sample_num)
            return make_frame(spectra_for_sample)

        BasicFrameMaker.__init__(self, spts, make_frame=make_frame__wrapper, config=fms_config)

    @staticmethod
    def get_spectra_for_sample_pos(spts, sample_num):
        spectra_for_frame = {
            filename: spt['data']['channel0'][sample_num]
            for filename, spt in spts.items()
            if spt['config']['num_spectra'] > sample_num
        }
        return spectra_for_frame


class FmsFormatWriter(BasicFormatWriter):
    def __init__(self, frame_maker, config=None, props=None):
        header_data = {
            'config': config,
            'props': props,
        }
        BasicFormatWriter.__init__(self, frame_maker, header_data=header_data)

    @staticmethod
    def create_stream_wrapper_parts(header_data):
        """
        Each subclass of BasicFormatWriter must include this function
        """
        config_dict = {
            'config': header_data['config'],
            'props': header_data['props'],
        }
        beginning = to_minjson(config_dict)[:-1] + ',"data":{'
        ending = '}}'
        return beginning, ending

    def before_write_frames(self):
        self.wf.write('"channel0":[')

    def pack_frame(self, frame):
        return map_dict_to_indices(frame, self.header_data['props'])

    def after_write_frames(self):
        self.wf.write(']')
