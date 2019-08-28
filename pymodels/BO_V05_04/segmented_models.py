import numpy as _np
import mathphys as _mp
import pyaccel as _pyaccel

rbend_sirius = _pyaccel.elements.rbend
quadrupole = _pyaccel.elements.quadrupole
sextupole = _pyaccel.elements.sextupole
marker = _pyaccel.elements.marker

_d2r = _np.pi/180


def dipole(energy):
    """Dipole segmented model."""
    b, b_edge, b_pb = 1, 2, 3
    # FIELDMAP
    # trajectory centered in good-field region. init_rx is set to +9.045 mm
    # *** interpolation of fields is now cubic ***
    # *** dipole angles were normalized to better close 360 degrees ***
    # *** more refined segmented model.
    # *** dipole angle is now in units of degrees
    # --- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m],[T] for polynom_b ---

    # Average Dipole Model for BD at 3GeV (991.63A)
    # =============================================
    # date: 2019-07-26
    # Based on multipole expansion around reference trajectory from fieldmap analysis of measurement data
    # folder = bo-dipoles/model-09/analysis/hallprobe/production/x-ref-28p255mm-reftraj
    # ref_rx  = 28.255 mm (used in the alignment)
    # init_rx = 9.1476 mm (value that matches ref_rx for the average model)
    # goal_tunes = [19.20433, 7.31417];
    # goal_chrom = [0.5, 0.5];

    b_model_high_en = _np.array([
        #--- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m^(n-1)] for polynom_b ---
        #type   len[m]   angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
        [b,      0.19600, 1.16095, -4.5855e-05, -2.2616e-01, -1.9931e+00, -5.2809e+00, -7.2055e+01, -2.8342e+04, -2.0405e+06],
        [b,      0.19200, 1.14607, -4.6296e-05, -2.1071e-01, -1.9221e+00, -4.9789e+00, -1.5270e+02, +2.4240e+03, -7.1606e+05],
        [b,      0.18200, 1.09390, -4.5705e-05, -1.8355e-01, -1.9326e+00, +1.7971e+00, -2.7381e+02, +3.4881e+03, +2.5253e+05],
        [b,      0.01000, 0.04988, -3.7956e-05, -2.3442e-01, -2.1923e+00, +2.3988e+01, -9.6648e+02, +4.2551e+04, -2.6469e+05],
        [b,      0.01000, 0.03607, -3.2233e-05, -1.5777e-01, -1.7058e+00, +3.5159e+01, -8.1160e+02, +5.4334e+03, -2.2594e+06],
        [b_edge, 0,0,0,0,0,0,0,0,0],
        [b,      0.01300, 0.03238, -2.5586e-05, -5.1427e-02, -2.0566e+00, +2.7487e+01, -1.4495e+03, +1.5325e+04, +2.2138e+06],
        [b,      0.01700, 0.02914, -1.5916e-05, +3.1680e-03, -2.3815e+00, +1.5507e+01, -4.7649e+02, +1.1270e+03, +2.4813e+05],
        [b,      0.02000, 0.02274, -1.1903e-05, +2.1920e-02, -2.1754e+00, +3.5485e+00, +4.8788e+01, -3.0931e+03, -6.3494e+05],
        [b,      0.03000, 0.01848, -7.3813e-06, +1.8886e-02, -1.4361e+00, -1.4453e+00, +9.1969e+01, +3.0972e+03, -3.0985e+05],
        [b,      0.05000, 0.01039, +3.2630e-04, +8.5522e-03, -5.0122e-01, -6.4221e-01, -4.7512e+01, -6.7946e+02, +3.8237e+05],
        [b_pb,   0,0,0,0,0,0,0,0,0]
    ])

    # Dipole Model for BD-006 at 149.3018 MeV (60.46A)
    # =============================================
    # date: 2019-07-29
    # Based on multipole expansion around reference trajectory from fieldmap analysis of measurement data
    # folder = bo-dipoles/model-09/analysis/hallprobe/excitation_curve/x-ref-28p255mm-reftraj/bd-006/0060p46A
    # ref_rx  = 28.255 mm (used in the alignment)
    # init_rx = 9.1563 mm (average, different for each dipole to match ref_rx)
    # goal_tunes = [19.20433, 7.31417];
    # goal_chrom = [0.5, 0.5];

    b_model_low_en = _np.array([
        #--- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m^(n-1)] for polynom_b ---
        #type   len[m]   angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
        [b,      0.19600, 1.16095, -2.9521e-05, -2.2953e-01, -1.9835e+00, -3.1164e+00, -5.5670e+02, -1.7476e+04, -5.0956e+05],
        [b,      0.19200, 1.14607, +4.6028e-05, -2.1389e-01, -1.9732e+00, +1.0720e+00, -3.3952e+02, -2.9134e+04, +1.6710e+06],
        [b,      0.18200, 1.09390, +4.6495e-04, -1.8724e-01, -1.9278e+00, -3.4280e-01, -2.5900e+02, -3.8416e+03, +4.5036e+05],
        [b,      0.01000, 0.04988, +1.3811e-03, -2.5658e-01, -1.8540e+00, +1.4360e+01, +1.5288e+03, -8.5204e+03, -8.8288e+06],
        [b,      0.01000, 0.03607, +1.0497e-03, -1.7873e-01, -1.3828e+00, +1.7956e+01, +1.1377e+03, +2.1959e+04, -9.8321e+06],
        [b_edge, 0,0,0,0,0,0,0,0,0],
        [b,      0.01300, 0.03238, +3.7135e-04, -6.0692e-02, -1.9748e+00, +1.9712e+01, +4.7660e+02, +2.6825e+04, -6.4633e+06],
        [b,      0.01700, 0.02914, +3.8800e-05, +1.0925e-03, -2.4287e+00, +9.8002e+00, +1.9017e+02, +2.7471e+04, -2.9952e+06],
        [b,      0.02000, 0.02274, -1.4480e-04, +2.2144e-02, -2.2824e+00, -3.1138e-01, +7.3542e+02, +2.3161e+04, -3.8130e+06],
        [b,      0.03000, 0.01848, -2.0692e-04, +2.0159e-02, -1.4701e+00, -6.1800e+00, -1.6290e+01, +3.2373e+04, +2.7180e+05],
        [b,      0.05000, 0.01039, -8.3314e-04, +6.7566e-03, -4.7985e-01, +1.4036e+00, -2.2084e+02, -8.8720e+03, +1.0762e+06],
        [b_pb,   0,0,0,0,0,0,0,0,0]
    ])


    # interpolates multipoles linearly in energy
    b_model = b_model_high_en
    b_model[:,3:] = b_model_low_en[:,3:] + (energy - 149.3018e6)/(3e9-149.3018e6) * (b_model_high_en[:,3:] - b_model_low_en[:,3:])

    # turns deflection angle error off (convenient for having a nominal model with zero 4d closed orbit)
    b_model[:,3] = 0

    bd = []
    for i in range(b_model.shape[0]):
        if b_model[i,0] == b:
            bd.append(rbend_sirius('B', length=b_model[i,1], angle=_d2r*b_model[i,2], polynom_b=b_model[i,3:]))
        elif b_model[i,0] == b_edge:
            bd.append(marker('edgeB'))
        elif b_model[i,0] == b_pb:
            bd.append(marker('physB'))
        else:
            raise Exception("Bending type not recognized.")
    mb = marker('mB')
    bd = [bd[::-1] , mb, bd]
    b_length_segmented = 2*sum(b_model[:,1])

    return (bd, b_length_segmented)


