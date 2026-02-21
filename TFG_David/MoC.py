import math
import numpy as np
import matplotlib.pyplot as plt

#%% INPUTS
plotting    = True
M_e         = 2.5                                     # Exit Mach number
n           = 25                                      # Number of characteristics
D_t         = 1                                       # Throat diameter
r           = D_t / 2                                 # Throat radius

GAMMA       = 1.4                                     # Heat capacity ratio
GAMMA1      = (GAMMA + 1) / (GAMMA - 1)

k1          = 1 + ((GAMMA - 1) / 2 * M_e ** 2)
k2          = (GAMMA + 1) / (2 * (GAMMA - 1))
A_ratio     = 1 / M_e * (2 * k1 / (GAMMA + 1)) ** k2  # Ratio between critical area and outlet

nu_e        = math.sqrt((GAMMA + 1) / (GAMMA - 1))                               \
              * math.atan(math.sqrt((GAMMA - 1) / (GAMMA + 1) * (M_e ** 2 - 1))) \
              - math.atan(math.sqrt(M_e ** 2 - 1))

theta_max   = nu_e / 2
theta_start = np.linspace(0.001, theta_max, n)

#%% CHARACTERISTICS
nui    = np.zeros((n, n))
thetai = np.zeros((n, n))

C_Ii   = np.zeros((n, n))
C_IIi  = np.zeros((n, n))

nub    = np.zeros((1, n))
thetab = np.zeros((1, n))

C_Ib   = np.zeros((1, n))
C_IIb  = np.zeros((1, n))

thetai[:, 0] = theta_start
nui   [:, 0] = thetai[:, 0]

C_Ii  [:, 0] = 2 * nui[:, 0]
C_IIi [:, 0] = nui[:, 0] - thetai[:, 0]

for i in range(n - 1):
    for j in range(n - 1 - i):
        if j == 0:
            nui   [j, i + 1] = C_Ii[j + 1, i]
            thetai[j, i + 1] = 0
            C_Ii  [j, i + 1] = nui[j, i + 1] + thetai[j, i + 1]
            C_IIi [j, i + 1] = nui[j, i + 1] - thetai[j, i + 1]
        else:
            nui   [j, i + 1] = 1 / 2 * (C_Ii[j + 1, i] + C_IIi[j - 1, i + 1])
            thetai[j, i + 1] = 1 / 2 * (C_Ii[j + 1, i] - C_IIi[j - 1, i + 1])
            C_Ii  [j, i + 1] = nui[j, i + 1] + thetai[j, i + 1]
            C_IIi [j, i + 1] = nui[j, i + 1] - thetai[j, i + 1]

for i in range(n):
    thetab[0, i] = thetai[n - 1 - i, i]
    C_IIb [0, i] = C_IIi[n - 1 - i, i]
    nub   [0, i] = thetab[0, i] + C_IIb[0, i]
    C_Ib  [0, i] = thetab[0, i] + nui[0, i]

z1    = np.zeros((1, n))
nu    = np.vstack((nui, z1))
theta = np.vstack((thetai, z1))
C_I   = np.vstack((C_Ii, z1))
C_II  = np.vstack((C_IIi, z1))

z2    = np.zeros((n + 1, 1))
nu    = np.hstack((nu, z2))
theta = np.hstack((theta, z2))
C_I   = np.hstack((C_I, z2))
C_II  = np.hstack((C_II, z2))

for i in range(n):
    nu   [n - i, i] = nub   [0, i]
    theta[n - i, i] = thetab[0, i]
    C_I  [n - i, i] = C_Ib  [0, i]
    C_II [n - i, i] = C_IIb [0, i]

thetad = theta * 180 / math.pi

#%% CONTOUR CALCULATION
DM         = 0.01
MARG_ERROR = 1e-5
M          = np.zeros((n + 1, n + 1))
mi         = np.zeros((n + 1, n + 1))
theta_p_mi = np.zeros((n + 1, n + 1))
theta_m_mi = np.zeros((n + 1, n + 1))
fun        = np.zeros((n + 1, n + 1))
fun1       = np.zeros((n + 1, n + 1))
fun2       = np.zeros((n + 1, n + 1))
dfun_dM    = np.zeros((n + 1, n + 1))

