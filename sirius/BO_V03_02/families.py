
import pyaccel as _pyaccel


_family_segmentation={
    'B-1'  : 20,'B-2'  : 20,'B'  : 20, 'QF' : 2, 'QD' : 1, 'SD' : 1, 'QS':1,
    'SF' : 1, 'CH' : 1, 'CV' : 1,
    'BPM' : 1, 'Scrn':1, 'DCCT':1,'TuneP':1,'TuneS':1,'GSL':1,
    'RFCav' : 1, 'start': 1, 'BEND': 14,
    'InjK': 1, 'EjeK': 1
}

family_mapping = {
    'B': 'dipole',

    'QF': 'quadrupole',
    'QD': 'quadrupole',
    'QS': 'quadrupole',

    'SD': 'sextupole',
    'SF': 'sextupole',

    'InjK': 'pulsed_magnet',
    'EjeK': 'pulsed_magnet',

    'BPM': 'bpm',
    'DCCT':    'beam_current_monitor',
    'Scrn':    'beam_profile_monitor',
    'TuneP':   'tune_pickup',
    'TuneS':   'tune_shaker',

    'CH': 'horizontal_corrector',
    'CV': 'vertical_corrector',

    'RFCav': 'rf_cavity',
}

def families_dipoles():
    return ['B']

def families_quadrupoles():
    return ['QF', 'QD']

def families_sextupoles():
    return ['SF', 'SD']

def families_horizontal_correctors():
    return ['CH']

def families_vertical_correctors():
    return ['CV']

def families_skew_correctors():
    return ['QS']

def families_rf():
    return ['RFCav']

def families_pulsed_magnets():
    return ['InjK', 'EjeK']

def families_di():
    return ['DCCT','BPM','Scrn','TuneP','TuneS','GSL']

def get_section_name_mapping(lattice):
        lat = lattice[:]
        section_map = ['' for i in range(len(lat))]

        ## find where the nomenclature starts counting and shift the lattice:
        start = _pyaccel.lattice.find_indices(lat,'fam_name','start')[0]
        b1 = _pyaccel.lattice.find_indices(lat, 'fam_name','B')
        if b1[0]>start:
            ind_shift = (b1[-1] + 1) # Next element of last b1
        else:
            for i in b1[::-1]: # except there is a b1 before start
                if i<start:
                    ind_shift = i + 1
                    break
        lat = _pyaccel.lattice.shift(lat,ind_shift)

        #Find indices important to define the change of the names of the subsections
        b  = _pyaccel.lattice.find_indices(lat,'fam_name','B')
        qf = _pyaccel.lattice.find_indices(lat,'fam_name','QF')
        b_nrsegs  = len(b )//50
        qf_nrsegs = len(qf)//50

        ## divide the ring in 50 sectors defined by the b1 dipoles:
        Sects = []
        ini = 0
        for i in range(len(b)//b_nrsegs):
            fim = b[(i+1)*b_nrsegs-1] + 1
            Sects.append(list(range(ini,fim)))
            ini = fim

        # Names of the subsections:
        sub_secs = ['U','','D','']

        for i, sec in enumerate(Sects,1):
            ## conditions that define change in subsection name:
            sec_b = [x for x in b if sec[0]<= x <= sec[-1]] # define changes to ''
            relev_inds  = [sec_b[0]-1, sec_b[-1]]
            sec_qf= [x for x in qf if sec[0]<= x <= sec[-1]] # define changes to '' and D
            relev_inds += [sec_qf[0]-1, sec_qf[-1]]
            relev_inds.sort()
            ## fill the section_map variable
            ref = 0
            for j in sec:
                section_map[(ind_shift+j)%len(lat)] = "{0:02d}".format(i)
                section_map[(ind_shift+j)%len(lat)] += sub_secs[ref]
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
    get_idx = lambda x: x[0]

    #### Fill the data dictionary with index info ######
    data = {}
    for key, idx in latt_dict.items():
        nr = _family_segmentation.get(key)
        if nr is None: continue
        # Create a list of lists for the indexes
        data[key] = [ idx[i*nr:(i+1)*nr] for i in range(len(idx)//nr)  ]

    # quadrupoles knobs for optics correction
    idx = []
    fams = ['QF','QD']
    for fam in fams: idx.extend(data[fam])
    data['QN']=sorted(idx,key=get_idx)

    # sbs - sextupoles knobs for optics correction
    idx = []
    fams = ['SD','SF']
    for fam in fams: idx.extend(data[fam])
    data['SN']=sorted(idx,key=get_idx)

    # Dipole Families for power supplies
    idx = []
    fams = ['B']
    for fam in fams: idx.extend(data[fam])
    data['B-1']=sorted(idx,key=get_idx)
    data['B-2']=sorted(idx,key=get_idx)


    ### Now organize the data dictionary:
    new_data = dict()
    for key, idx in data.items():
        # find out the name of the section each element is installed
        secs = [ section_map[get_idx(i)] for i in new_idx ]

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
