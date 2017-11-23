import utils
import msgpack

# TODO: implement JSON formats (reading + writing)
# > create a static function: 'load_from_json' that returns a FmsFormat
# > create methods: 'to_json', 'write_json_to_file'
# no need for a read_output_file
# put those methods in the Super class!


class BasicFormat:
    def __init__(self, format_schema, create_blank, data=None):
        self.format_schema = format_schema

        self._data = create_blank()
        if type(data) is dict:
            utils.update(self._data, data)
            self.validate()

    # Schema
    def validate(self):
        """validate and convert data types if necessary"""
        self._data = self.format_schema.validate(self._data)

    # Files
    @classmethod
    def load(cls, rf):
        filedata = msgpack.unpack(rf)
        return cls(filedata)

    def get_packed(self):
        self.validate()
        return msgpack.packb(self._data)

    def write_to_file(self, filename):
        packeddata = self.get_packed()
        wf = open(filename, 'wb')
        wf.write(packeddata)
        wf.close()

    # Config
    def get_config(self):
        return self._data['config'].copy()

    def update_config(self, config_dict, **config_args):
        config = self._data['config']
        utils.update(config, config_dict)
        utils.update(config, config_args)

    # Data

    # Not 'get_data', since this returns not only the value of the data but
    # also the reference to the data in the internal dict object, self._data

    def data(self):
        return self._data['data']

    # Subclasses implement their own data helper methods
