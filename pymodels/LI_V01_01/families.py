"""Element family definitions"""

import numpy as _np

from siriuspy.namesys import join_name as _join_name
import pyaccel as _pyaccel

_family_segmentation = {
    'Spect': 2, 'Lens': 1, 'LensRev': 1,
    'QF1': 1, 'QF2': 1, 'QF3': 1,
    'QD1': 1, 'QD2': 1,
    'CH': 1, 'CV': 1,
    'Slnd01': 1, 'Slnd02': 1, 'Slnd03': 1, 'Slnd04': 1, 'Slnd05': 1,
    'Slnd06': 1, 'Slnd07': 1, 'Slnd08': 1, 'Slnd09': 1, 'Slnd10': 1,
    'Slnd11': 1, 'Slnd12': 1, 'Slnd13': 1, 'Slnd14': 1, 'Slnd15': 1,
    'Slnd16': 1, 'Slnd17': 1, 'Slnd18': 1, 'Slnd19': 1, 'Slnd20': 1,
    'Slnd21': 1,
    'BPM': 1, 'Scrn': 1, 'ICT': 1,
    'AccStr': 1, 'Bun': 1, 'SHB': 1,
    'EGun': 1
    }

_discipline_mapping = {
    'Spect': 'PS',
    'Lens': 'PS',
    'LensRev': 'PS',
    'QF1': 'PS',
    'QF2': 'PS',
    'QF3': 'PS',
    'QD1': 'PS',
    'QD2': 'PS',
    'CH': 'PS',
    'CV': 'PS',
    'Slnd01': 'PS',
    'Slnd02': 'PS',
    'Slnd03': 'PS',
    'Slnd04': 'PS',
    'Slnd05': 'PS',
    'Slnd06': 'PS',
    'Slnd07': 'PS',
    'Slnd08': 'PS',
    'Slnd09': 'PS',
    'Slnd10': 'PS',
    'Slnd11': 'PS',
    'Slnd12': 'PS',
    'Slnd13': 'PS',
    'Slnd14': 'PS',
    'Slnd15': 'PS',
    'Slnd16': 'PS',
    'Slnd17': 'PS',
    'Slnd18': 'PS',
    'Slnd19': 'PS',
    'Slnd20': 'PS',
    'Slnd21': 'PS',
    'BPM': 'DI',
    'Scrn': 'DI',
    'ICT': 'DI',
    'AccStr': 'RF',
    'Bun': 'RF',
    'SHB': 'RF',
    'EGun': 'EG'
    }

family_mapping = {
    'Spect': 'dipole',
    'Lens': 'magnetic_lens',
    'LensRev': 'magnetic_lens',
    'QF1': 'quadrupole',
    'QF2': 'quadrupole',
    'QF3': 'quadrupole',
    'QD1': 'quadrupole',
    'QD2': 'quadrupole',

    'CH': 'horizontal_corrector',
    'CV': 'vertical_corrector',

    'Slnd01': 'solenoid',
    'Slnd02': 'solenoid',
    'Slnd03': 'solenoid',
    'Slnd04': 'solenoid',
    'Slnd05': 'solenoid',
    'Slnd06': 'solenoid',
    'Slnd07': 'solenoid',
    'Slnd08': 'solenoid',
    'Slnd09': 'solenoid',
    'Slnd10': 'solenoid',
    'Slnd11': 'solenoid',
    'Slnd12': 'solenoid',
    'Slnd13': 'solenoid',
    'Slnd14': 'solenoid',
    'Slnd15': 'solenoid',
    'Slnd16': 'solenoid',
    'Slnd17': 'solenoid',
    'Slnd18': 'solenoid',
    'Slnd19': 'solenoid',
    'Slnd20': 'solenoid',
    'Slnd21': 'solenoid',

    'BPM': 'bpm',
    'Scrn': 'beam_profile_monitor',
    'ICT': 'beam_current_monitor',

    'AccStr': 'accelerating_structure',
    'Bun': 'buncher',
    'SHB': 'sub_harmonic_buncher',
    'EGun': 'electron_gun'
    }


def families_dipoles():
    """."""
    return ['Spect']


def families_pulsed_magnets():
    """."""
    return []


def families_quadrupoles():
    """."""
    return ['QD1', 'QD2', 'QF1', 'QF2', 'QF3']


def families_horizontal_correctors():
    """."""
    return ['CH']


def families_vertical_correctors():
    """."""
    return ['CV']


def families_sextupoles():
    """."""
    return []


def families_skew_correctors():
    """."""
    return []


def families_solenoids():
    """."""
    return [
        'Slnd01', 'Slnd02', 'Slnd03', 'Slnd04', 'Slnd05', 'Slnd06', 'Slnd07',
        'Slnd08', 'Slnd09', 'Slnd10', 'Slnd11', 'Slnd12', 'Slnd13', 'Slnd14',
        'Slnd15', 'Slnd16', 'Slnd17', 'Slnd18', 'Slnd19', 'Slnd20', 'Slnd21'
        ]


def families_lens():
    """."""
    return ['Lens', 'LensRev']


def families_rf():
    """."""
    return ['AccStr', 'Bun', 'SHB']


def families_di():
    """."""
    return ['Scrn', 'ICT', 'BPM']


def families_magnets():
    """."""
    fams = []
    fams.extend(families_dipoles())
    fams.extend(families_quadrupoles())
    fams.extend(families_sextupoles())
    fams.extend(families_skew_correctors())
    fams.extend(families_horizontal_correctors())
    fams.extend(families_vertical_correctors())
    fams.extend(families_solenoids())
    fams.extend(families_lens())
    return fams


def get_section_name_mapping(lattice):
    """."""
    section_map = len(lattice)*['']

    # Find indices important to define the change of the names of the
    # subsections
    spect = _pyaccel.lattice.find_indices(lattice, 'fam_name', 'Spect')
    spect_nrsegs = len(spect)

    # Names of the sections:
    if abs(lattice[spect[0]].angle) >= 40*(_np.pi/360)/spect_nrsegs:
        secs = ['01', '03']
    else:
        secs = ['01', '02']

    # conditions that define change in subsection name:
    relev_inds = [spect[-1], len(lattice)-1]
    relev_inds.sort()
    # fill the section_map variable
    ref = 0
    for j in range(len(lattice)):
        section_map[j] = secs[ref]
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

    # Fill the data dictionary with index info ######
    data = {}
    for key, idx in latt_dict.items():
        nr_ = _family_segmentation.get(key)
        if nr_ is None:
            continue
        # Create a list of lists for the indexes
        data[key] = [idx[i*nr_:(i+1)*nr_] for i in range(len(idx)//nr_)]

    # Now organize the data dictionary:
    new_data = dict()
    for key, idx in data.items():
        # find out the name of the section each element is installed
        secs = [section_map[i[0]] for i in idx]

        # find out if there are more than one element per section and
        # attribute a number to it
        num = len(secs)*['']
        if len(secs) > 1:
            j = 1
            num[0] = f'{j:d}' if secs[0] == secs[1] else ''
            j = j + 1 if secs[0] == secs[1] else 1
            for i in range(1, len(secs)-1):
                num[i] = f'{j:d}' if secs[i] == secs[i+1] or \
                    secs[i] == secs[i-1] else ''
                j = j+1 if secs[i] == secs[i+1] else 1
            num[-1] = f'{j:d}' if (secs[-1] == secs[-2]) else ''

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
        for sub, inst in zip(subs, insts):
            devnames.append(
                _join_name(sec='LI', dis=dis, sub=sub, idx=inst, dev=key))
        new_data[key]['devnames'] = devnames

    return new_data