def sx_sextupole(energy, fam_name, hardedge_SL):
    """ This script build an AT sextupole model based on analysis of a fieldmap generated for a 3D magnetic model
    of the magnet and based on rotating coil measurement data for the constructed magnet.

    Input:

    energy [eV]         : beam energy
    hardedge_SL [1/m^2] : nominal integrated sextupole strength

    Output:

    model            : AT segmented model
    model_length [m] : total model length

    Procedure:

    1. Renormalizes all multipoles of the fieldmap segmented model so that
       its main integrated multipole matches the nominal one.
    2. Takes the rotating coild integrated multipoles and divides them by
       the magnetic rigidity corresponding to the beam energy. This yields
       the normalized integrated multipolar strengths (PolynomB) for the model
    3. Merges the fieldmap and rotating coil data into one segmented structure.
       It does so by making sure that each corresponding fieldmap integrated multipole
       matches the rotating coil integrated multipole. It keeps the
       longitudinal multipole profile of the segmented model."""

    magnet_type = 2

    b = 1

    # FIELDMAP
    # *** interpolation of fields is now cubic ***
    # *** more refined segmented model.
    # *** dipole angle is now in units of degrees
    #--- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m],[T] for polynom_b ---
    fmap_monomials = _np.array([0,2,8,14],dtype=int)
    main_mon_fmap_idx = _np.where(fmap_monomials == magnet_type)[0][0]

    # Sextupole model 2017-01-05 (3GeV)
    # =================================
    # sextupole model-03
    # filename: 2017-01-05_BO_Sextupole_Model03_Sim_X=-20_20mm_Z=-300_300mm_Imc=135A.txt
    sx_model_3GeV = _np.array([
    # type  len[m]    angle[deg]  PolyB(n=0)   PolyB(n=2)   PolyB(n=8)   PolyB(n=14)
    [b,      0.0525 ,  +0.00000 ,  -2.38e-06 ,  +1.90e+01 ,  -1.79e+10 ,  -3.25e+20]
    ])

    # Sextupole model 2017-01-05 (150Mev)
    # ===================================
    # sextupole model-03
    # filename: 2017-01-05_BO_Sextupole_Model03_Sim_X=-20_20mm_Z=-300_300mm_Imc=6.75A.txt
    sx_model_150MeV = _np.array([
    # type  len[m]    angle[deg]  PolyB(n=0)   PolyB(n=2)   PolyB(n=8)   PolyB(n=14)
    [b,      0.0525 ,  +0.00000 ,  -2.38e-06 ,  +1.90e+01 ,  -1.79e+10 ,  -3.25e+20]
    ])

    # interpolates multipoles linearly in energy
    sx_model = sx_model_3GeV
    sx_model[:,3:] = sx_model_150MeV[:,3:] + (energy - 150e6)/(3e9-150e6) * (sx_model_3GeV[:,3:] - sx_model_150MeV[:,3:])


    # ROTATING COIL MEASUREMENT
    # =========================
    # data based on quadrupole prototype
    # Rescale multipolar profile according to rotating coild measurement
    rcoil_monomials  = _np.array([],dtype=int)
    rcoil_integrated_multipoles = _np.array([],dtype=float)
    # ---------------------------------------------------------------

    fmap_lens = sx_model[:,1]

    # rescale multipoles of the model according to nominal strength value passed as argument
    # --------------------------------------------------------------------------------------
    model_SL = 2*sum(sx_model[:,3+main_mon_fmap_idx] * fmap_lens)
    rescaling = hardedge_SL / model_SL
    sx_model[:,3:] = sx_model[:,3:] * rescaling


    # rescale multipoles of the rotating coild data according to nominal strength value passed as argument
    # ----------------------------------------------------------------------------------------------------
    if len(rcoil_monomials) != 0:
        brho, *_ = _mp.beam_optics.beam_rigidity(energy=energy)
        rcoil_normalized_integrated_multipoles = -rcoil_integrated_multipoles / brho
        rcoil_main_multipole_idx = _np.where(rcoil_monomials == magnet_type)[0][0]
        rescaling = hardedge_SL / rcoil_normalized_integrated_multipoles[rcoil_main_multipole_idx]
        rcoil_normalized_integrated_multipoles = rcoil_normalized_integrated_multipoles * rescaling


    # builds final model with fieldmap and rotating coild measurements
    # ----------------------------------------------------------------
    monomials = _np.unique(_np.hstack([fmap_monomials,rcoil_monomials]))
    sx_modelC = _np.zeros([sx_model.shape[0],len(monomials)+3])
    sx_modelC[:,:3] = sx_model[:,:3]
    for i in range(len(monomials)):
        rcoil_idx = _np.where(rcoil_monomials == monomials[i])[0]
        fmap_idx  = _np.where(fmap_monomials == monomials[i])[0]
        if len(rcoil_idx) == 0:
            # this multipole is not in rotating coil data: does nothing then.
            sx_modelC[:,i+3] = sx_model[:,fmap_idx[0]+3]
        else:
            if len(fmap_idx) == 0:
                # if this multipole is not in fmap model then uses main
                # multipole to build a multipolar profile
                fmap_integrated_multipole = 2*sum(sx_model[:,main_mon_fmap_idx+3] * fmap_lens)
            else:
                fmap_integrated_multipole = 2*sum(sx_model[:,fmap_idx[0]+3] * fmap_lens)
            rescaling = rcoil_normalized_integrated_multipoles[rcoil_idx[0]] / fmap_integrated_multipole
            sx_modelC[:,i+3] = sx_model[:,fmap_idx[0]+3] * rescaling;


    # converts deflection angle from degress to radians
    sx_modelC[:,2] *= _d2r

    # turns deflection angle error off (convenient for having a nominal model with zero 4d closed orbit)
    sel = _np.where(monomials == 0)[0]
    if len(sel):  sx_modelC[:,3+sel[0]] = 0

    sx = []
    for i in range(sx_modelC.shape[0]):
        if sx_modelC[i,0] == b:
            pol_b = _np.zeros(int(max(monomials))+1)
            pol_a = _np.zeros(int(max(monomials))+1)
            pol_b[monomials] = sx_modelC[i,3:]
            s = sextupole(fam_name, 2*sx_modelC[i,1], 0) # factor 2 in length for one-segment model
            s.polynom_b=pol_b
            s.polynom_a=pol_a
            sx.append(s)
        else:
            raise Exception("Sextupole type not recognized.")

    model_length = 2*sum(sx_modelC[:,1])
    return (sx, model_length)


