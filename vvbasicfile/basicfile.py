import utils
import json
import gzip


class BasicFormat(utils.SchematicAttributesObject):
    def __init__(self, data=None, packeddata=None, format_attrs=None):
        # uses schemas to validate + defaults to initialize the specified attributes for the format
        utils.SchematicAttributesObject.__init__(self, attrs=format_attrs)

        # hold the data provided, if one dict packed of all the attributes or just a data dict
        if type(packeddata) is dict:
            self._packeddata = packeddata.copy()
            self.validate(attr='_packeddata')
            self._unpack()
            self.validate(notattr='_packeddata')
        elif type(data) is dict:
            utils.update(self.data, data)
            self.validate(attr='data')

    # Files

    # TODO: combine these pairs of functions into load_from_file and write_to_file with
    # compressed option
    # and IF THE FILES GET TOO BIG, *implement optional streaming!* ((1) for json, and sometimes
    #  (2) first for gzip!); from spt to fms, and fms to rnd
    # STREAM PIPELINE: (gzip ->) json -> [->fms/->rnd] -> json (-> gzip)

    # > Load files
    @classmethod
    def load_from_file(cls, filename):
        """load a gzip-compressed json file"""
        with gzip.open(filename, 'rb') as rf:
            jsondata = rf.read()
            packedfiledata = json.loads(jsondata)

            return cls(packeddata=packedfiledata)

    @classmethod
    def load_from_json_file(cls, filename):
        """load a json file"""
        with open(filename, 'r') as rf:
            packedfiledata = json.load(rf)

            return cls(packeddata=packedfiledata)

    # > Write files
    def write_to_file(self, filename):
        self.validate(notattr='_packeddata')
        self._pack()
        self.validate(attr='_packeddata')

        jsondata = json.dumps(self._packeddata)
        with gzip.open(filename, 'wb') as wf:
            wf.write(jsondata)

    def write_to_json_file(self, filename):
        self.validate(notattr='_packeddata')
        self._pack()
        self.validate(attr='_packeddata')

        with open(filename, 'w') as wf:
            json.dump(self._packeddata, wf)

    # Config
    def get_config(self):
        return self.config.copy()

    def update_config(self, config_dict, **config_args):
        utils.update(self.config, config_dict)
        utils.update(self.config, config_args)

    # Data

    # Subclasses implement their own data helper methods

    # The pack/unpack methods should be overriden by subclasses to involve other data attributes

    def _pack(self):
        self._packeddata = {
            'config': utils.copy(self.config),
            'data': utils.copy(self.data),
        }

    def _unpack(self):
        self.config = utils.copy(self._packeddata['config'])
        self.data = utils.copy(self._packeddata['data'])
