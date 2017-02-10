"""Element family definitions"""

import pyaccel as _pyaccel

_family_segmentation = {
    'B':2, 'CH': 1, 'CV': 1,
    'QD1':1,'QF1':1,'QD2A':1,'QF2A':1,'QF2B':1,'QD2B':1,
    'QF3':1,'QD3':1,'QF4':1,'QD4':1,
    'InjS':2,
    'ICT':1, 'HSlit':1,'VSlit':1,'Scrn':1,'BPM':1
}

family_mapping = {
    'B':       'dipole',
    'CH':      'horizontal_corrector',
    'CV':      'vertical_corrector',
    'QD1':     'quadrupole',
    'QF1':     'quadrupole',
    'QD2A':    'quadrupole',
    'QF2A':    'quadrupole',
    'QF2B':    'quadrupole',
    'QD2B':    'quadrupole',
    'QF3':     'quadrupole',
    'QD3':     'quadrupole',
    'QF4':     'quadrupole',
    'QD4':     'quadrupole',
    'InjS':    'pulsed_magnet',
    'ICT':     'beam_current_monitor',
    'HSlit':   'horizontal_slit',
    'VSlit':   'vertical_slit',
    'Scrn':    'beam_profile_monitor',
    'BPM':     'bpm'
}

def families_dipoles():
    return ['B']

def families_pulsed_magnets():
    return ['InjS']

def families_quadrupoles():
    return ['QD1','QF1','QD2A','QF2A','QF2B','QD2B','QF3','QD3','QF4','QD4']

def families_horizontal_correctors():
    return ['CH']

def families_vertical_correctors():
    return ['CV']

def families_sextupoles():
    return []

def families_skew_correctors():
    return []

def families_rf():
    return []

def families_di():
    return ['ICT','BPM','Scrn','HSlit','VSlit']

def get_section_name_mapping(lattice):
    section_map = len(lattice)*['']

    #Find indices important to define the change of the names of the sections
    b = _pyaccel.lattice.find_indices(lattice,'fam_name','B')
    b_nrsegs = len(b)//3
    start = _pyaccel.lattice.find_indices(lattice,'fam_name','start')
    fim = _pyaccel.lattice.find_indices(lattice,'fam_name','end')

    # Names of the sections:
    secs = ['01','02','03','04']

    ## conditions that define change in section name:
    relev_inds  = [b[b_nrsegs-1], b[2*b_nrsegs-1], b[-1]]
    relev_inds += [fim[0]]
    relev_inds.sort()
    ## fill the section_map variable
    ref = 0
    for j in range(len(lattice)):
        section_map[j] += secs[ref]
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

    return new_data
