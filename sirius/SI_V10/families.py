"""Element family definitions"""

from . import lattice as _lattice
import pyaccel as _pyaccel


def families_dipoles():
    return ['bend',]

def families_quadrupoles():
    return ['qfa', 'qda', 'qfb', 'qdb1', 'qdb2', 'qf1', 'qf2', 'qf3', 'qf4',]

def families_sextupoles():
    return ['sda', 'sfa', 'sdb', 'sfb',
            'sd1j', 'sf1j', 'sd2j', 'sd3j', 'sf2j',
            'sd1k', 'sf1k', 'sd2k', 'sd3k', 'sf2k', ]

def families_horizontal_correctors():
    return ['chf', 'chs',]

def families_vertical_correctors():
    return ['cvf', 'cvs',]

def families_skew_correctors():
    return ['qs',]

def families_rf():
    return ['cav',]

def get_family_data(lattice):
    """Get pyaccel lattice model index and segmentation for each family name

    Keyword argument:
    lattice -- lattice model

    Returns dict.
    """
    latt_dict=_pyaccel.lattice.find_dict(lattice,'fam_name')
    data={}
    for key in latt_dict.keys():
        if key in _family_segmentation.keys():
            data[key]={'index' : latt_dict[key], 'nr_segs' : _family_segmentation[key] , 'families' : key}

    for key in data.keys():
        if data[key]['nr_segs'] != 1:
            new_index=[]
            j=0
            for i in range(len(data[key]['index'])//data[key]['nr_segs']):
                new_index.append(data[key]['index'][j:j+data[key]['nr_segs']])
                j += data[key]['nr_segs']
            data[key]['index']=new_index

    # chs - slow horizontal correctors
    data['chs']={}
    data['chs']['index']=[]
    data['chs']['families'] = ['sfa','sfb','sd1j','sf2j','sd1k','sf2k']
    for family in data['chs']['families']:
        data['chs']['index'] = data['chs']['index'] + data[family]['index']
    data['chs']['index']=sorted(data['chs']['index'])

    # cvs - slow vertical correctors
    data['cvs']={}
    data['cvs']['index']=[]
    data['cvs']['families'] = ['sfa','sfb','sd1j','sd3j','sd1k','sd3k']
    for family in data['cvs']['families']:
        data['cvs']['index'] = data['cvs']['index'] + data[family]['index']
    data['cvs']['index']=sorted(data['cvs']['index'])

    # chf - fast horizontal correctors
    data['chf']={}
    data['chf']['families'] = ['cf']
    data['chf']['index']=data['cf']['index']

    # cvf - fast vertical correctors
    data['cvf']={}
    data['cvf']['families'] = ['cf']
    data['cvf']['index']=data['cf']['index']

    # qs - skew quad correctors
    data['qs']={}
    data['qs']['index']=[]
    data['qs']['families'] = ['sda','sfa','sf1j','sf1k']
    for family in data['qs']['families']:
        data['qs']['index'] = data['qs']['index'] + data[family]['index']
    data['qs']['index']=sorted(data['qs']['index'])

    # qn - quadrupoles knobs for optics correction
    data['qn']={}
    data['qn']['index']=[]
    data['qn']['families'] = ['qfa','qda','qf1','qf2','qf3','qf4','qdb1','qfb','qdb2']
    for family in data['qn']['families']:
        data['qn']['index'] = data['qn']['index'] + data[family]['index']
    data['qn']['index']=sorted(data['qn']['index'])

    # rf cavity
    data['cav']

    #girders
    girder =  get_girder_data(lattice)
    if girder is not None:
        data['girder'] = girder

    return data

def get_girder_data(lattice):
    data = []
    gir = _pyaccel.lattice.find_indices(lattice,'fam_name','girder')
    if len(gir) == 0: return None

    gir_ini = gir[0::2]
    gir_end = gir[1::2]
    for i in range(len(gir_ini)):
        idx = list(range(gir_ini[i],gir_end[i]+1))
        data.append(dict({'index':idx}))

    return data

_family_segmentation={
    'b1'  : 2, 'b2' : 3, 'bc_hf' : 14, 'bc_lf' : 14,
    'qfa' : 1, 'qda': 1, 'qdb2': 1, 'qfb': 1,
    'qdb1': 1, 'qf1': 1, 'qf2' : 1, 'qf3': 1, 'qf4': 1,
    'sda' : 1, 'sfa': 1, 'sdb' : 1, 'sfb': 1,
    'sd1j': 1, 'sf1j': 1, 'sd2j': 1, 'sd3j' : 1, 'sf2j': 1,
    'sd1k': 1, 'sf1k': 1, 'sd2k': 1, 'sd3k' : 1, 'sf2k': 1,
    'bpm' : 1, 'cf' : 1,
    'chf' : 1, 'cvf': 1, 'qs'  : 1, 'chs': 1, 'cvs': 1, 'qn' : 1,
    'cav' : 1,
}

_family_mapping = {

    'b1': 'dipole',
    'b2': 'dipole',
    'bc': 'dipole',

    'qfa' : 'quadrupole',
    'qda' : 'quadrupole',
    'qdb2': 'quadrupole',
    'qfb' : 'quadrupole',
    'qdb1': 'quadrupole',
    'qf1' : 'quadrupole',
    'qf2' : 'quadrupole',
    'qf3' : 'quadrupole',
    'qf4' : 'quadrupole',

    'sda' : 'sextupole',
    'sfa' : 'sextupole',
    'sdb' : 'sextupole',
    'sfb' : 'sextupole',
    'sd1j': 'sextupole',
    'sf1j': 'sextupole',
    'sd2j': 'sextupole',
    'sd3j': 'sextupole',
    'sf2j': 'sextupole',
    'sd1k': 'sextupole',
    'sf1k': 'sextupole',
    'sd2k': 'sextupole',
    'sd3k': 'sextupole',
    'sf2k': 'sextupole',

    'bpm': 'bpm',

    'cf' : 'fast_corrector',
    'chf': 'fast_horizontal_corrector',
    'cvf': 'fast_vertical_corrector',

    'chs': 'slow_horizontal_corrector',
    'cvs': 'slow_vertical_corrector',

    'qs' : 'skew_quadrupole',
}
