from schema import Schema, Use, Optional, Or


rnd_schema = Schema({
    'config': {
        'width': Use(int),
        'height': Use(int),
        'num_frames': Use(int),
        'speed': Use(float),
        Optional('meta'): Use(dict),
    },
    'data': [
        [
            Or({
                'type': Or(unicode, str),
                'args': {
                    Or(unicode, str): object,
                },
                Optional('name'): Or(unicode, str),
            }, {
                'hide': Or(unicode, str),
            })
        ]
    ],
})

blank_rnd = {
    'config': {
        'width': 960,
        'height': 540,
        'num_frames': 0,
        'speed': 0.0,
    },
    'data': []
}


def get_blank_rnd():
    return blank_rnd.copy()