for i, j in np.ndindex((n + 1, n + 1)):
    if i == n or j > n - i:
        continue

    M_0       = 1.05
    fun[j, i] = (math.sqrt(GAMMA1)                                      \
                * math.atan(math.sqrt(GAMMA1 ** (-1) * (M_0 ** 2 - 1))) \
                - math.atan(math.sqrt(M_0 ** 2 - 1))) - nu[j, i]

    while abs(fun[j, i]) > MARG_ERROR:
        M_1              = M_0 + DM
        M_2              = M_0 - DM

        fun1[j, i]       = (math.sqrt(GAMMA1)                                       \
                            * math.atan(math.sqrt(GAMMA1 ** (-1) * (M_1 ** 2 - 1))) \
                            - math.atan(math.sqrt(M_1 ** 2 - 1))) - nu[j, i]
        fun2[j, i]       = (math.sqrt(GAMMA1)                                       \
                            * math.atan(math.sqrt(GAMMA1 ** (-1) * (M_2 ** 2 - 1))) \
                            - math.atan(math.sqrt(M_2 ** 2 - 1))) - nu[j, i]
        dfun_dM[j, i]    = (fun1[j, i] - fun2[j, i]) / (2 * DM)

        M[j, i]          = M_0 - (fun[j, i] / dfun_dM[j, i])
        M_0              = M[j, i]

        mi[j, i]         = math.asin(1 / M[j, i])
        theta_p_mi[j, i] = theta[j, i] + mi[j, i]
        theta_m_mi[j, i] = theta[j, i] - mi[j, i]

        fun[j, i]        = (math.sqrt(GAMMA1)                                       \
                            * math.atan(math.sqrt(GAMMA1 ** (-1) * (M_0 ** 2 - 1))) \
                            - math.atan(math.sqrt(M_0 ** 2 - 1))) - nu[j, i]

theta_p_mid = theta_p_mi * 180 / math.pi
theta_m_mid = theta_m_mi * 180 / math.pi
mid         = mi * 180 / math.pi

xp   = np.zeros((n + 1, n + 1))
yp   = np.zeros((n + 1, n + 1))
m_I  = np.zeros((n + 1, n + 1))
m_II = np.zeros((n + 1, n + 1))

for i, j in np.ndindex((n + 1, n + 1)):
    if i == n or j > n - i:
        continue

    if i == 0 and j < n:
        m_I[j, i] = math.tan(theta_m_mi[j, i])
    elif i == 0 and j == n:
        m_I[j, i] = math.tan(theta[j, i])
    elif j == n - i and i > 0:
        m_I[j, i] = math.tan(1 / 2 * (theta[j, i] + theta[j + 1, i - 1]))
    else:
        m_I[j, i] = math.tan(1 / 2 * (theta_m_mi[j, i] + theta_m_mi[j + 1, i - 1]))

for i, j in np.ndindex((n + 1, n + 1)):
    if i == n or j > n - i:
        continue

    if j == 0:
        m_II[j, i] = math.tan(theta_p_mi[j, i])
    else:
        m_II[j, i] = math.tan(1 / 2 * (theta_p_mi[j, i] + theta_p_mi[j - 1, i]))

for i, j in np.ndindex((n + 1, n + 1)):
    x0 = 0
    y0 = r

    if i == n or j > n - i:
        continue

    if j == 0 and i == 0:
        xp[j, i] = x0 - y0 / m_I[j, i]
        yp[j, i] = 0
    elif j > 0 and i == 0:
        xp[j, i] = (y0                \
                    - yp[j - 1, i]    \
                    + m_II[j, i]      \
                    * xp[j - 1, i]    \
                    - m_I[j, i] * x0) \
                    / (m_II[j, i] - m_I[j, i])
        yp[j, i] = y0 + m_I[j, i]*(xp[j, i] - x0)
    elif j == 0 and i > 0:
        xp[j, i] = (yp[j + 1, i - 1]                \
                    - ((-1) * yp[j + 1, i - 1])     \
                    + ((-1) * m_I[j, i])            \
                    * xp[j + 1, i - 1]              \
                    - m_I[j, i] * xp[j + 1, i - 1]) \
                    / ((-1) * m_I[j, i] - m_I[j, i])
        yp[j, i] = 0
    elif j > 0 and i > 0:
        xp[j, i] = (yp[j + 1, i - 1]                \
                    - yp[j - 1, i]                  \
                    + m_II[j, i]                    \
                    * xp[j - 1, i]                  \
                    - m_I[j, i] * xp[j + 1, i - 1]) \
                    / (m_II[j, i] - m_I[j, i])
        yp[j, i] = yp[j + 1, i - 1]                 \
                    + m_I[j, i]                     \
                    * (xp[j, i] - xp[j + 1, i - 1])

