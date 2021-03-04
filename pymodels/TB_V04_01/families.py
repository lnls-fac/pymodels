"""Element family definitions."""

from siriuspy.namesys import join_name as _join_name
import pyaccel as _pyaccel

_family_segmentation = {
    'B': 16, 'CH': 1, 'CV': 1, 'CHV': 1, 'QS': 1,
    'QF2L': 1, 'QD2L': 1, 'QF3L': 1,
    'Spect': 2,
    'QD1': 1, 'QF1': 1, 'QD2A': 1, 'QF2A': 1, 'QF2B': 1, 'QD2B': 1,
    'QF3': 1, 'QD3': 1, 'QF4': 1, 'QD4': 1,
    'InjSept': 6,
    'ICT': 1, 'FCT': 1, 'SlitH': 1, 'SlitV': 1, 'Scrn': 1, 'BPM': 1
    }

_discipline_mapping = {
    'B':       'PS',
    'Spect':   'PS',
    'CHV':     'PS',
    'CH':      'PS',
    'CV':      'PS',
    'QF2L':    'PS',
    'QD2L':    'PS',
    'QF3L':    'PS',
    'QD1':     'PS',
    'QF1':     'PS',
    'QD2A':    'PS',
    'QF2A':    'PS',
    'QF2B':    'PS',
    'QD2B':    'PS',
    'QF3':     'PS',
    'QD3':     'PS',
    'QF4':     'PS',
    'QD4':     'PS',
    'InjSept': 'PU',
    'ICT':     'DI',
    'FCT':     'DI',
    'SlitH':   'DI',
    'SlitV':   'DI',
    'Scrn':    'DI',
    'BPM':     'DI'
    }

family_mapping = {
    'B':       'dipole',
    'Spect':   'spectrometer',
    'CHV':     'general_corrector',
    'CH':      'horizontal_corrector',
    'CV':      'vertical_corrector',
    'QS':      'skew_quadrupole',
    'QF2L':    'linac_quadrupole',
    'QD2L':    'linac_quadrupole',
    'QF3L':    'linac_quadrupole',
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
    'InjSept': 'pulsed_magnet',
    'ICT':     'beam_current_monitor',
    'FCT':     'beam_current_monitor',
    'SlitH':   'horizontal_slit',
    'SlitV':   'vertical_slit',
    'Scrn':    'beam_profile_monitor',
    'BPM':     'bpm'
    }


def families_dipoles():
    """Return dipole families."""
    return ['B', 'Spect']


def families_pulsed_magnets():
    """Return pulsed magnet families."""
    return ['InjSept']


def families_quadrupoles():
    """Return quadrupole families."""
    return [
        'QF2L', 'QD2L', 'QF3L', 'QD1', 'QF1', 'QD2A', 'QF2A', 'QF2B', 'QD2B',
        'QF3', 'QD3', 'QF4', 'QD4']


def families_horizontal_correctors():
    """Return horizontal corrector families."""
    return ['CHV', ]


def families_vertical_correctors():
    """Return vertical corrector families."""
    return ['CHV', ]


def families_sextupoles():
    """Return sextupole families."""
    return []


def families_skew_correctors():
    """Return skew corrector families."""
    return ['QS']


def families_rf():
    """Return RF families."""
    return []


def families_di():
    """Return pulsed magnet families."""
    return ['ICT', 'FCT', 'BPM', 'Scrn', 'SlitH', 'SlitV']


def get_section_name_mapping(lattice):
    """Return list with section name of each lattice element."""
    section_map = len(lattice)*['']

    # find indices important to define the change of the names of the sections
    b = _pyaccel.lattice.find_indices(lattice, 'fam_name', 'B')
    b_nrsegs = len(b)//3

    # names of the sections:
    secs = ['01', '02', '03', '04']

    # conditions that define change in section name:
    relev_inds = [b[b_nrsegs-1], b[2*b_nrsegs-1], b[-1]]
    relev_inds += [len(lattice)-1]
    relev_inds.sort()
    # fill the section_map variable
    ref = 0
    for j in range(len(lattice)):
        section_map[j] += secs[ref]
        if j >= relev_inds[ref]:
            ref += 1

    return section_map


def get_family_data(lattice):
    """Get pyaccel lattice model index and segmentation for each family name.

    Keyword argument:
    lattice -- lattice model

    Returns dict.
    """
    latt_dict = _pyaccel.lattice.find_dict(lattice, 'fam_name')
    section_map = get_section_name_mapping(lattice)

    # fill the data dictionary with index info:
    data = {}
    for key, idx in latt_dict.items():
        nr = _family_segmentation.get(key)
        if nr is None:
            continue
        # create a list of lists for the indexes
        data[key] = [idx[i*nr:(i+1)*nr] for i in range(len(idx)//nr)]

    data['CH'] = list(data['CHV'])
    data['CV'] = list(data['CHV'])

    # last corrector is now a skew quad and a CV:
    data['CV'].extend(data['QS'])

    # now organize the data dictionary:
    new_data = dict()
    for key, idx in data.items():
        # find out the name of the section each element is installed
        secs = [section_map[i[0]] for i in idx]

        # find out if there are more than one element per section and
        # attribute a number to it
        num = len(secs)*['']
        if len(secs) > 1:
            j = 1
            if secs[0] == secs[1]:
                num[0] = '{0:d}'.format(j)
                j += 1
            for i in range(1, len(secs)-1):
                if secs[i] == secs[i+1] or secs[i] == secs[i-1]:
                    num[i] = '{0:d}'.format(j)

                if secs[i] == secs[i+1]:
                    j += 1
                else:
                    j = 1

            if secs[-1] == secs[-2]:
                num[-1] = '{0:d}'.format(j)

        new_data[key] = {'index': idx, 'subsection': secs, 'instance': num}

    # get control system devname
    for key in new_data:
        if key not in _discipline_mapping:
            continue
        dis = _discipline_mapping[key]
        dta = new_data[key]
        devnames = []
        subs = dta['subsection']
        insts = dta['instance']
        sec = 'LI' if key.endswith('L') else 'TB'
        dev = key[:-1] if key.endswith('L') else key
        for sub, inst in zip(subs, insts):
            devnames.append(
                _join_name(sec=sec, dis=dis, sub=sub, idx=inst, dev=dev))
        new_data[key]['devnames'] = devnames

    return new_data
