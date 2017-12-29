from collections import Mapping
from vvbasicfile import ijson


# Recursive update
def update(d, u):
    for k, v in u.items():
        if isinstance(v, Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


# Clone/copy object
def copy(o):
    o_type = type(o)
    if o_type is dict:
        return o.copy()
    elif o_type is list:
        return o[:]
    else:
        return o


# Used for packing/unpacking frames

# for packing
def map_dict_to_indices(d, keys, leftovers=False):
    if leftovers:
        l, d_leftovers = _map_dict_to_indices_leftovers(d, keys)
        ret = (l, d_leftovers)
    else:
        l = _map_dict_to_indices(d, keys)
        ret = l

    # remove trailing None elements
    while l and l[-1] is None:
        l.pop()

    return ret


def _map_dict_to_indices(d, keys):
    return [d.get(key, None) for key in keys]


def _map_dict_to_indices_leftovers(d, keys):
    d_leftovers = d.copy()
    l = [d_leftovers.pop(key, None) for key in keys]
    return l, d_leftovers


# for unpacking
def map_list_to_keys(l, keys):
    return dict(zip(keys, l))


class SchematicAttributesObject:
    def __init__(self, attrs=None):
        self.attributes = attrs
        self.set_attr_defaults()

    def set_attr_defaults(self):
        for attr, attr_structure in self.attributes.items():
            setattr(self, attr, attr_structure['default'])

    # Schemas
    def validate(self, attr=None, notattr=None):
        """validate and convert data types if necessary"""

        if attr is not None:
            specified_attrs = {attr: self.attributes[attr]}
        else:
            specified_attrs = self.attributes

        for attr, attr_structure in specified_attrs.items():
            if notattr is not None and attr is notattr:
                continue

            attrval = getattr(self, attr)
            if attrval is None or attrval == {}:
                continue

            attr_schema = attr_structure['schema']
            validatedattrval = attr_schema.validate(attrval)
            setattr(self, attr, validatedattrval)


def load_basicfile_field(srcpath, field=None):
    with open(srcpath, 'r') as rf:
        return next(ijson.items(rf, field))