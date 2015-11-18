
import pyaccel as _pyaccel
from . import lattice as _lattice


def families_dipoles():
    return ['bend']


def families_quadrupoles():
    return ['qf', 'qd']


def families_sextupoles():
    return ['sf', 'sd']


def families_horizontal_correctors():
    return ['ch']


def families_vertical_correctors():
    return ['cv']


def families_rf():
    return ['cav']


def get_family_data(lattice):
    latt_dict=_pyaccel.lattice.find_dict(lattice,'fam_name')
    data={}

    for key in latt_dict.keys():
        if key in _family_segmentation.keys():
            data[key] = {'index' : latt_dict[key], 'nr_segs' : _family_segmentation[key]}

    for key in data.keys():
        if key == 'qf':
            idx=data[key]['index'].pop()
            data[key]['index'].insert(0,idx)

        if data[key]['nr_segs'] != 1:
            new_index = []
            j = 0
            for i in range(len(data[key]['index'])//data[key]['nr_segs']):
                new_index.append(data[key]['index'][j:j+data[key]['nr_segs']])
                j += data[key]['nr_segs']
            data[key]['index'] = new_index

    #girders
    girder =  get_girder_data(lattice)
    if girder is not None: data['girder'] = girder

    return data

def get_girder_data(lattice):
    data = []
    girders = _pyaccel.lattice.find_indices(lattice,'fam_name','girder')
    if len(girders) == 0: return None

    idx = list(range(girders[-1], len(lattice))) + list(range(girders[0]))
    data.append(dict({'index':idx}))

    gir = girders[1:-1]
    gir_ini = gir[0::2]
    gir_end = gir[1::2]
    for i in range(len(gir_ini)):
        idx = list(range(gir_ini[i],gir_end[i]+1))
        data.append(dict({'index':idx}))

    return data


_family_segmentation={ 'b'  : 14, 'qf' : 2, 'qd' : 1, 'sd' : 1,
                       'sf' : 1, 'bpm' : 1, 'ch' : 1, 'cv' : 1,
                       'cav' : 1, 'start': 1,}
_family_mapping = {
    'b': 'dipole',
    'bend': 'dipole',

    'qf': 'quadrupole',
    'qd': 'quadrupole',

    'sd': 'sextupole',
    'sf': 'sextupole',

    'bpm': 'bpm',

    'ch': 'horizontal_corrector',
    'cv': 'vertical_corrector',

    'cav': 'rf_cavity',
}
