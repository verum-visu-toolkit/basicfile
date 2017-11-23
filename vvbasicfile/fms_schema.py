from schema import Schema, Use, Optional, Regex


fms_schema = Schema({
    'config': {
        'num_channels': Use(int),
        'num_frames': Use(int),
        'speed': Use(float),
        Optional('meta'): Use(dict),
    },
    'data': {
        Regex('^channel[0-9]+$'): [dict],
    },
})

blank_fms = {
    'config': {
        'num_channels': 1,
        'num_frames': 0,
        'speed': 0.0,
    },
    'data': {
        'channel0': [],
    },
}


def get_blank_fms():
    return blank_fms.copy()
