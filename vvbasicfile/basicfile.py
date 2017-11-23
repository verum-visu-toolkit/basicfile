import utils
import json
import gzip


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

    # > Load files
    @classmethod
    def load_from_file(cls, filename):
        """load a gzip-compressed json file"""
        with gzip.open(filename, 'rb') as rf:
            jsondata = rf.read()
            filedata = json.loads(jsondata)
            return cls(filedata)

    @classmethod
    def load_from_json_file(cls, filename):
        """load a json file"""
        with open(filename, 'r') as rf:
            filedata = json.load(rf)
            return cls(filedata)

    # > Write files
    def write_to_file(self, filename):
        self.validate()
        jsondata = json.dumps(self._data)
        with gzip.open(filename, 'wb') as wf:
            wf.write(jsondata)

    def write_to_json_file(self, filename):
        self.validate()
        with open(filename, 'w') as wf:
            json.dump(self._data, wf)

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
