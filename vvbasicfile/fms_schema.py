from schema import Schema, Use, Optional, Regex, Or

# Packed data schema; packed data is stored in FmsFormat object attribute '_packeddata'
packed_fms_structure = {
    'schema': Schema({
        'config': {
            'num_channels': Use(int),
            'num_frames': Use(int),
            'speed': Use(float),
            Optional('meta'): Use(dict),
        },
        'props': [Use(str)],
        'data': {  # channels
            Regex('^channel[0-9]+$'): [  # frames
                [  # position-indexed properties
                    Or([Use(float)], dict)
                ]
            ],
        },
    }),
    'default': {
        'config': {
            'num_channels': 1,
            'num_frames': 0,
            'speed': 0.0,
        },
        'props': [],
        'data': {
            'channel0': [],
        },
    },
}

# Unpacked data schema; unpacked data is stored in FmsFormat object attributes
fms_structures = {
    'data': {
        'schema': Schema({
            Regex('^channel[0-9]+$'): [dict],
        }),
        'default': {
            'channel0': [],
        },
    },
    'config': {
        'schema': Schema({
            'num_channels': Use(int),
            'num_frames': Use(int),
            'speed': Use(float),
            Optional('meta'): Use(dict),
        }),
        'default': {
            'num_channels': 1,
            'num_frames': 0,
            'speed': 0.0,
        },
    },
    'props': {
        'schema': Schema([basestring]),
        'default': [],
    },
    '_packeddata': packed_fms_structure,
}