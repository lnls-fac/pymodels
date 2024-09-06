from pymodels import si
from pymodels.SI_V25_04.lattice import get_optics_mode
# import numpy as np
# import pyaccel as pa
# from pymodels.SI_V25_04.segmented_models import dipole_b1, dipole_b2, dipole_bc


acc = si.create_accelerator()
fam = si.families.get_family_data(acc)
strengs = get_optics_mode()

use_rbend = True # Define dipoles as RBEND instead of SBEND
if use_rbend:
    bendtype = "RBEND"
else:
    bendtype = "SBEND"

stri = """!!! SIRIUS Storage Ring Model
! Date: 06-September-2024
! Version: SI_V25_04

!!! -- INITIAL PARAMETERS --

ACCLEN := 0;!
circum_new := 518.3899; ! [m]
circum_old := 518.3960; ! [m]
dcircum := circum_new - circum_old;
dcircum_frac := dcircum/20.0/2.0; ! divide circumference difference in all 20 straight sections

!!! -- INJECTION SECTOR --

L500p: DRIFT, L=0.500 + dcircum_frac;
LKKp: DRIFT, L=1.9150 + dcircum_frac;
LPMU: DRIFT, L=0.0600;
L050: DRIFT, L=0.050;
L150: DRIFT, L=0.150;
L182: DRIFT, L=0.182;
L399: DRIFT, L=0.399;

M_START : MARKER, L=0;  ! start of the model
M_END : MARKER, L=0;  ! end of the model
MIA : MARKER, L=0;  ! center of long straight sections (even-numbered)
InjVCb : MARKER, L=0;  ! Bigger injection vaccum chamber limits
InjVCs : MARKER, L=0;  ! Smaller injection vchamber limits
SVVC : MARKER, L=0;  ! VScrap vchamber limits (drawing: len = 398 mm)
ScrapV : MARKER, L=0;  ! vertical scraper

!* -- PULSED MAGNETS --
InjDpKckr : SEXTUPOLE, L=0.400, K2=0.0;  ! injection kicker
InjNLKckr : SEXTUPOLE, L=0.450, K2=0.0;  ! pulsed multipole magnet

!* DPK :
INJ_SEC_DPK : LINE=(
    InjVCb, L399, InjVCb, InjVCs, L182, L500p, M_END,
    M_START, MIA, LKKp,
    );!

!* DPK_END:
INJ_SEC_DPK_END : LINE=(
    InjVCb, L399, InjVCb, InjVCs, L182, L500p, M_END,
    M_START, MIA, LKKp, InjDpKckr,
    );!

!* NLK:
INJ_SEC_NLK : LINE=(
    InjVCb, L399, InjVCb, InjVCs, L182, L500p, M_END,
    M_START, MIA, LKKp, InjDpKckr, InjVCs,
    SVVC, LPMU, L050, ScrapV, L150, SVVC,
    );!

!* NLK_END :
INJ_SEC_NLK_END : LINE=(
    InjVCb, L399, InjVCb, InjVCs, L182, L500p, M_END,
    M_START, MIA, LKKp, InjDpKckr, InjVCs,
    SVVC, LPMU, L050, ScrapV, L150, SVVC,
    InjNLKckr);!

!* INJECTION SECTOR SELECTION : NLK_END
SI_INJ : LINE=(INJ_SEC_NLK_END);

!!! -- DRIFTS --

LIA : DRIFT, L=1.5179;
LIB : DRIFT, L=1.0879;
LIP : DRIFT, L=1.0879;
LPMD : DRIFT, L=0.4929;
LID3 : DRIFT, L=1.8679;
L144p : DRIFT, L=0.144 + dcircum_frac;
L208p : DRIFT, L=0.208 + dcircum_frac;
L350p : DRIFT, L=0.350 + dcircum_frac;
L600p : DRIFT, L=0.600 + dcircum_frac;
L800p : DRIFT, L=0.7999;
L011 : DRIFT, L=0.011;
L019 : DRIFT, L=0.019;
L049 : DRIFT, L=0.049;
L050 : DRIFT, L=0.050;
L052 : DRIFT, L=0.052;
L056 : DRIFT, L=0.056;
L063 : DRIFT, L=0.063;
L074 : DRIFT, L=0.074;
L075 : DRIFT, L=0.075;
L082 : DRIFT, L=0.082;
L090 : DRIFT, L=0.090;
L100 : DRIFT, L=0.100;
L109 : DRIFT, L=0.109;
L112 : DRIFT, L=0.112;
L119 : DRIFT, L=0.119;
L120 : DRIFT, L=0.120;
L125 : DRIFT, L=0.125;
L127 : DRIFT, L=0.127;
L133 : DRIFT, L=0.133;
L134 : DRIFT, L=0.134;
L135 : DRIFT, L=0.135;
L140 : DRIFT, L=0.140;
L150 : DRIFT, L=0.150;
L156 : DRIFT, L=0.156;
L170 : DRIFT, L=0.170;
L188 : DRIFT, L=0.188;
L200 : DRIFT, L=0.200;
L201 : DRIFT, L=0.201;
L203 : DRIFT, L=0.203;
L205 : DRIFT, L=0.205;
L216 : DRIFT, L=0.216;
L230 : DRIFT, L=0.230;
L237 : DRIFT, L=0.237;
L240 : DRIFT, L=0.240;
L260 : DRIFT, L=0.260;
L270 : DRIFT, L=0.270;
L297 : DRIFT, L=0.297;
L325 : DRIFT, L=0.325;
L329 : DRIFT, L=0.329;
L336 : DRIFT, L=0.336;
L365 : DRIFT, L=0.365;
L419 : DRIFT, L=0.419;
L474 : DRIFT, L=0.474;
L500 : DRIFT, L=0.500;
L511 : DRIFT, L=0.511;
L665 : DRIFT, L=0.665;
L715 : DRIFT, L=0.715;
L839 : DRIFT, L=0.839;

"""

st = f"""!!! -- DIPOLES --

DIPOLES_K0_on := 0;
DIPOLES_K1_on := 1;
DIPOLES_K2_on := 1;
DIPOLES_K3_on := 1;
"""

if use_rbend:
    st += "\nOPTION, RBARC = FALSE;\n"

# print(st)
stri += st + '\n'

