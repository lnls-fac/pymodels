"""Element family definitions"""

import numpy as _numpy
import pyaccel as _pyaccel
from . import lattice as _lattice

def families_dipoles():
    return ['B1','B2','BC']

def families_quadrupoles():
    return ['QFA', 'QDA', 'QFB', 'QDB1', 'QDB2', 'QFP', 'QDP1', 'QDP2', 'Q1', 'Q2', 'Q3', 'Q4',]

def families_sextupoles():
    return ['SDA0', 'SDB0', 'SDP0',
            'SDA1', 'SDB1', 'SDP1',
            'SDA2', 'SDB2', 'SDP2',
            'SDA3', 'SDB3', 'SDP3',
            'SFA0', 'SFB0', 'SFP0',
            'SFA1', 'SFB1', 'SFP1',
            'SFA2', 'SFB2', 'SFP2']

def families_horizontal_correctors():
    return ['FCH', 'CH',]

def families_vertical_correctors():
    return ['FCV', 'CV',]

def families_skew_correctors():
    return ['QS',]

def families_rf():
    return ['RFCav',]

def families_pulsed_magnets():
    return ['InjDpK', 'InjNLK']

def get_section_name_mapping(lattice):
    lat = lattice[:]
    section_map = ['' for i in range(len(lat))]

    ## find where the nomenclature starts counting and shift the lattice:
    start = _pyaccel.lattice.find_indices(lat,'fam_name','start')[0]
    b1 = _pyaccel.lattice.find_indices(lat, 'fam_name','B1')
    if b1[0]>start:
        ind_shift = (b1[-1] + 1) # Next element of last b1
    else:
        for i in b1[::-1]: # except there is a b1 before start
            if i<start:
                ind_shift = i + 1
                break
    lat = _pyaccel.lattice.shift(lat,ind_shift)

    #Find indices important to define the change of the names of the subsections
    b1 = _pyaccel.lattice.find_indices(lat,'fam_name','B1')
    b1_nrsegs = len(b1)//40
    b2 = _pyaccel.lattice.find_indices(lat,'fam_name','B2')
    b2_nrsegs = len(b2)//40
    bc = _pyaccel.lattice.find_indices(lat,'fam_name','BC_LF')
    bpm = _pyaccel.lattice.find_indices(lat,'fam_name','BPM')

    ## divide the ring in 20 sectors defined by the b1 dipoles:
    Sects = []
    ini = 0
    for i in range(len(b1)//(2*b1_nrsegs)):
        fim = b1[(i+1)*2*b1_nrsegs-1] + 1
        Sects.append(list(range(ini,fim)))
        ini = fim

    # Names of the subsections:
    sub_secs = ['M1','SX','M2','','C1','','C2','','C3','','C4','']
    symm = ['SA','SB','SP','SB']

    for i, sec in enumerate(Sects,1):
        ## conditions that define change in subsection name:
        sec_b1 = [x for x in b1 if sec[0]<= x <= sec[-1]] # define changes to '' and C1
        relev_inds  = [sec_b1[0]-1, sec_b1[b1_nrsegs-1], sec_b1[b1_nrsegs]-1, sec_b1[-1]]
        sec_b2 = [x for x in b2 if sec[0]<= x <= sec[-1]] # define changes to '', C2 and C4
        relev_inds += [sec_b2[0]-1, sec_b2[b2_nrsegs-1], sec_b2[b2_nrsegs]-1, sec_b2[-1]]
        sec_bc = [x for x in bc if sec[0]<= x <= sec[-1]] # define changes to '' and C3
        relev_inds += [sec_bc[0]-1, sec_bc[-1]]
        sec_bpm = [x for x in bpm if sec[0]<= x <= sec[-1]] # define changes to SX and M2
        relev_inds += [sec_bpm[0], sec_bpm[1]-1]
        relev_inds.sort()
        ## fill the section_map variable
        ref = 0
        for j in sec:
            section_map[(ind_shift+j)%len(lat)] = "{0:02d}".format(i)
            section_map[(ind_shift+j)%len(lat)] += symm[(i-1)%len(symm)] if sub_secs[ref] == 'SX' else sub_secs[ref]
            if j >= relev_inds[ref]: ref += 1

    return section_map


def get_family_data(lattice):
    """Get pyaccel lattice model index and segmentation for each family name

    Keyword argument:
    lattice -- lattice model

    Returns dict.
    """
    latt_dict = _pyaccel.lattice.find_dict(lattice,'fam_name')
    section_map = get_section_name_mapping(lattice)

    #### Fill the data dictionary with index info ######
    data = {}
    for key, idx in latt_dict.items():
        nr = _family_segmentation.get(key)
        if nr is None: continue
        data[key] = idx

    # ch - slow horizontal correctors
    idx = []
    fams = ['SDA0', 'SFB0', 'SFP0', 'SDA1', 'SDB1', 'SDP1', 'SFA2', 'SFB2', 'SFP2']
    for fam in fams: idx.extend(latt_dict[fam])
    data['CH']=sorted(idx)

    # cv - slow vertical correctors
    idx = []
    fams = ['SDA0', 'SFB0', 'SFP0', 'SDA1', 'SDB1', 'SDP1',
            'SDA3', 'SDB3', 'SDP3', 'SFA2', 'SFB2', 'SFP2', 'CV']
    for fam in fams:
        if fam in {'SFA2', 'SFB2', 'SFP2'}: # for these families there are skew only in C3 sections
            idx.extend([i for i in latt_dict[fam] if 'C3' in section_map[i]])
        else:
            idx.extend(latt_dict[fam])
    data['CV']=sorted(idx)

    # bc
    data['BC']=sorted(latt_dict['BC_HF']+latt_dict['BC_LF'])

    # fch - fast horizontal correctors
    data['FCH']=sorted(latt_dict['FC']+latt_dict['FCQ'])

    # fcv - fast vertical correctors
    data['FCV']=sorted(latt_dict['FC']+latt_dict['FCQ'])

    # qs - skew quad correctors
    idx = []
    fams = ['SFA0', 'SDB0', 'SDP0', 'FCQ', 'SDA2', 'SDB2', 'SDP2', 'SDA3', 'SDB3', 'SDP3']
    for fam in fams:
        if fam in {'SDA2', 'SDB2', 'SDP2'}: # for these families there are skew only in C1 sections
            idx.extend([i for i in latt_dict[fam] if 'C1' in section_map[i]])
        elif fam in {'SDA3', 'SDB3', 'SDP3'}:# for these families there are skew only in C3 sections
            idx.extend([i for i in latt_dict[fam] if 'C3' in section_map[i]])
        else:
            idx.extend(latt_dict[fam])
    data['QS']=sorted(idx)

    # quadrupoles knobs for optics correction
    idx = []
    fams = ['QFA','QDA', 'QDB2', 'QFB', 'QDB1', 'QDP2', 'QFP', 'QDP1', 'Q1', 'Q2','Q3', 'Q4']
    for fam in fams: idx.extend(latt_dict[fam])
    data['QN']=sorted(idx)

    # sbs - sextupoles knobs for optics correction
    idx = []
    fams = ['SDA0', 'SDB0', 'SDP0', 'SDA1', 'SDB1', 'SDP1', 'SDA2', 'SDB2', 'SDP2', 'SDA3', 'SDB3', 'SDP3',
            'SFA0', 'SFB0', 'SFP0', 'SFA1', 'SFB1', 'SFP1', 'SFA2', 'SFB2', 'SFP2']
    for fam in fams: idx.extend(latt_dict[fam])
    data['SN']=sorted(idx)


    ### Now organize the data dictionary:
    new_data = dict()
    for key, idx in data.items():
        # Create a list of lists for the indexes
        nr = _family_segmentation.get(key)
        if nr is None: continue
        new_idx = [ idx[i*nr:(i+1)*nr] for i in range(len(idx)//nr)  ]

        # find out the name of the section each element is installed
        secs = [ section_map[i[0]] for i in new_idx ]

        # find out if there are more than one element per section and attribute a number to it
        num = len(secs)*['']
        if len(secs)>1:
            j=1
            f = lambda x: '{0:d}'.format(x)
            num[0]     = f(j)   if secs[0]==secs[1] else                           ''
            j          = j+1    if secs[0]==secs[1] else                           1
            for i in range(1,len(secs)-1):
                num[i] = f(j)   if secs[i]==secs[i+1] or secs[i]==secs[i-1] else   ''
                j      = j+1    if secs[i]==secs[i+1] else                         1
            num[-1]    = f(j)   if (secs[-1] == secs[-2]) else                     ''

        new_data[key] = {'index':new_idx, 'subsection':secs, 'instance':num}

    #girders
    girder =  get_girder_data(lattice)
    if girder is not None: new_data['girder'] = girder

    return new_data

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
    'b1'    : 30, 'b2'    : 36,
    'bc'    : 44, 'bc_hf' : 16, 'bc_lf' : 14,
    'qfa'   : 1,  'qda'   : 1,
    'qfb'   : 1,  'qdb1'  : 1,  'qdb2'  : 1,
    'qfp'   : 1,  'qdp1'  : 1,  'qdp2'  : 1,
    'q1'    : 1,  'q2'    : 1,  'q3'    : 1,  'q4'   : 1,
    'sda0'  : 1, 'sdb0'   : 1,  'sdp0'  : 1,
    'sda1'  : 1, 'sdb1'   : 1,  'sdp1'  : 1,
    'sda2'  : 1, 'sdb2'   : 1,  'sdp2'  : 1,
    'sda3'  : 1, 'sdb3'   : 1,  'sdp3'  : 1,
    'sfa0'  : 1, 'sfb0'   : 1,  'sfp0'  : 1,
    'sfa1'  : 1, 'sfb1'   : 1,  'sfp1'  : 1,
    'sfa2'  : 1, 'sfb2'   : 1,  'sfp2'  : 1,
    'bpm'   : 1, 'rbpm'   : 1,
    'fc'    : 1, 'fcq'    : 1,  'fch'   : 1,  'fcv'  : 1,
    'qs'    : 1, 'ch'     : 1,  'cv'    : 1,  'qn'   : 1, 'sn' : 1,
    'cav'   : 1, 'start'  : 1,
    'dipk'  : 1, 'nlk'    : 1,
}

_family_mapping = {

    'b1'  : 'dipole',
    'b2'  : 'dipole',
    'bc'  : 'dipole',

    'qfa' : 'quadrupole',
    'qda' : 'quadrupole',
    'qdb2': 'quadrupole',
    'qfb' : 'quadrupole',
    'qdb1': 'quadrupole',
    'qdp2': 'quadrupole',
    'qfp' : 'quadrupole',
    'qdp1': 'quadrupole',
    'q1'  : 'quadrupole',
    'q2'  : 'quadrupole',
    'q3'  : 'quadrupole',
    'q4'  : 'quadrupole',

    'sda0': 'sextupole',
    'sdb0': 'sextupole',
    'sdp0': 'sextupole',
    'sda1': 'sextupole',
    'sdb1': 'sextupole',
    'sdp1': 'sextupole',
    'sda2': 'sextupole',
    'sdb2': 'sextupole',
    'sdp2': 'sextupole',
    'sda3': 'sextupole',
    'sdb3': 'sextupole',
    'sdp3': 'sextupole',
    'sfa0': 'sextupole',
    'sfb0': 'sextupole',
    'sfp0': 'sextupole',
    'sfa1': 'sextupole',
    'sfb1': 'sextupole',
    'sfp1': 'sextupole',
    'sfa2': 'sextupole',
    'sfb2': 'sextupole',
    'sfp2': 'sextupole',

    'nlk'  : 'pulsed_magnet',
    'dipk' : 'pulsed_magnet',

    'bpm' : 'bpm',
    'rbpm': 'bpm',

    'fc'  : 'fast_corrector',
    'fcq' : 'fast_corrector',
    'fch' : 'fast_horizontal_corrector',
    'fcv' : 'fast_vertical_corrector',

    'ch'  : 'slow_horizontal_corrector',
    'cv'  : 'slow_vertical_corrector',

    'qs'  : 'skew_quadrupole',
}
