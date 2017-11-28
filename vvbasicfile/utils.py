from collections import Mapping


# Recursive update
def update(d, u):
    for k, v in u.iteritems():
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