# print("!* BC")
stri += "!* BC\n"
monomials = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10]
segmodel = [
    #         len[m]  angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)   PolyB(n=7)   PolyB(n=8)   PolyB(n=10)
    ['BC', 0.00100, 0.01877, -1.4741e-05, -3.2459e-03, -2.5934e+01, +2.2655e+02, -4.2041e+05, -1.9362e+06, -8.8515e+08, +1.8066e+10, -4.1927e+13, +1.8535e+17],
    ['BC', 0.00400, 0.07328, -3.5868e-06, -8.0872e-03, -2.3947e+01, +1.9896e+02, -3.8312e+05, -1.5555e+06, -8.7538e+08, +1.5588e+10, -3.4411e+13, +1.5036e+17],
    ['BC', 0.00500, 0.08149, -1.5878e-06, -2.2156e-02, -1.6636e+01, +9.5225e+01, -2.4803e+05, -2.8667e+05, -6.2015e+08, +5.9788e+09, -1.1795e+13, +5.3967e+16],
    ['BC', 0.00500, 0.06914, -2.2515e-06, -2.6794e-02, -9.9744e+00, +4.0910e+01, -1.2934e+05, -1.8459e+04, +6.5912e+06, +1.8432e+09, -3.7282e+12, +1.5831e+16],
    ['BC', 0.00500, 0.05972, +2.4800e-07, -2.6704e-02, -7.1238e+00, +2.8365e+01, -7.1836e+04, -1.7947e+05, +2.5073e+08, +1.9029e+09, -3.3936e+12, +1.2829e+16],
    ['BC', 0.01000, 0.09814, -7.2919e-07, -2.5788e-02, -5.4243e+00, +1.8297e+01, -3.6399e+04, -1.8928e+05, +2.7961e+08, +1.5270e+09, -3.1054e+12, +1.1735e+16],
    ['BC', 0.01000, 0.07568, -1.8658e-06, -2.4549e-02, -3.7961e+00, +7.9939e+00, -1.8270e+04, -9.0518e+04, +2.3235e+08, +8.1040e+08, -2.4656e+12, +9.3410e+15],
    ['BC', 0.01000, 0.05755, -6.9437e-07, -1.9501e-02, -2.2458e+00, +2.9742e+00, -1.0525e+04, -1.8749e+04, +1.6339e+08, +2.9806e+08, -1.6673e+12, +6.2159e+15],
    ['BC', 0.01000, 0.04544, -1.2861e-07, -1.2764e-03, -8.7276e-01, -4.5371e-01, -5.5830e+03, +2.6585e+04, +9.6483e+07, +1.2858e+06, -1.0053e+12, +3.9069e+15],
    ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['BC', 0.03200, 0.11887, -3.6974e-08, +1.2757e-02, +1.1825e+00, +1.8453e+00, -4.6262e+03, +2.4200e+04, +7.3751e+07, -6.3579e+07, -7.8054e+11, +3.0544e+15],
    ['BC', 0.03200, 0.09720, -9.0591e-07, -1.2063e-01, +5.2835e-01, +1.0917e+01, -3.2323e+03, -1.8683e+03, +4.9009e+07, -4.9946e+07, -4.6379e+11, +1.7988e+15],
    ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['BC', 0.16000, 0.62161, -1.1668e-06, -8.9725e-01, +4.4207e-01, +3.2247e+01, +1.9416e+03, -2.8567e+05, -5.0265e+07, +1.4028e+09, +6.1042e+11, -2.5574e+15],
    ['BC', 0.16000, 0.62274, +2.8034e-07, -9.0717e-01, +2.0879e-01, -6.2815e-01, +1.9822e+03, +2.4218e+05, -4.1507e+07, -1.1837e+09, +4.3276e+11, -1.5769e+15],
    ['BC', 0.01200, 0.04249, +5.4796e-07, -8.8611e-01, +4.9910e-01, +2.4958e+01, -9.4206e+03, -1.6025e+05, +1.8960e+08, +8.8432e+08, -1.6666e+12, +5.5453e+15],
    ['BC_EDGE', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['BC', 0.01400, 0.03339, -4.4895e-07, -4.4684e-01, -1.8750e+00, +2.2077e+01, -5.5912e+03, -1.6748e+05, +1.0327e+08, +9.3221e+08, -8.6332e+11, +2.7550e+15],
    ['BC', 0.01600, 0.01935, +7.1551e-07, -1.1215e-01, -1.9597e+00, +1.3313e+01, -3.5424e+03, -1.6337e+05, +6.3653e+07, +8.9179e+08, -5.4044e+11, +1.7393e+15],
    ['BC', 0.03500, 0.01344, -1.7487e-07, -1.9828e-02, -1.2534e+00, +1.9342e+01, +2.8084e+03, -2.9546e+05, -5.0640e+07, +1.4694e+09, +4.0940e+11, -1.2172e+15]
]
bcp   = 0
def bcpstr(segm, cc):
    st = f"BC.p{cc} : {bendtype}, L={segm[1]:.5f}, ANGLE={seg[2]:.5f}*PI/180, "
    st += f"K0:={seg[3]:+.4e}*BC_K0_on, "
    st += f"K1:={seg[4]:+.4e}*BC_K1_on, "
    st += f"K2:={seg[5]:+.4e}*BC_K2_on, "
    st += f"K3:={seg[6]:+.4e}*BC_K3_on;"
    return st
st = "BC_K0_on := 1*DIPOLES_K0_on;\n" +\
"BC_K1_on := 1*DIPOLES_K1_on;\n" +\
"BC_K2_on := 1*DIPOLES_K2_on;\n" +\
"BC_K3_on := 1*DIPOLES_K3_on;"
# print(st)
stri += st + '\n'
tst = "BC.halfseg : LINE=("
for i,seg in enumerate(segmodel):
    md = seg[0]
    if md == 'BC':
        bcp += 1
        st = bcpstr(seg, bcp)
        tst += st[:6].replace(" ", "")
        # print(st)
        stri += st + "\n"
    elif md == 'm_accep':
        st = f"BC.M_ACCEP"
        tst += st
    elif md == 'BC_EDGE':
        st = f"BC.EDGE"
        tst += st
    tst += ', '
st = "BC.M_ACCEP : MARKER, L=0;\n" +\
f"BC.EDGE : MARKER, L=0;\n" +\
f"BC.MC : MARKER, L=0;"
# print(st)
stri += st + '\n'
tst = tst[:-2]
tst += ");"
# print(tst)
stri += tst + "\n"
st = f"BC : LINE=(-BC.halfseg, BC.MC, BC.M_ACCEP, BC.halfseg);\n"
# print(st)
stri += st + '\n'
# print("!* B1")
stri += "!* B1\n"
monomials = [0, 1, 2, 3, 4, 5, 6]
segmodel = [
    # type     len[m]   angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
    ['B1', 0.00200, 0.00633, -1.9696e-06, -7.2541e-01, -5.4213e-01, +5.4347e+00, +2.5091e+02, +4.9772e+02, -1.9113e+06],
    ['B1', 0.00300, 0.00951, -3.8061e-06, -7.2968e-01, -4.5292e-01, +4.3822e+00, +3.1863e+02, +1.5282e+03, -2.3387e+06],
    ['B1', 0.00500, 0.01592, -4.7568e-07, -7.4227e-01, -2.1669e-01, +2.9544e+00, +2.9316e+02, +1.4632e+03, -2.0877e+06],
    ['B1', 0.00500, 0.01603, -1.9480e-06, -7.5771e-01, -1.0657e-02, +3.5007e+00, +2.9571e+02, -1.7742e+03, -2.0010e+06],
    ['B1', 0.00500, 0.01611, -2.7633e-06, -7.6662e-01, +3.3285e-02, +4.7919e+00, +3.3381e+02, -3.3109e+03, -2.0402e+06],
    ['B1', 0.01000, 0.03236, -1.9098e-06, -7.7081e-01, +1.6451e-02, +5.3028e+00, +3.7119e+02, -4.8877e+03, -2.0590e+06],
    ['B1', 0.04000, 0.12963, -1.6309e-06, -7.7247e-01, +4.8673e-02, +4.6505e+00, +3.3306e+02, -2.1646e+03, -1.5868e+06],
    ['B1', 0.15000, 0.48382, -1.9888e-06, -7.7332e-01, +9.7601e-02, +5.3336e+00, +2.5126e+02, +8.0649e+02, -9.2335e+05],
    ['B1', 0.10000, 0.32247, -2.1025e-06, -7.7271e-01, +1.1969e-01, +5.6811e+00, +2.1496e+02, +5.2023e+03, -6.0518e+05],
    ['B1', 0.05000, 0.16165, -2.1257e-06, -7.7203e-01, +5.6224e-02, +4.5293e+00, +6.3908e+01, +6.1651e+03, +3.4951e+05],
    ['B1', 0.03400, 0.10509, -1.8623e-06, -7.7144e-01, -1.2160e-01, +9.1976e+00, -5.3231e+01, +9.0360e+03, +7.2783e+05],
    ['B1_EDGE', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['B1', 0.01600, 0.03414, -9.6169e-07, -4.5231e-01, -1.8149e+00, +1.9400e+01, -2.2843e+02, +1.6525e+04, -4.0477e+04],
    ['B1', 0.04000, 0.03296, -5.2504e-07, -8.6643e-02, -1.7536e+00, +8.5147e+00, -5.8350e+01, +4.2954e+03, -3.7834e+04],
    ['B1', 0.04000, 0.00774, -1.6259e-07, -8.3065e-03, -3.8990e-01, +1.3183e+00, +2.5814e+01, +3.1642e+02, -5.0464e+04],
    ['B1', 0.05000, 0.00389, -7.9445e-08, -1.0742e-03, -9.8271e-02, +5.0359e-02, -1.0312e+01, +9.0013e+02, +8.2477e+04],
    ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
b1p   = 0
def b1pstr(segm, cc):
    st = f"B1.p{cc} : {bendtype}, L={segm[1]:.5f}, ANGLE={seg[2]:.5f}*PI/180, "
    st += f"K0:={seg[3]:+.4e}*B1_K0_on, "
    st += f"K1:={seg[4]:+.4e}*B1_K1_on, "
    st += f"K2:={seg[5]:+.4e}*B1_K2_on, "
    st += f"K3:={seg[6]:+.4e}*B1_K3_on;"
    return st
st = "B1_K0_on := 1*DIPOLES_K0_on;\n" +\
"B1_K1_on := 1*DIPOLES_K1_on;\n" +\
"B1_K2_on := 1*DIPOLES_K2_on;\n" +\
"B1_K3_on := 1*DIPOLES_K3_on;"
# print(st)
stri += st + '\n'
hseg = "B1.halfseg.2 : LINE=("
ihsegst = "B1.halfseg.1 : LINE=("
ihseg = []
for i,seg in enumerate(segmodel):
    md = seg[0]
    if md == 'B1':
        b1p += 1
        st = b1pstr(seg, b1p)
        hseg += st[:6].replace(" ", "")
        ihseg += [st[:6].replace(" ", "")]
        # print(st)
        stri += st + '\n'
    elif md == 'm_accep':
        st = f"B1.M_ACCEP"
        hseg += st
        ihseg += [st]
    elif md == 'B1_EDGE':
        st = f"B1.EDGE"
        hseg += st
        ihseg += [st]
    hseg += ', '
st = "B1.M_ACCEP : MARKER, L=0;\n" +\
"B1.EDGE : MARKER, L=0;\n" +\
"B1_SRC : MARKER, L=0;\n" +\
"B1.MB1 : MARKER, L=0;"
# print(st)
stri += st + '\n'

hseg = hseg[:-2]
hseg += ");"
ihseg = ihseg[::-1]
ihseg.insert(7, "B1_SRC")
ihseg = ihsegst + ", ".join(ihseg) + ");"

# print(ihseg)
stri += ihseg + '\n'
# print(hseg)
stri += hseg + '\n'

st = "B1 : LINE=(B1.halfseg.1, B1.MB1, B1.M_ACCEP, B1.halfseg.2);"
# print(st)
stri += st + '\n\n'
# print("!* B2")
stri += "!* B2\n"

monomials = [0, 1, 2, 3, 4, 5, 6]
segmodel = [
    #type     len[m]   angle[deg]  PolyB(n=0)   PolyB(n=1)   PolyB(n=2)   PolyB(n=3)   PolyB(n=4)   PolyB(n=5)   PolyB(n=6)
    ['B2', 0.12500, 0.40623, +2.8141e-07, -7.7535e-01, +3.8504e-02, +1.7048e+00, -2.6809e+02, +8.8090e+03, +1.8541e+06],
    ['B2', 0.05500, 0.17963, +2.4869e-07, -7.7400e-01, +1.8903e-02, +1.3538e+00, -2.7871e+02, +8.4667e+03, +1.7913e+06],
    ['B2', 0.01000, 0.03260, -1.4532e-07, -7.6990e-01, -7.3993e-03, +1.4325e+00, -3.7053e+02, +9.0098e+03, +1.8818e+06],
    ['B2', 0.00500, 0.01624, -9.6976e-07, -7.6272e-01, -4.4905e-02, +3.7505e-01, -4.0759e+02, +1.0527e+04, +1.8729e+06],
    ['B2', 0.00500, 0.01619, -8.5112e-08, -7.5413e-01, -1.7000e-01, +1.3254e-01, -4.2095e+02, +1.2650e+04, +1.8762e+06],
    ['B2', 0.00500, 0.01616, +5.0825e-07, -7.4866e-01, -2.8166e-01, +7.1392e-01, -3.5386e+02, +1.3287e+04, +1.5160e+06],
    ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['B2', 0.00500, 0.01618, +1.7001e-06, -7.5218e-01, -2.1312e-01, +3.8486e-01, -3.9031e+02, +1.2889e+04, +1.7072e+06],
    ['B2', 0.01000, 0.03254, +1.3585e-06, -7.6428e-01, -4.1565e-02, +6.7680e-01, -4.0577e+02, +1.0602e+04, +1.8735e+06],
    ['B2', 0.01000, 0.03269, +2.9027e-07, -7.7165e-01, -8.0002e-03, +1.7812e+00, -3.2568e+02, +8.2067e+03, +1.7365e+06],
    ['B2', 0.17500, 0.57073, -1.1637e-07, -7.7428e-01, +6.8988e-02, +4.1024e+00, -5.1871e+01, +7.5752e+02, +5.9943e+05],
    ['B2', 0.17500, 0.57034, -3.3225e-07, -7.7352e-01, +7.8447e-02, +5.4514e+00, +1.9975e+02, +3.3621e+03, -3.1314e+05],
    ['B2', 0.02000, 0.06315, +2.2577e-08, -7.8534e-01, -1.4538e-01, +9.2976e+00, -1.5715e+02, +1.2311e+04, +1.1408e+06],
    ['B2', 0.01000, 0.02719, +8.7645e-08, -6.7626e-01, -3.1354e-01, +1.6050e+01, -3.9938e+02, +1.6288e+04, +8.1085e+05],
    ['B2_EDGE', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['B2', 0.01500, 0.02866, +6.3204e-08, -3.6034e-01, -2.3415e+00, +2.0402e+01, -3.9166e+02, +1.9055e+04, +3.1586e+05],
    ['B2', 0.02000, 0.01994, +5.4460e-07, -1.0711e-01, -2.1654e+00, +1.1296e+01, -1.7816e+02, +7.2357e+03, +1.6786e+05],
    ['B2', 0.03000, 0.01188, +1.3393e-07, -2.3886e-02, -8.9207e-01, +3.8284e+00, -1.5146e+01, +5.3693e+02, +7.8230e+04],
    ['B2', 0.03200, 0.00444, -2.8999e-07, -4.5556e-03, -2.6166e-01, +7.8754e-01, +1.5573e+00, +8.3579e+01, +3.8831e+04],
    ['B2', 0.03250, 0.00341, -1.3468e-07, -1.2481e-03, -1.3069e-01, +3.6679e-01, +1.3671e+01, -7.7370e+02, -2.9544e+04],
    ['m_accep', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
b2p   = 0
maccp = 0
def b2pstr(segm, cc):
    st = f"B2.p{cc} : {bendtype}, L={segm[1]:.5f}, ANGLE={seg[2]:.5f}*PI/180, "
    st += f"K0:={seg[3]:+.4e}*B2_K0_on, "
    st += f"K1:={seg[4]:+.4e}*B2_K1_on, "
    st += f"K2:={seg[5]:+.4e}*B2_K2_on, "
    st += f"K3:={seg[6]:+.4e}*B2_K3_on;"
    return st
st = "B2_K0_on := 1*DIPOLES_K0_on;\n" +\
"B2_K1_on := 1*DIPOLES_K1_on;\n" +\
"B2_K2_on := 1*DIPOLES_K2_on;\n" +\
"B2_K3_on := 1*DIPOLES_K3_on;"
# print(st)
stri += st + '\n'
tst = "B2.halfseg : LINE=("
for i,seg in enumerate(segmodel):
    md = seg[0]
    if md == 'B2':
        b2p += 1
        st = b2pstr(seg, b2p)
        tst += st[:6].replace(" ", "")
        # print(st)
        stri += st + '\n'
    elif md == 'm_accep':
        maccp += 1
        st = f"B2.M_ACCEP"
        tst += st
    elif md == 'B2_EDGE':
        st = f"B2.EDGE"
        tst += st
    tst += ', '
st = "B2.M_ACCEP : MARKER, L=0;\n" +\
"B2.EDGE : MARKER, L=0;\n" +\
"B2.MB2 : MARKER, L=0;"
# print(st)
stri += st + '\n'
tst = tst[:-2]
tst += ");"
# print(tst)
stri += tst + '\n'
st = "B2 : LINE=(-B2.halfseg, B2.MB2, B2.M_ACCEP, B2.halfseg);\n"
# print(st)
stri += st + '\n'
from pymodels.SI_V25_04.segmented_models import quadrupole_q14, quadrupole_q20, quadrupole_q30
ff={

"Q1":   (quadrupole_q20, 20),
"Q2":   (quadrupole_q20, 20),
"Q3":   (quadrupole_q20, 20),
"Q4":   (quadrupole_q20, 20),
"QFA":  (quadrupole_q20, 20),
"QDA":  (quadrupole_q14, 14),
"QDB1": (quadrupole_q14, 14),
"QDB2": (quadrupole_q14, 14),
"QDP1": (quadrupole_q14, 14),
"QDP2": (quadrupole_q14, 14),
"QFB":  (quadrupole_q30, 30),
"QFP":  (quadrupole_q30, 30),

}
strq14 = """!* Q14
Q14.pB.1 = -4.06e+00;
Q14.pB.5 = +6.38e+04;
Q14.pB.9 = -1.45e+13;
Q14.pB.13 = +2.90e+20;

"""
strq20 = """!* Q20
Q20.pB.1 = -4.74e+00;
Q20.pB.5 = +8.41e+04;
Q20.pB.9 = -1.83e+13;
Q20.pB.13 = +3.47e+20;

"""
strq30 = """!* Q30
Q30.pB.1 = -4.75e+00;
Q30.pB.5 = +1.06e+05;
Q30.pB.9 = -1.95e+13;
Q30.pB.13 = +3.56e+20;

"""
flagq20 = True
flagq14 = True
flagq30 = True
def addquadstring(num):
    global flagq14
    global flagq20
    global flagq30
    global stri
    if num == 14 and flagq14:
        # print(strq14)
        stri += strq14
        flagq14 = False
    elif num == 20 and flagq20:
        # print(strq20)
        flagq20 = False
        stri += strq20
    elif num == 30 and flagq30:
        # print(strq30)
        flagq30 = False
        stri += strq30
    return
# print("!!! -- QUADRUPOLES --\n")
stri += "!!! -- QUADRUPOLES --\n\n"
for t in ff.keys():
    func, num = ff[t]
    b = func(t, strengs[t])
    addquadstring(num)
    for j, e in enumerate(b):
        # kn = ", ".join([f"K{i}={k:1.2e}"  if (i!=1) else f"K{i}:=STREN.{t}" for i,k in enumerate(e.polynom_b)])
        kn = f"K1:=STREN.{t}"
        kn += f";!, K5:=Q{num}.pB.5*RESCALE.{t}"
        kn += f", K9:=Q{num}.pB.9*RESCALE.{t}"
        kn += f", K13:=Q{num}.pB.13*RESCALE.{t}"
        l = e.length
        # print(f"STREN.{t} := {e.polynom_b[1]};")
        # print(f"RESCALE.{t} := STREN.{t} / Q{num}.pB.1;")
        # print(f"{t} : QUADRUPOLE, L={l:.4f}, {kn};\n")
        stri += f"STREN.{t} := {e.polynom_b[1]};\n" + \
            f"RESCALE.{t} := STREN.{t} / Q{num}.pB.1;\n" + \
            f"{t} : QUADRUPOLE, L={l:.4f}, {kn};\n\n"
# # print('!!! -- SEXTUPOLES --\n')
stri += """!!! -- SEXTUPOLES --

SEXTUPOLES_on := 1;

"""
for key in strengs.keys():
    if key.startswith('S'):
        st = strengs[key]
        pol='+1'
        if st<0:
            pol='-1'
        # # print(f"STREN.{key} := {st};")
        # # print(f"{key} : SEXTUPOLE, L=0.150, K2:=STREN.{key};\n")
        stri += f"STREN.{key} := {st};\n" +\
            f"{key}_on := 1*SEXTUPOLES_on;\n" +\
            f"{key} : SEXTUPOLE, L=0.150, K2:=STREN.{key}*{key}_on;\n\n"
stri += """!!! -- slow vertical corrector --
CV : SEXTUPOLE, L=0.150, K2=0.0;  ! same model as BO correctors

!!! -- pulsed magnets --
PingV : SEXTUPOLE, L=0.32, K2=0.0;  ! Vertical Pinger

!!! -- fast correctors --
! 60 magnets: normal quad poles (CH+CV and CH+CV+QS):
FC1 : SEXTUPOLE, L=0.084, K2=0.0;
FC1FF : SEXTUPOLE, L=0.084, K2=0.0;  ! feedforward
! 20 magnets: skew quad poles (CH+CV and CH+CV+QS):
FC2 : SEXTUPOLE, L=0.082, K2=0.0;

!!! -- rf cavities --
HARMONIC_NUMBER = 864;
RF_VOLT := 3.0; ! [MV]
SRFCav : RFCAVITY, L=0, VOLT:=RF_VOLT, HARMON:=HARMONIC_NUMBER;
H3Cav : MARKER, L=0; !

!!! -- lattice markers --
MIB : MARKER, L=0; !  # center of short straight sections (odd-numbered)
MIP : MARKER, L=0; !  # center of short straight sections (odd-numbered)
!# marker used to delimitate girders.
!# one marker at begin and another at end of girder:
GIR : MARKER, L=0; !
!# marker for the extremities of IDs in long straight sections
MIDA : MARKER, L=0; !
!# marker for the extremities of IDs in short straight sections
MIDB : MARKER, L=0; !
!# marker for the extremities of IDs in short straight sections
MIDP : MARKER, L=0; !
!# end of injection septum
InjSeptF : MARKER, L=0; !

!!! --- diagnostic components ---
BPM : MONITOR; !
IDBPM : MONITOR; !
DCCT : MARKER, L=0; !  # dcct to measure beam current
ScrapH : MARKER, L=0; ! # horizontal scraper
GSL15 : MARKER, L=0; !  # Generic Stripline (lambda/4)
GSL07 : MARKER, L=0; !  # Generic Stripline (lambda/8)
GBPM : MONITOR; !  # General BPM
BbBPkup : MARKER, L=0; !  # Bunch-by-Bunch Pickup
BbBKckrH  : MARKER, L=0; !  # Horizontal Bunch-by-Bunch Shaker
BbBKckrV : MARKER, L=0; !  # Vertical Bunch-by-Bunch Shaker
BbBKckL : MARKER, L=0; !  # Longitudinal Bunch-by-Bunch Shaker
TuneShkrH : MARKER, L=0; !  # Horizontal Tune Shaker
TuneShkrV : MARKER, L=0; !  # Vertical Tune Shaker
TunePkupH : MARKER, L=0; !  # Horizontal Tune Pickup
TunePkupV : MARKER, L=0; !  # Vertical Tune Pickup
SHVC : MARKER, L=0; !  # HScrap vchamber limits (drawing: len = 313 mm)

!!! --- insertion devices (half devices) ---
IDLEN.APU22 := 1.3;
IDLEN.IVU18 := 2.0;
IDLEN.DELTA52 := 1.2;
IDLEN.APU58 := 1.3;
IDLEN.WIG180 := 2.654;
IDLEN.PAPU50 := 0.984;

!* CARNAUBA
ID06Hu : DRIFT, L:=IDLEN.APU22/2;
ID06Hd : DRIFT, L:=IDLEN.APU22/2;

!* CATERETE
ID07Hu : DRIFT, L:=IDLEN.APU22/2;
ID07Hd : DRIFT, L:=IDLEN.APU22/2;

!* EMA
ID08Hu : DRIFT, L:=IDLEN.IVU18/2;
ID08Hd : DRIFT, L:=IDLEN.IVU18/2;

!* MANACA
ID09Hu : DRIFT, L:=IDLEN.APU22/2;
ID09Hd : DRIFT, L:=IDLEN.APU22/2;

!* SABIA
ID10Hu : DRIFT, L:=IDLEN.DELTA52/2;
ID10Hd : DRIFT, L:=IDLEN.DELTA52/2;

!* IPE
ID11Hu : DRIFT, L:=IDLEN.APU58/2;
ID11Hd : DRIFT, L:=IDLEN.APU58/2;

!* PAINEIRA
ID14Hu : DRIFT, L:=IDLEN.WIG180/2;
ID14Hd : DRIFT, L:=IDLEN.WIG180/2;

!* SAPUCAIA
ID17Hu : DRIFT, L:=IDLEN.PAPU50/2;
ID17Hd : DRIFT, L:=IDLEN.PAPU50/2;

IDC1 : SEXTUPOLE, L=0.100, K2=0.0; ! # ID corrector
IDC2 : SEXTUPOLE, L=0.084, K2=0.0; ! # ID corrector used in PAPU50
IDC3 : SEXTUPOLE, L=0.100, K2=0.0; ! # ID corrector (only IDCH)
IDQS : SEXTUPOLE, L=0.200, K2=0.0; ! # ID quadskew corrector

!!! -- sectors --
M1A : LINE=(L134, QDA, L150, SDA0, GIR, L074, GIR, FC1, L082, QFA, L150, SFA0, L135, BPM, GIR);!  # high beta xxM1 girder (with fast corrector)
M1AFF : LINE=(
    L134, QDA, L150, SDA0, GIR, L074, GIR, FC1FF, L082, QFA, L150, SFA0,
    L135, BPM, GIR);!  # high beta xxM1 girder (with ff corrector)
M1B : LINE=(L134, QDB1, L150, SDB0, GIR, L240, GIR, QFB, L150, SFB0, L049, FC1, L052, QDB2, L140, BPM, GIR);!  # low beta xxM1 girder
M1P : LINE=(L134, QDP1, L150, SDP0, GIR, L240, GIR, QFP, L150, SFP0, L049, FC1, L052, QDP2, L140, BPM, GIR);!  # low beta xxM1 girder
M2A : LINE=(-M1A);!  # high beta xxM2 girder (with fast correctors)
M2AFF : LINE=(-M1AFF);!  # high beta xxM2 girder (with ff correctors)
M2B : LINE=(-M1B);!  # low beta xxM2 girder
M2P : LINE=(-M1P);!  # low beta xxM2 girder

M2B_BbBPkup : LINE=(GIR, BPM, L140, QDB2, L052, FC1, L049, SFB0, L150, QFB, GIR, L120, BbBPkup, L120, GIR, SDB0, L150, QDB1, L134);!

! arc sector in between B1-B2 (high beta odd-numbered straight sections):
C1A : LINE=(GIR, L474, GIR, SDA1, L170, Q1, L135, BPM, L125, SFA1, L230, Q2, L170, SDA2, GIR, L205, GIR, BPM, L011);!

! arc sector in between B1-B2 (low beta  even-numbered straight sections):
C1B : LINE=(GIR, L474, GIR, SDB1, L170, Q1, L135, BPM, L125, SFB1, L230, Q2, L170, SDB2, GIR, L205, GIR, BPM, L011);!

! arc sector in between B1-B2 (low beta even-numbered straight sections):
C1P : LINE=(GIR, L474, GIR, SDP1, L170, Q1, L135, BPM, L125, SFP1, L230, Q2, L170, SDP2, GIR, L205, GIR, BPM, L011);!

! arc sector in between B2-BC (high beta odd-numbered straight sections):
C2A : LINE=(GIR, L336, GIR, SDA3, L170, Q3, L230, SFA2, L260, Q4, L200, CV, GIR, L201, GIR, FC2, L119, BPM, L075);!

! arc sector in between B2-BC (low beta even-numbered straight sections):
C2B : LINE=(GIR, L336, GIR, SDB3, L170, Q3, L230, SFB2, L260, Q4, L200, CV, GIR, L201, GIR, FC2, L119, BPM, L075);!

! arc sector in between B2-BC (low beta even-numbered straight sections):
C2P : LINE=(GIR, L336, GIR, SDP3, L170, Q3, L230, SFP2, L260, Q4, L200, CV, GIR, L201, GIR, FC2, L119, BPM, L075);!

! arc sector in between BC-B2 (high beta odd-numbered straight sections):
C3A : LINE=(GIR, L715, GIR, L112, Q4, L133, BPM, L127, SFA2, L056, FC1, L090, Q3, L170, SDA3, GIR, L325, GIR, BPM, L011);!

! arc sector in between BC-B2 (low beta even-numbered straight sections):
C3B : LINE=(GIR, L715, GIR, L112, Q4, L133, BPM, L127, SFB2, L056, FC1, L090, Q3, L170, SDB3, GIR, L325, GIR, BPM, L011);!

! arc sector in between BC-B2 (low beta even-numbered straight sections):
C3P : LINE=(GIR, L715, GIR, L112, Q4, L133, BPM, L127, SFP2, L056, FC1, L090, Q3, L170, SDP3, GIR, L325, GIR, BPM, L011);!

! arc sector in between B2-B1 (high beta odd-numbered straight sections):
C4A : LINE=(GIR, L216, GIR, SDA2, L170, Q2, L230, SFA1, L125, BPM, L135, Q1, L170, SDA1, GIR, L474, GIR);!

! arc sector in between B2-B1 (high beta odd-numbered straight sections):
C4A_BbBKckrV : LINE=(GIR, L216, GIR, SDA2, L170, Q2, L230, SFA1, L125, BPM, L135, Q1, L170, SDA1, L237, BbBKckrV, GIR, L237, GIR);!

! arc sector in between B2-B1 (low beta even-numbered straight sections):
C4B : LINE=(GIR, L216, GIR, SDB2, L170, Q2, L230, SFB1, L125, BPM, L135, Q1, L170, SDB1, GIR, L474, GIR);!

! arc sector in between B2-B1 (low beta even-numbered straight sections):
C4B_GBPM : LINE=(GIR, L216, GIR, SDB2, L170, Q2, L230, SFB1, L125, BPM, L135, Q1, L170, SDB1, GBPM, GIR, L474, GIR);!

! arc sector in between B2-B1 (low beta even-numbered straight sections):
C4B_DCCT : LINE=(GIR, L216, GIR, SDB2, L170, Q2, L230, SFB1, L125, BPM, L135, Q1, L170, SDB1, L237, DCCT, GIR, L237, GIR);!

! arc sector in between B2-B1 (low beta even-numbered straight sections):
C4B_TunePkupV : LINE=(GIR, L216, GIR, SDB2, L170, Q2, L230, SFB1, L125, BPM, L135, Q1, L170, SDB1, L237, TunePkupV, GIR, L237, GIR);!

! arc sector in between B2-B1 (low beta even-numbered straight sections)
C4B_PingV : LINE=(GIR, L216, GIR, SDB2, L170, Q2, L230, SFB1, L125, BPM, L135, Q1, L170, SDB1, L135, PingV, GIR, L019, GIR);!

! arc sector in between B2-B1 (low beta even-numbered straight sections):
C4P : LINE=(GIR, L216, GIR, SDP2, L170, Q2, L230, SFP1, L125, BPM, L135, Q1, L170, SDP1, GIR, L474, GIR);!

! arc sector in between B2-B1 (low beta even-numbered straight sections):
C4P_DCCT : LINE=(GIR, L216, GIR, SDP2, L170, Q2, L230, SFP1, L125, BPM, L135, Q1, L170, SDP1, L237, DCCT, GIR, L237, GIR);!

! arc sector in between B2-B1 (low beta even-numbered straight sections):
C4P_TuneShkrV : LINE=(GIR, L216, GIR, SDP2, L170, Q2, L230, SFP1, L125, BPM, L135, Q1, L170, SDP1, L237, TuneShkrV, GIR, L237, GIR);!

!! --- insertion sectors ---
IDA : LINE=(L500, LIA, L500, MIDA, L500, L500p, MIA, L500p, L500, MIDA, L500, LIA, L500);!  # high beta ID straight section

IDB : LINE=(L500, LIB, L500, MIDB, L500, L500p, MIB, L500p, L500, MIDB, L500, LIB, L500);!  # low beta ID straight section

IDP : LINE=(L500, LIP, L500, MIDP, L500, L500p, MIP, L500p, L500, MIDP, L500, LIP, L500);!  # low beta ID straight section

IDA_01_INJ : LINE=(SHVC, L156, ScrapH, L156, SHVC, L188, TuneShkrH, LIA, L419, InjSeptF, SI_INJ, LPMD);!  # high beta INJ straight section and Scrapers

IDB_02 : LINE=(L500, LIB, L500, MIDB, L500, L500p, MIB, L500p, L500, MIDB, L500, H3Cav, LIB, L500);!  # low beta ID straight section

IDP_03_CAV : LINE=(L500, LIP, L500, L500, L500p, MIP, SRFCav, L500p, L500, L500, LIP, L500);!  # low beta RF cavity straight section

IDB_04 : LINE=(IDB);

IDA_05 : LINE=(IDA);

IDB_06 : LINE=(L500, LIB, L500, L350p, MIDB, ID06Hu, MIB, ID06Hd, MIDB, L350p, L500, LIB, L500);!  # low beta ID straight section (CARNAUBA)

IDP_07 : LINE=(L500, LIP, L500, L350p, MIDP, ID07Hu, MIP, ID07Hd, MIDP, L350p, L500, LIP, L500);!  # low beta ID straight section (CATERETE)

IDB_08 : LINE=(L500, LIB, L150, L350p, MIDB, ID08Hu, MIB, ID08Hd, MIDB, L350p, L150, LIB, L500);!  # low beta ID straight section (EMA)

IDA_09 : LINE=(L500, LID3, L500p, MIDA, ID09Hu, MIA, ID09Hd, MIDA, L500p, LID3, L500);!  # high beta ID straight section (MANACA)

IDB_10 : LINE=(L839, L800p, IDQS, L270, IDBPM, L135, IDC1, L144p, MIDB, ID10Hu, MIB, ID10Hd, MIDB, L144p, IDC1, L135, IDBPM, L270, IDQS, L800p, L839);!  # low beta (SABIA)

IDP_11 : LINE=(L500, LIP, L500, L350p, MIDP, ID11Hu, MIP, ID11Hd, MIDP, L350p, L500, LIP, L500);!  # low beta ID straight section (IPE) L=1.3m

IDB_12 : LINE=(L500, LIB, L665, L100, L135, MIDB, L600p, MIB, L600p, MIDB, L135, L100, L665, LIB, L500);!  # low beta ID straight section

IDA_13 : LINE=(IDA);

IDB_14 : LINE=(L365, LIB, L208p, IDC3, MIDB, ID14Hu, MIB, ID14Hd, MIDB, IDC3, L208p, LIB, L365);!  # low beta ID straight section (PAINEIRA)

IDP_15 : LINE=(IDP);

IDB_16 : LINE=(L500, LIB, L500, MIDB, L500, L500p, MIB, L500p, L500, MIDB, L500, BbBKckL, LIB, L500);!  # low beta ID straight section

IDA_17 : LINE=(L500, LIA, L511, L350p, IDC2, L063, MIDA, ID17Hu, MIA, ID17Hd, MIDA, L063, IDC2, L350p, L511, BbBKckrH, LIA, L500);!  # high beta ID straight !# section (SAPUCAIA)

IDB_18_TUNEPKUPH : LINE=(L500, LIB, L500, MIDB, L500, L500p, MIB, L500p, L500, MIDB, L500, TunePkupH, LIB, L500);!  # low beta ID straight section

IDB_19_GSL15 : LINE=(L500, GSL15, LIP, L500, MIDP, L500, L500p, MIP, L500p, L500, MIDP, L500, LIP, L500);!  # low beta ID straight section

IDB_20_GSL07 : LINE=(L500, GSL07, LIB, L500, MIDB, L500, L500p, MIB, L500p, L500, MIDB, L500, LIB, L500);!  # low beta ID straight section

!!! -- girders --

!!! straight sections
SS_S01 : LINE=(IDA_01_INJ);!  # INJECTION
SS_S02 : LINE=(IDB_02);!
SS_S03 : LINE=(IDP_03_CAV);!
SS_S04 : LINE=(IDB_04);!
SS_S05 : LINE=(IDA_05);!
SS_S06 : LINE=(IDB_06);!  # CARNAUBA
SS_S07 : LINE=(IDP_07);!  # CATERETE
SS_S08 : LINE=(IDB_08);!  # EMA
SS_S09 : LINE=(IDA_09);!  # MANACA
SS_S10 : LINE=(IDB_10);!  # SABIA
SS_S11 : LINE=(IDP_11);!  # IPE
SS_S12 : LINE=(IDB_12);!
SS_S13 : LINE=(IDA_13);!
SS_S14 : LINE=(IDB_14);!  # PAINEIRA
SS_S15 : LINE=(IDP_15);!
SS_S16 : LINE=(IDB_16);!  # INGA
SS_S17 : LINE=(IDA_17);!  # SAPUCAIA
SS_S18 : LINE=(IDB_18_TUNEPKUPH);!
SS_S19 : LINE=(IDB_19_GSL15);!
SS_S20 : LINE=(IDB_20_GSL07);!

!!! down and upstream straight sections
M1_S01 : LINE=(M1AFF);!
M2_S01 : LINE=(M2AFF);!
M1_S02 : LINE=(M1B);!
M2_S02 : LINE=(M2B);!
M1_S03 : LINE=(M1P);!
M2_S03 : LINE=(M2P);!
M1_S04 : LINE=(M1B);!
M2_S04 : LINE=(M2B);!
M1_S05 : LINE=(M1A);!
M2_S05 : LINE=(M2A);!
M1_S06 : LINE=(M1B);!
M2_S06 : LINE=(M2B);!
M1_S07 : LINE=(M1P);!
M2_S07 : LINE=(M2P);!
M1_S08 : LINE=(M1B);!
M2_S08 : LINE=(M2B);!
M1_S09 : LINE=(M1A);!
M2_S09 : LINE=(M2A);!
M1_S10 : LINE=(M1B);!
M2_S10 : LINE=(M2B);!
M1_S11 : LINE=(M1P);!
M2_S11 : LINE=(M2P);!
M1_S12 : LINE=(M1B);!
M2_S12 : LINE=(M2B);!
M1_S13 : LINE=(M1A);!
M2_S13 : LINE=(M2A);!
M1_S14 : LINE=(M1B);!
M2_S14 : LINE=(M2B);!
M1_S15 : LINE=(M1P);!
M2_S15 : LINE=(M2P);!
M1_S16 : LINE=(M1B);!
M2_S16 : LINE=(M2B_BbBPkup);!
M1_S17 : LINE=(M1A);!
M2_S17 : LINE=(M2A);!
M1_S18 : LINE=(M1B);!
M2_S18 : LINE=(M2B);!
M1_S19 : LINE=(M1P);!
M2_S19 : LINE=(M2P);!
M1_S20 : LINE=(M1B);!
M2_S20 : LINE=(M2B);!

!!! dispersive arcs
C1_S01 : LINE=(C1A);!
C2_S01 : LINE=(C2A);!
C3_S01 : LINE=(C3B);!
C4_S01 : LINE=(C4B);!
C1_S02 : LINE=(C1B);!
C2_S02 : LINE=(C2B);!
C3_S02 : LINE=(C3P);!
C4_S02 : LINE=(C4P);!
C1_S03 : LINE=(C1P);!
C2_S03 : LINE=(C2P);!
C3_S03 : LINE=(C3B);!
C4_S03 : LINE=(C4B);!
C1_S04 : LINE=(C1B);!
C2_S04 : LINE=(C2B);!
C3_S04 : LINE=(C3A);!
C4_S04 : LINE=(C4A);!
C1_S05 : LINE=(C1A);!
C2_S05 : LINE=(C2A);!
C3_S05 : LINE=(C3B);!
C4_S05 : LINE=(C4B);!
C1_S06 : LINE=(C1B);!
C2_S06 : LINE=(C2B);!
C3_S06 : LINE=(C3P);!
C4_S06 : LINE=(C4P);!
C1_S07 : LINE=(C1P);!
C2_S07 : LINE=(C2P);!
C3_S07 : LINE=(C3B);!
C4_S07 : LINE=(C4B);!
C1_S08 : LINE=(C1B);!
C2_S08 : LINE=(C2B);!
C3_S08 : LINE=(C3A);!
C4_S08 : LINE=(C4A);!
C1_S09 : LINE=(C1A);!
C2_S09 : LINE=(C2A);!
C3_S09 : LINE=(C3B);!
C4_S09 : LINE=(C4B);!
C1_S10 : LINE=(C1B);!
C2_S10 : LINE=(C2B);!
C3_S10 : LINE=(C3P);!
C4_S10 : LINE=(C4P);!
C1_S11 : LINE=(C1P);!
C2_S11 : LINE=(C2P);!
C3_S11 : LINE=(C3B);!
C4_S11 : LINE=(C4B);!
C1_S12 : LINE=(C1B);!
C2_S12 : LINE=(C2B);!
C3_S12 : LINE=(C3A);!
C4_S12 : LINE=(C4A);!
C1_S13 : LINE=(C1A);!
C2_S13 : LINE=(C2A);!
C3_S13 : LINE=(C3B);!
C4_S13 : LINE=(C4B_DCCT);!
C1_S14 : LINE=(C1B);!
C2_S14 : LINE=(C2B);!
C3_S14 : LINE=(C3P);!
C4_S14 : LINE=(C4P_DCCT);!
C1_S15 : LINE=(C1P);!
C2_S15 : LINE=(C2P);!
C3_S15 : LINE=(C3B);!
C4_S15 : LINE=(C4B_GBPM);!
C1_S16 : LINE=(C1B);!
C2_S16 : LINE=(C2B);!
C3_S16 : LINE=(C3A);!
C4_S16 : LINE=(C4A_BbBKckrV);!
C1_S17 : LINE=(C1A);!
C2_S17 : LINE=(C2A);!
C3_S17 : LINE=(C3B);!
C4_S17 : LINE=(C4B_TunePkupV);!
C1_S18 : LINE=(C1B);!
C2_S18 : LINE=(C2B);!
C3_S18 : LINE=(C3P);!
C4_S18 : LINE=(C4P_TuneShkrV);!
C1_S19 : LINE=(C1P);!
C2_S19 : LINE=(C2P);!
C3_S19 : LINE=(C3B);!
C4_S19 : LINE=(C4B_PingV);!
C1_S20 : LINE=(C1B);!
C2_S20 : LINE=(C2B);!
C3_S20 : LINE=(C3A);!
C4_S20 : LINE=(C4A);!

!!! SECTORS # 01..20
S01 : LINE=(M1_S01, SS_S01, M2_S01, B1, C1_S01, B2, C2_S01, BC, C3_S01, B2, C4_S01, B1);!
S02 : LINE=(M1_S02, SS_S02, M2_S02, B1, C1_S02, B2, C2_S02, BC, C3_S02, B2, C4_S02, B1);!
S03 : LINE=(M1_S03, SS_S03, M2_S03, B1, C1_S03, B2, C2_S03, BC, C3_S03, B2, C4_S03, B1);!
S04 : LINE=(M1_S04, SS_S04, M2_S04, B1, C1_S04, B2, C2_S04, BC, C3_S04, B2, C4_S04, B1);!
S05 : LINE=(M1_S05, SS_S05, M2_S05, B1, C1_S05, B2, C2_S05, BC, C3_S05, B2, C4_S05, B1);!
S06 : LINE=(M1_S06, SS_S06, M2_S06, B1, C1_S06, B2, C2_S06, BC, C3_S06, B2, C4_S06, B1);!
S07 : LINE=(M1_S07, SS_S07, M2_S07, B1, C1_S07, B2, C2_S07, BC, C3_S07, B2, C4_S07, B1);!
S08 : LINE=(M1_S08, SS_S08, M2_S08, B1, C1_S08, B2, C2_S08, BC, C3_S08, B2, C4_S08, B1);!
S09 : LINE=(M1_S09, SS_S09, M2_S09, B1, C1_S09, B2, C2_S09, BC, C3_S09, B2, C4_S09, B1);!
S10 : LINE=(M1_S10, SS_S10, M2_S10, B1, C1_S10, B2, C2_S10, BC, C3_S10, B2, C4_S10, B1);!
S11 : LINE=(M1_S11, SS_S11, M2_S11, B1, C1_S11, B2, C2_S11, BC, C3_S11, B2, C4_S11, B1);!
S12 : LINE=(M1_S12, SS_S12, M2_S12, B1, C1_S12, B2, C2_S12, BC, C3_S12, B2, C4_S12, B1);!
S13 : LINE=(M1_S13, SS_S13, M2_S13, B1, C1_S13, B2, C2_S13, BC, C3_S13, B2, C4_S13, B1);!
S14 : LINE=(M1_S14, SS_S14, M2_S14, B1, C1_S14, B2, C2_S14, BC, C3_S14, B2, C4_S14, B1);!
S15 : LINE=(M1_S15, SS_S15, M2_S15, B1, C1_S15, B2, C2_S15, BC, C3_S15, B2, C4_S15, B1);!
S16 : LINE=(M1_S16, SS_S16, M2_S16, B1, C1_S16, B2, C2_S16, BC, C3_S16, B2, C4_S16, B1);!
S17 : LINE=(M1_S17, SS_S17, M2_S17, B1, C1_S17, B2, C2_S17, BC, C3_S17, B2, C4_S17, B1);!
S18 : LINE=(M1_S18, SS_S18, M2_S18, B1, C1_S18, B2, C2_S18, BC, C3_S18, B2, C4_S18, B1);!
S19 : LINE=(M1_S19, SS_S19, M2_S19, B1, C1_S19, B2, C2_S19, BC, C3_S19, B2, C4_S19, B1);!
S20 : LINE=(M1_S20, SS_S20, M2_S20, B1, C1_S20, B2, C2_S20, BC, C3_S20, B2, C4_S20, B1);!

!!! The ring
SI : LINE=(S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14, S15, S16, S17, S18, S19, S20);!

BEAM, PARTICLE=ELECTRON, RADIATE=TRUE, ENERGY=3.0;
USE, PERIOD=SI;
SAVE, SEQUENCE=SI, FILE=sirius-ring.temp, BARE;
CALL, FILE=sirius-ring.temp;
REMOVEFILE, FILE=sirius-ring.temp;

SEQEDIT, SEQUENCE=SI;
FLATTEN;
CYCLE, START=M_START;
ENDEDIT;

"""
f = open('sirius.seq', 'w')
f.write(stri)
f.close()