def qd_quadrupole(energy, fam_name, hardedge_KL):
    """ This script build an AT sextupole model based on analysis of a fieldmap generated for a 3D magnetic model
    of the magnet and based on rotating coil measurement data for the constructed magnet.

    Input:

    energy [eV]         : beam energy
    hardedge_SL [1/m^2] : nominal integrated sextupole strength

    Output:

    model            : AT segmented model
    model_length [m] : total model length

    Procedure:

    1. Renormalizes all multipoles of the fieldmap segmented model so that
       its main integrated multipole matches the nominal one.
    2. Takes the rotating coild integrated multipoles and divides them by
       the magnetic rigidity corresponding to the beam energy. This yields
       the normalized integrated multipolar strengths (PolynomB) for the model
    3. Merges the fieldmap and rotating coil data into one segmented structure.
       It does so by making sure that each corresponding fieldmap integrated multipole
       matches the rotating coil integrated multipole. It keeps the
       longitudinal multipole profile of the segmented model."""

    magnet_type = 1

    b = 1

    # FIELDMAP
    # *** interpolation of fields is now cubic ***
    # *** more refined segmented model.
    # *** dipole angle is now in units of degrees
    #--- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m],[T] for polynom_b ---
    fmap_monomials = _np.array([1,5,9,13],dtype=int)
    main_mon_fmap_idx = _np.where(fmap_monomials == magnet_type)[0][0]

    # QD model 2017-01-11 (3GeV)
    # ===========================
    # quadrupole model-02
    # filename: 2017-01-10_BO_QD_Model02_Sim_X=-20_20mm_Z=-300_300mm_Imc=113.7A.txt
    qd_model_3GeV = _np.array([
    # type  len[m]   angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)   PolyB(n=13)
    [b,     0.050  ,  +0.00000 ,  -5.00e-01 ,  +2.48e+04 ,  -6.87e+10 ,  -3.30e+14]
    ])

    # QF model 2017-01-11 (150MeV)
    # ============================
    # quadrupole model-02
    # filename: 2017-01-10_BO_QD_Model02_Sim_X=-20_20mm_Z=-300_300mm_Imc=5.7A.txt
    qd_model_150MeV = _np.array([
    # type  len[m]   angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)   PolyB(n=13)
    [b,      0.050  ,  +0.00000 ,  -5.01e-01 ,  +2.49e+04 ,  -6.89e+10 ,  -3.25e+14]
    ])

    # interpolates multipoles linearly in energy
    qd_model = qd_model_3GeV
    qd_model[:,3:] = qd_model_150MeV[:,3:] + (energy - 150e6)/(3e9-150e6) * (qd_model_3GeV[:,3:] - qd_model_150MeV[:,3:])


    # ROTATING COIL MEASUREMENT
    # =========================
    # data based on quadrupole prototype
    # Rescale multipolar profile according to rotating coild measurement
    rcoil_monomials  = _np.array([],dtype=int)
    rcoil_integrated_multipoles = _np.array([],dtype=float)
    # ---------------------------------------------------------------

    fmap_lens = qd_model[:,1]

    # rescale multipoles of the model according to nominal strength value passed as argument
    # --------------------------------------------------------------------------------------
    model_KL = 2*sum(qd_model[:,3+main_mon_fmap_idx] * fmap_lens)
    rescaling = hardedge_KL / model_KL
    qd_model[:,3:] = qd_model[:,3:] * rescaling


    # rescale multipoles of the rotating coild data according to nominal strength value passed as argument
    # ----------------------------------------------------------------------------------------------------
    if len(rcoil_monomials) != 0:
        brho, *_ = _mp.beam_optics.beam_rigidity(energy=energy)
        rcoil_normalized_integrated_multipoles = -rcoil_integrated_multipoles / brho
        rcoil_main_multipole_idx = _np.where(rcoil_monomials == magnet_type)[0][0]
        rescaling = hardedge_SL / rcoil_normalized_integrated_multipoles[rcoil_main_multipole_idx]
        rcoil_normalized_integrated_multipoles = rcoil_normalized_integrated_multipoles * rescaling


    # builds final model with fieldmap and rotating coild measurements
    # ----------------------------------------------------------------
    monomials = _np.unique(_np.hstack([fmap_monomials,rcoil_monomials]))
    qd_modelC = _np.zeros([qd_model.shape[0],len(monomials)+3])
    qd_modelC[:,:3] = qd_model[:,:3]
    for i in range(len(monomials)):
        rcoil_idx = _np.where(rcoil_monomials == monomials[i])[0]
        fmap_idx  = _np.where(fmap_monomials == monomials[i])[0]
        if len(rcoil_idx) == 0:
            # this multipole is not in rotating coil data: does nothing then.
            qd_modelC[:,i+3] = qd_model[:,fmap_idx[0]+3]
        else:
            if len(fmap_idx) == 0:
                # if this multipole is not in fmap model then uses main
                # multipole to build a multipolar profile
                fmap_integrated_multipole = 2*sum(qd_model[:,main_mon_fmap_idx+3] * fmap_lens)
            else:
                fmap_integrated_multipole = 2*sum(qd_model[:,fmap_idx[0]+3] * fmap_lens)
            rescaling = rcoil_normalized_integrated_multipoles[rcoil_idx[0]] / fmap_integrated_multipole
            qd_modelC[:,i+3] = qd_model[:,fmap_idx[0]+3] * rescaling;


    # converts deflection angle from degress to radians
    qd_modelC[:,2] *= _d2r

    # turns deflection angle error off (convenient for having a nominal model with zero 4d closed orbit)
    sel = _np.where(monomials == 0)[0]
    if len(sel):  qd_modelC[:,3+sel[0]] = 0

    qd = []
    for i in range(qd_modelC.shape[0]):
        if qd_modelC[i,0] == b:
            pol_b = _np.zeros(int(max(monomials))+1)
            pol_a = _np.zeros(int(max(monomials))+1)
            pol_b[monomials] = qd_modelC[i,3:]
            q = quadrupole(fam_name, 2*qd_modelC[i,1], 0) # factor 2 in length for one-segment model
            q.polynom_b=pol_b
            q.polynom_a=pol_a
            qd.append(q)
        else:
            raise Exception("Quadrupole type not recognized.")

    model_length = 2*sum(qd_modelC[:,1])
    return (qd, model_length)