Aratio1 = yp[1, n - 1] / y0

#%% PLOT
if plotting:
    xWallPoints = np.zeros(n + 1)
    yWallPoints = np.zeros(n + 1)

    xWallPoints[0] = x0
    yWallPoints[0] = y0

    for i in range(n):
        xWallPoints[i + 1] = xp[n - i, i]
        yWallPoints[i + 1] = yp[n - i, i]

    y0f = -1 * y0
    ypf = -1 * yp

    xlist1 = []
    ylist1 = []
    xlist2 = []
    ylist2 = []

    xlist1.extend([x0, xp[n, 0]])
    xlist1.append(None)
    ylist1.extend([y0, yp[n, 0]])
    ylist1.append(None)
    xlist1.extend([x0, xp[n, 0]])
    xlist1.append(None)
    ylist1.extend([y0f, ypf[n, 0]])
    ylist1.append(None)

    xlist2.extend([xp[1, 0], xp[0, 1]])
    xlist2.append(None)
    ylist2.extend([yp[1, 0], yp[0, 1]])
    ylist2.append(None)
    xlist2.extend([xp[1, 0], xp[0, 1]])
    xlist2.append(None)
    ylist2.extend([ypf[1, 0], ypf[0, 1]])
    ylist2.append(None)

    for i in range(n + 1):
        if i < n:
            xlist2.extend([x0, xp[i, 0]])
            xlist2.append(None)
            ylist2.extend([y0, yp[i, 0]])
            ylist2.append(None)
            xlist2.extend([x0, xp[i, 0]])
            xlist2.append(None)
            ylist2.extend([y0f, ypf[i, 0]])
            ylist2.append(None)

        for j in range(n + 1):
            if i == n or j > n - i:
                continue

            if j < n - i:
                xlist2.extend([xp[j, i], xp[j + 1, i]])
                xlist2.append(None)
                ylist2.extend([yp[j, i], yp[j + 1, i]])
                ylist2.append(None)
                xlist2.extend([xp[j, i], xp[j + 1, i]])
                xlist2.append(None)
                ylist2.extend([ypf[j, i], ypf[j + 1, i]])
                ylist2.append(None)
            elif j == n - i and i < n - 1:
                xlist1.extend([xp[j, i], xp[j - 1, i + 1]])
                xlist1.append(None)
                ylist1.extend([yp[j, i], yp[j - 1, i + 1]])
                ylist1.append(None)
                xlist1.extend([xp[j, i], xp[j - 1, i + 1]])
                xlist1.append(None)
                ylist1.extend([ypf[j, i], ypf[j - 1, i + 1]])
                ylist1.append(None)

    for i in range(n + 1):
        for j in range(i):
            if 1 < i < n:
                xlist2.extend([xp[i - j, j], xp[i - 1 - j, j + 1]])
                xlist2.append(None)
                ylist2.extend([yp[i - j, j], yp[i - 1 - j, j + 1]])
                ylist2.append(None)
                xlist2.extend([xp[i - j, j], xp[i - 1 - j, j + 1]])
                xlist2.append(None)
                ylist2.extend([ypf[i - j, j], ypf[i - 1 - j, j + 1]])
                ylist2.append(None)

    plt.figure()
    plt.grid(True)

    plt.plot(xlist1, ylist1, marker='o', c='b', ls='-', zorder=2)
    plt.plot(xlist2, ylist2, marker='o', mec='silver', mfc='silver', ms='2.0', \
             c='silver', ls='--', linewidth='0.85', zorder=1)

    plt.show()
