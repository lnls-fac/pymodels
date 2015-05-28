#!/usr/bin/env python3

import math as _math
import pyaccel as _pyaccel
import mathphys as _mp
from . import optics_mode_M0 as _optics_mode_M0

_default_optics_mode = _optics_mode_M0
_energy = 3e9 #[eV]
_family_segmentation={ 'qd'  : 1, 'qf'  : 1, 'bpm' : 1, 'ch'  : 1,
                       'cv'  : 1, 'seb' : 2, 'seg' : 2, 'sef' : 2,
                       'bf'  : 2, 'bd'  : 2}

def create_lattice():

    # -- selection of optics mode --
    global _default_optics_mode
    _default_optics_mode = _optics_mode_M0

    # -- shortcut symbols --
    marker = _pyaccel.elements.marker
    drift  = _pyaccel.elements.drift
    quadrupole   = _pyaccel.elements.quadrupole
    rbend_sirius = _pyaccel.elements.rbend
    hcorrector   = _pyaccel.elements.hcorrector
    vcorrector   = _pyaccel.elements.vcorrector
    strengths    = _default_optics_mode.strengths

    #correctors length
    c_length = 0.1 #Verificar tamanho real

    # -- drifts --
    l20   = drift('l20', 0.20)
    l25   = drift('l25', 0.25)
    l20c  = drift('l20c', 0.20 - c_length/2.0)
    l25c  = drift('l25c', 0.25 - c_length/2.0)
    l25cc = drift('l25cc', 0.25 - c_length)
    l40   = drift('l40', 0.40)

    la1p = drift('la1p', 0.18000)
    la2p = drift('la2p', 0.26777)
    la3p = drift('la3p', 0.26000)

    lb1p = drift('lb1p', 0.22000)
    lb2p = drift('lb2p', 0.35004)

    lc1p = drift('lc1p', 0.23000)
    lc2p = drift('lc2p', 0.28004)
    lc3p = drift('lc3p', 0.26000)

    ld1p = drift('ld1p', 0.16000)
    ld2p = drift('ld2p', 0.17726)
    ld3  = drift('ld3' , 0.25000)
    ld4p = drift('ld4p', 0.22000)
    ld5p = drift('ld5p', 0.30000)

    # -- lattice markers --
    mbf   = marker('mbf')
    mbd   = marker('mbd')
    msf   = marker('msf')
    msg   = marker('msg')
    mseb  = marker('mseb')
    start = marker('start')
    end   = marker('end')

    # -- quadrupoles --
    qa1 = quadrupole('qa1', 0.2, strengths['qa1'])
    qa2 = quadrupole('qa2', 0.2, strengths['qa2'])
    qb1 = quadrupole('qb1', 0.2, strengths['qb1'])
    qc1 = quadrupole('qc1', 0.2, strengths['qc1'])
    qc2 = quadrupole('qc2', 0.2, strengths['qc2'])
    qd1 = quadrupole('qd1', 0.2, strengths['qd1'])
    qd2 = quadrupole('qd2', 0.2, strengths['qd2'])
    qd3 = quadrupole('qd3', 0.2, strengths['qd3'])
    qd4 = quadrupole('qd4', 0.2, strengths['qd4'])

    # -- bpms --
    bpm = marker('bpm')

    # -- correctors --
    ch = quadrupole('ch', c_length, 0.0)
    cv = quadrupole('cv', c_length, 0.0)

    # -- bending magnets --
    deg2rad = _math.pi/180.0

    # -- bf --
    h1 = rbend_sirius('bf', 1.151658/2, 5.333333*deg2rad/2, 5.333333*deg2rad/2, 0, 0, 0, 0, [0, 0, 0], [0, 0.1593, 0])
    h2 = rbend_sirius('bf', 1.151658/2, 5.333333*deg2rad/2, 0, 5.333333*deg2rad/2, 0, 0, 0, [0, 0, 0], [0, 0.1593, 0])
    bf = [h1, mbf, h2]

    # -- bd --
    h1 = rbend_sirius('bd', 1.151658/2, 5.333333*deg2rad/2, 5.333333*deg2rad/2, 0, 0, 0, 0, [0, 0, 0], [0, -0.1593, 0])
    h2 = rbend_sirius('bd', 1.151658/2, 5.333333*deg2rad/2, 0, 5.333333*deg2rad/2, 0, 0, 0, [0, 0, 0], [0, -0.1593, 0])
    bd = [h1, mbd, h2]

    # -- sep booster --
    h1 = rbend_sirius('seb', 0.85/2, -3.6*deg2rad/2, -3.6*deg2rad/2, 0, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    h2 = rbend_sirius('seb', 0.85/2, -3.6*deg2rad/2, 0, -3.6*deg2rad/2, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    septex = [h1, mseb, h2]

    # -- sep grosso --
    h1 = rbend_sirius('seg', 1.10/2, 6.2*deg2rad/2, 6.2*deg2rad/2, 0, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    h2 = rbend_sirius('seg', 1.10/2, 6.2*deg2rad/2, 0, 6.2*deg2rad/2, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    septgr  = [h1, msg, h2]

    # -- sep fino --
    h1 = rbend_sirius('sef', 0.925/2, 3.13*deg2rad/2, 3.13*deg2rad/2, 0, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    h2 = rbend_sirius('sef', 0.925/2, 3.13*deg2rad/2, 0, 3.13*deg2rad/2, 0, 0, 0, [0, 0, 0], [0, 0, 0])
    septfi = [h1, msf, h2]

    # -- lines --
    la1   = [la1p, l20c, cv, l20c, l40, l40]
    la2   = [la2p, l20, l40, l40, l40]
    la3   = [la3p, l40, l40, bpm, l20c, ch, l25cc, cv, l25c]
    lb1   = [lb1p, l20, l40, l40, l40]
    lb2   = [lb2p, l20, l40, l40, l40, l40, bpm, l20c, ch, l25cc, cv, l25c]
    lc1   = [lc1p, l20, l40, l40, l40]
    lc2   = [lc2p, l40]
    lc3   = [lc3p, l20, l40, l40, bpm, l20c, ch, l25cc, cv, l25c]
    ld1   = [ld1p, l20]
    ld2   = [ld2p, l40, l40, bpm, l20c, ch, l25cc, cv, l20c]
    ld4   = [ld4p, l40]
    ld5   = [ld5p, l20, l40, l40, l40, bpm, l20c, cv, l25c]
    linea = [septex, l20, septex, la1, qa1, la2, qa2, la3]
    lineb = [bf, lb1, qb1, lb2]
    linec = [bd, lc1, qc1, lc2, qc2, lc3]
    lined = [bd, ld1, qd1, ld2, qd2, ld3, qd3, ld4, qd4, ld5]
    linee = [septgr, l40, septfi, bpm]
    ltba  = [start, linea, lineb, linec, lined, linee, end]

    # line extension to PMM
    l10      = drift('l10', 0.10)
    lki      = drift('lki', 2.14)
    lkipmm   = drift('lkipmm', 0.807)
    MIA      = marker('MIA')
    sept_in  = marker('sept_in')
    kick_in  = marker('kick_in')
    PMM      = marker('PMM')
    AN_kipmm = [sept_in, l10, MIA, lki, lkipmm, PMM]
    ltba_estendido  = [start, linea, lineb, linec, lined, linee, AN_kipmm, end]

    # finalization
    elist = ltba
    the_line = _pyaccel.lattice.buildlat(elist)

    # shifts model to marker 'start'
    idx = _pyaccel.lattice.findcells(the_line, 'fam_name', 'start')
    the_line = _pyaccel.lattice.shiftlat(the_line, idx[0])

    # sets number of integration steps
    set_num_integ_steps(the_line)

    # Define Camara de Vacuo
    set_vacuum_chamber(the_line)

    return the_line


def set_num_integ_steps(the_line):

    bends = []
    for i in range(len(the_line)):
        if the_line[i].angle:
            bends.append(i)

    dl = 0.035

    for i in range(len(the_line)):
        if the_line[i].angle:
            bend_nis = int( _math.ceil(the_line[i].length/dl))
            if bend_nis <= 10:
                the_line[i].nr_steps = 10
            else:
                the_line[i].nr_steps = bend_nis
        elif any(the_line[i].polynom_b) and i not in bends:
            the_line[i].nr_steps = 10


def set_vacuum_chamber(the_line):
    vchamber_h = 0.016
    vchamber_v = 0.016
    for i in range(len(the_line)):
        the_line[i].hmax = vchamber_h
        the_line[i].vmax = vchamber_v


def sirius_ts_family_data(lattice):
    latt_dict=_pyaccel.lattice.finddict(lattice,'fam_name')
    data={}

    for key in latt_dict.keys():
        if key in _family_segmentation.keys():
            data[key] = {'index' : latt_dict[key], 'nr_segs' : _family_segmentation[key] , 'families' : key}

    #bpm
    data['bpm']['index'].pop()

    # qf
    data['qf']={}
    data['qf']['index'] = []
    data['qf']['nr_segs'] = _family_segmentation['qf']
    data['qf']['families'] = ['qa1', 'qc1', 'qc2', 'qd2', 'qd3']
    for family in data['qf']['families']:
        data['qf']['index'] = data['qf']['index'] + latt_dict[family]
    data['qf']['index']=sorted(data['qf']['index'])

    # qd
    data['qd']={}
    data['qd']['index'] = []
    data['qd']['nr_segs'] = _family_segmentation['qd']
    data['qd']['families'] = ['qa2', 'qb1', 'qd1', 'qd4']
    for family in data['qd']['families']:
        data['qd']['index'] = data['qd']['index'] + latt_dict[family]
    data['qd']['index']=sorted(data['qd']['index'])

    for key in data.keys():
        if data[key]['nr_segs'] != 1:
            new_index = []
            j = 0
            for i in range(len(data[key]['index'])//data[key]['nr_segs']):
                new_index.append(data[key]['index'][j:j+data[key]['nr_segs']])
                j += data[key]['nr_segs']
            data[key]['index'] = new_index

    return data

_the_line=create_lattice()
_family_data=sirius_ts_family_data(_the_line)
