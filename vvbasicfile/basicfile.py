from vvbasicfile import ijson
from ujson import dumps as to_minjson


class BasicFormatReader:
    def __init__(self, readpath):
        self.readpath = readpath
        self.rf = None
        self.packed_frames_gen = None

        # for compatibility with python3
        self.__next__ = self.next

    # should be overwritten by child classes for channel support
    data_location = 'data'

    def __enter__(self):
        self.onenter()  # overwritten in subclasses

        self.rf = open(self.readpath, 'r')

        self.packed_frames_gen = ijson.items(self.rf, self.data_location + '.item')
        return self

    # overwritten in children
    def onenter(self): pass

    def __iter__(self):
        """
        for frame in reader:
            ...
        """
        return self

    def next(self):
        try:
            packed_frame = next(self.packed_frames_gen)
            unpacked_frame = self.unpack_frame(packed_frame)
            return unpacked_frame
        except StopIteration:
            raise StopIteration('no more frames to read from basicfile')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rf.close()

    # overwritten in children
    def unpack_frame(self, packed_frame): return packed_frame


class BasicFrameMaker:
    """
    Generator for BasicFormat frames
    """
    def __init__(self, data, make_frame=None, config=None):
        self.data = data
        self.make_frame = make_frame
        self.num_frames = config['num_frames']
        # for compatibility with python3
        self.__next__ = self.next

        self.frame_gen = self._gen()

    def _gen(self):
        for sample_num in range(self.num_frames):
            yield self.make_frame(sample_num, self.data)

    def __iter__(self):
        return self

    def next(self):
        return next(self.frame_gen)


class BasicFormatWriter:
    def __init__(self, frame_maker, header_data=None):
        self.frame_maker = frame_maker
        self.header_data = header_data
        self.wf = None

    def write(self, destfilepath, tqdm=None):
        wf = self.wf = open(destfilepath, 'w')
        beginning, ending = self.create_stream_wrapper_parts(self.header_data)

        wf.write(beginning)

        # > multiple channels control code might have smth here (like a for loop)
        # add flag for num_channels

        self.before_write_frames()

        enum_frame_gen = enumerate(self.frame_maker)
        if tqdm is not None:
            enum_frame_gen = tqdm(enum_frame_gen, unit='frames')

        for frame_num, frame in enum_frame_gen:
            packed_frame = self.pack_frame(frame)

            try:
                current_frame_jsonstr = ',' + to_minjson(packed_frame)
            except:
                wf.write(',{"err":22}')  # 22: EINVAL, invalid argument
                continue

            if frame_num is 0:
                current_frame_jsonstr = current_frame_jsonstr[1:]

            try:
                wf.write(current_frame_jsonstr)
            except:
                wf.write(',{"err":5}')  # 5: EIO, I/O error

        self.after_write_frames()

        # > multiple channels control code might have smth here (like end of a for loop)

        wf.write(ending)

        wf.close()

    # The following functions should be defined by a child class

    @staticmethod
    def create_stream_wrapper_parts(header_data):
        raise Exception('create_stream_wrapper_parts must be defined by a child class')

    def before_write_frames(self): pass

    def pack_frame(self, unpacked_frame): return unpacked_frame

    def after_write_frames(self): pass
