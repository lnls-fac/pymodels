
from . import lattice as _lattice
import pyaccel as _pyaccel


def families_dipoles():
    return ('bend',)


def families_quadrupoles():
    return ('qfa', 'qda', 'qfb', 'qdb1', 'qdb2', 'qf1', 'qf2', 'qf3', 'qf4',)


def families_sextupoles():
    return ('sfa', 'sda', 'sfb', 'sdb', 'sd1', 'sd2', 'sd3', 'sd4', 'sd5', 'sd6', 'sf1', 'sf2', 'sf3', 'sf4',)


def families_horizontal_correctors():
    return ('chf', 'chs',)


def families_vertical_correctors():
    return ('cvf', 'cvs',)


def families_skew_correctors():
    return ('qs',)


def families_rf():
    return ('cav',)


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
    data['chs']['families'] = ['sfa','sd1','sd2','sf2','sf3','sd5','sd6','sfb']
    for family in data['chs']['families']:
        data['chs']['index'] = data['chs']['index'] + data[family]['index']
    data['chs']['index']=sorted(data['chs']['index'])

    # cvs - slow vertical correctors
    data['cvs']={}
    data['cvs']['index']=[]
    data['cvs']['families'] = ['sfa','sd1','sd3','sd4','sd6','sfb']
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
    data['qs']['families'] = ['sda','sf1','sf4','sdb']
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

    return data


_family_segmentation={
    'b1'  : 2, 'b2' : 3, 'b3'  : 2, 'bc' : 12,
    'qfa' : 1, 'qda': 1, 'qdb2': 1, 'qfb': 1,
    'qdb1': 1, 'qf1': 1, 'qf2' : 1, 'qf3': 1, 'qf4': 1,
    'sda' : 1, 'sfa': 1, 'sdb' : 1, 'sfb': 1, 'sd1': 1, 'sf1': 1, 'sd2': 1,
    'sd3' : 1, 'sf2': 1, 'sd6' : 1, 'sf4': 1, 'sd5': 1, 'sd4': 1, 'sf3': 1,
    'bpm' : 1, 'cf' : 1,
    'chf' : 1, 'cvf': 1, 'qs'  : 1, 'chs': 1, 'cvs': 1, 'qn' : 1,
    'cav' : 1,
}
_family_data = get_family_data(_lattice._the_ring)
_family_mapping = {
    'b1': 'dipole',
    'b2': 'dipole',
    'b3': 'dipole',
    'bc': 'dipole',

    'qfa': 'quadrupole',
    'qda': 'quadrupole',
    'qdb2': 'quadrupole',
    'qfb': 'quadrupole',
    'qdb1': 'quadrupole',
    'qf1': 'quadrupole',
    'qf2': 'quadrupole',
    'qf3': 'quadrupole',
    'qf4': 'quadrupole',

    'sda': 'sextupole',
    'sfa': 'sextupole',
    'sdb': 'sextupole',
    'sfb': 'sextupole',
    'sd1': 'sextupole',
    'sf1': 'sextupole',
    'sd2': 'sextupole',
    'sd3': 'sextupole',
    'sf2': 'sextupole',
    'sd6': 'sextupole',
    'sf4': 'sextupole',
    'sd5': 'sextupole',
    'sd4': 'sextupole',
    'sf3': 'sextupole',

    'bpm': 'bpm',

    'cf': 'fast_corrector',
    'chf': 'fast_horizontal_corrector',
    'cvf': 'fast_horizontal_corrector',

    'chs': 'slow_horizontal_corrector',
    'cvs': 'slow_vertical_corrector',

    'qs': 'skew_quadrupole',
}
