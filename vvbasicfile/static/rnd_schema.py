from schema import Schema, Use, Optional, Or

_data_schema_contents = [  # frames
    [  # commands
        Or({  # display command
            'type': basestring,
            'args': {
                basestring: object,
            },
            Optional('name'): basestring,
        }, {  # hide command
            'hide': basestring,
        })
    ]
]

packed_rnd_structure = {
    'schema': Schema({
        'config': {
            'width': Use(int),
            'height': Use(int),
            'num_frames': Use(int),
            'speed': Use(float),
            Optional('meta'): Use(dict),
        },
        'data': _data_schema_contents,
    }),
    'default': {
        'config': {
            'width': 960,
            'height': 540,
            'num_frames': 0,
            'speed': 0.0,
        },
        'data': [],
    },
}


rnd_structures = {
    'config': {
        'schema': Schema({
            'width': Use(int),
            'height': Use(int),
            'num_frames': Use(int),
            'speed': Use(float),
            Optional('meta'): Use(dict),
        }),
        'default': {
            'width': 960,
            'height': 540,
            'num_frames': 0,
            'speed': 0.0,
        },
    },
    'data': {
        'schema': Schema(_data_schema_contents),
        'default': [],
    },
    '_packeddata': packed_rnd_structure,
}