def qf_quadrupole(energy, fam_name, hardedge_KL):
    """ This script build an AT sextupole model based on analysis of a fieldmap generated for a 3D magnetic model
    of the magnet and based on rotating coil measurement data for the constructed magnet.

    Input:

    energy [eV]         : beam energy
    hardedge_SL [1/m^2] : nominal integrated sextupole strength

    Output:

    model            : AT segmented model
    model_length [m] : total model length

    Procedure:

    1. Renormalizes all multipoles of the fieldmap segmented model so that
       its main integrated multipole matches the nominal one.
    2. Takes the rotating coild integrated multipoles and divides them by
       the magnetic rigidity corresponding to the beam energy. This yields
       the normalized integrated multipolar strengths (PolynomB) for the model
    3. Merges the fieldmap and rotating coil data into one segmented structure.
       It does so by making sure that each corresponding fieldmap integrated multipole
       matches the rotating coil integrated multipole. It keeps the
       longitudinal multipole profile of the segmented model."""

    magnet_type = 1

    b = 1

    # FIELDMAP
    # *** interpolation of fields is now cubic ***
    # *** more refined segmented model.
    # *** dipole angle is now in units of degrees
    #--- model polynom_b (rz > 0). units: [m] for length, [rad] for angle and [m],[T] for polynom_b ---
    fmap_monomials = _np.array([1,5,9,13],dtype=int)
    main_mon_fmap_idx = _np.where(fmap_monomials == magnet_type)[0][0]

    # QF model 2017-01-09 (3GeV)
    # ===========================
    # quadrupole model06
    # filename: 2016-11-23_BQF_Model06_Sim_X=-20_20mm_Z=-450_450mm_I=110.8A.txt
    qf_model_3GeV = _np.array([
    # type  len[m]   angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)   PolyB(n=13)
    [b,     0.114  ,  +0.00000 ,  +1.78e+00 ,  -1.91e+04 ,  +2.37e+11 ,  +4.91e+16]
    ])

    # QF model 2017-01-09 (150MeV)
    # ============================
    # quadrupole model06
    # filename: 2016-12-06_BQF_Model06_Sim_X=-20_20mm_Z=-450_450mm_I=5.28A.txt
    qf_model_150MeV = _np.array([
    # type  len[m]   angle[deg]  PolyB(n=1)   PolyB(n=5)   PolyB(n=9)   PolyB(n=13)
    [b,     0.114  ,  +0.00000 ,  +1.78e+00 ,  -1.91e+04 ,  +2.38e+11 ,  +4.91e+16]
    ])

    # interpolates multipoles linearly in energy
    qf_model = qf_model_3GeV
    qf_model[:,3:] = qf_model_150MeV[:,3:] + (energy - 150e6)/(3e9-150e6) * (qf_model_3GeV[:,3:] - qf_model_150MeV[:,3:])


    # ROTATING COIL MEASUREMENT
    # =========================
    # data based on quadrupole prototype
    # Rescale multipolar profile according to rotating coild measurement
    rcoil_monomials  = _np.array([1,5,9,13],dtype=int)
    # based on relative [1.0, -1.0e-3, 1.1e-3, 0.08e-3]:
    rcoil_integrated_multipoles = _np.array([1,-1.066222407330279e+04,1.250513244082492e+11,9.696910847302045e+16])
    # ---------------------------------------------------------------

    fmap_lens = qf_model[:,1]

    # rescale multipoles of the model according to nominal strength value passed as argument
    # --------------------------------------------------------------------------------------
    model_KL = 2*sum(qf_model[:,3+main_mon_fmap_idx] * fmap_lens)
    rescaling = hardedge_KL / model_KL
    qf_model[:,3:] = qf_model[:,3:] * rescaling


    # rescale multipoles of the rotating coild data according to nominal strength value passed as argument
    # ----------------------------------------------------------------------------------------------------
    if len(rcoil_monomials) != 0:
        brho, *_ = _mp.beam_optics.beam_rigidity(energy=energy)
        rcoil_normalized_integrated_multipoles = -rcoil_integrated_multipoles / brho
        rcoil_main_multipole_idx = _np.where(rcoil_monomials == magnet_type)[0][0]
        rescaling = hardedge_KL / rcoil_normalized_integrated_multipoles[rcoil_main_multipole_idx]
        rcoil_normalized_integrated_multipoles = rcoil_normalized_integrated_multipoles * rescaling


    # builds final model with fieldmap and rotating coild measurements
    # ----------------------------------------------------------------
    monomials = _np.unique(_np.hstack([fmap_monomials,rcoil_monomials]))
    qf_modelC = _np.zeros([qf_model.shape[0],len(monomials)+3])
    qf_modelC[:,:3] = qf_model[:,:3]
    for i in range(len(monomials)):
        rcoil_idx = _np.where(rcoil_monomials == monomials[i])[0]
        fmap_idx  = _np.where(fmap_monomials == monomials[i])[0]
        if len(rcoil_idx) == 0:
            # this multipole is not in rotating coil data: does nothing then.
            qf_modelC[:,i+3] = qf_model[:,fmap_idx[0]+3]
        else:
            if len(fmap_idx) == 0:
                # if this multipole is not in fmap model then uses main
                # multipole to build a multipolar profile
                fmap_integrated_multipole = 2*sum(qf_model[:,main_mon_fmap_idx+3] * fmap_lens)
            else:
                fmap_integrated_multipole = 2*sum(qf_model[:,fmap_idx[0]+3] * fmap_lens)
            rescaling = rcoil_normalized_integrated_multipoles[rcoil_idx[0]] / fmap_integrated_multipole
            qf_modelC[:,i+3] = qf_model[:,fmap_idx[0]+3] * rescaling;


    # converts deflection angle from degress to radians
    qf_modelC[:,2] *= _d2r

    # turns deflection angle error off (convenient for having a nominal model with zero 4d closed orbit)
    sel = _np.where(monomials == 0)[0]
    if len(sel):  qf_modelC[:,3+sel[0]] = 0

    qf = []
    for i in range(qf_modelC.shape[0]):
        if qf_modelC[i,0] == b:
            pol_b = _np.zeros(int(max(monomials))+1)
            pol_a = _np.zeros(int(max(monomials))+1)
            pol_b[monomials] = qf_modelC[i,3:]
            q = quadrupole(fam_name, qf_modelC[i,1], 0)
            q.polynom_b=pol_b
            q.polynom_a=pol_a
            qf.append(q)
        else:
            raise Exception("Quadrupole type not recognized.")

    model_length = 2*sum(qf_modelC[:,1])
    mqf  = marker('mQF')
    qf   = [qf, mqf, qf]
    return (qf, model_length)
