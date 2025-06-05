graf_labirin = {
    'IN': {
        'benar': 'B1',
        'salah': 'S1'
    },
    'B1': {
        'benar': 'OUT',
        'salah': 'S1'
    },
    'S1': {
        'benar': 'S2',
        'salah': 'L1'
    },
    'S2': {
        'benar': 'OUT',
        'salah': 'L1'
    },
    'L1': {
        'benar': 'L2',
        'salah': 'L1'
    },
    'L2': {
        'benar': 'L3',
        'salah': 'L1'
    },
    'L3': {
        'benar': 'OUT',
        'salah': 'L2'
    },
    'OUT': {}
}