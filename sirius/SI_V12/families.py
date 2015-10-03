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
    return ['fch', 'ch',]

def families_vertical_correctors():
    return ['fcv', 'cv',]

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
            data[key]={'index' : latt_dict[key], 'nr_segs' : _family_segmentation[key]}

    # ch - slow horizontal correctors
    data['ch']={}
    data['ch']['index'] = []
    data['ch']['index'] = data['ch']['index'] + data['sfa']['index']
    data['ch']['index'] = data['ch']['index'] + data['sfb']['index']
    data['ch']['index'] = data['ch']['index'] + data['sd1j']['index']
    data['ch']['index'] = data['ch']['index'] + data['sf2j']['index']
    data['ch']['index'] = data['ch']['index'] + data['sd1k']['index']
    data['ch']['index'] = data['ch']['index'] + data['sf2k']['index']
    data['ch']['index']=sorted(data['ch']['index'])
    data['ch']['nr_segs'] = _family_segmentation['ch']

    # cv - slow vertical correctors
    data['cv']={}
    data['cv']['index']=[]
    data['cv']['index']=sorted(data['cv']['index'])
    data['cv']['nr_segs'] = _family_segmentation['cv']

    # fch - fast horizontal correctors
    data['fch']={}
    data['fch']['index'] = data['cf']['index']
    data['fch']['nr_segs'] = _family_segmentation['fch']

    # fcv - fast vertical correctors
    data['fcv']={}
    data['fcv']['index'] = data['cf']['index']
    data['fcv']['nr_segs'] = _family_segmentation['fcv']

    # qs - skew quad correctors
    data['qs']={}
    data['qs']['index'] = []
    data['qs']['index'] = data['qs']['index'] + data['sda']['index']
    data['qs']['index'] = data['qs']['index'] + data['sfa']['index']
    data['qs']['index'] = data['qs']['index'] + data['sf1j']['index']
    data['qs']['index'] = data['qs']['index'] + data['sf1k']['index']
    data['qs']['index'] = sorted(data['qs']['index'])
    data['qs']['nr_segs'] = _family_segmentation['qs']

    # qn - quadrupoles knobs for optics correction
    data['qn']={}
    data['qn']['index'] = []
    data['qn']['index'] = data['qn']['index'] + data['qfa']['index']
    data['qn']['index'] = data['qn']['index'] + data['qda']['index']
    data['qn']['index'] = data['qn']['index'] + data['qf1']['index']
    data['qn']['index'] = data['qn']['index'] + data['qf2']['index']
    data['qn']['index'] = data['qn']['index'] + data['qf3']['index']
    data['qn']['index'] = data['qn']['index'] + data['qf4']['index']
    data['qn']['index'] = data['qn']['index'] + data['qdb1']['index']
    data['qn']['index'] = data['qn']['index'] + data['qfb']['index']
    data['qn']['index'] = data['qn']['index'] + data['qdb2']['index']
    data['qn']['index'] = sorted(data['qn']['index'])
    data['qn']['nr_segs'] = _family_segmentation['qn']

    for key in data.keys():
        if data[key]['nr_segs'] != 1:
            new_index=[]
            j=0
            for i in range(len(data[key]['index'])//data[key]['nr_segs']):
                new_index.append(data[key]['index'][j:j+data[key]['nr_segs']])
                j += data[key]['nr_segs']
            data[key]['index']=new_index

    return data


_family_segmentation={
    'b1'  : 2, 'b2' : 3, 'bc_hf' : 14, 'bc_lf' : 14,
    'qfa' : 1, 'qda': 1, 'qdb2': 1, 'qfb': 1,
    'qdb1': 1, 'qf1': 1, 'qf2' : 1, 'qf3': 1, 'qf4': 1,
    'sda' : 1, 'sfa': 1, 'sdb' : 1, 'sfb': 1,
    'sd1j': 1, 'sf1j': 1, 'sd2j': 1, 'sd3j' : 1, 'sf2j': 1,
    'sd1k': 1, 'sf1k': 1, 'sd2k': 1, 'sd3k' : 1, 'sf2k': 1,
    'bpm' : 1, 'cf' : 1,
    'fch' : 1, 'fcv': 1, 'qs'  : 1, 'ch': 1, 'cv': 1, 'qn' : 1,
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
    'fch': 'fast_horizontal_corrector',
    'fcv': 'fast_vertical_corrector',

    'ch': 'slow_horizontal_corrector',
    'cv': 'slow_vertical_corrector',

    'qs' : 'skew_quadrupole',
}
