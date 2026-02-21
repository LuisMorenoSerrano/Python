import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import gridspec
from mpl_toolkits.axes_grid1 import AxesGrid
import matplotlib
from scipy.optimize import fsolve

# Matplotlib config
pt=1/72 # inch/pt

elsevierSingleColumn = 222# 255.0
elsevierSingleHalfColumn = 397.0
elsevierDoubleColumn = 468#539.0

def heightFig(width, aspectRatio = 4/3):
    return width/aspectRatio

elsevierOneColumnWidth=345.0 # pt
elsevierTwoColumnWidth=222.0 # pt

oneColumnFig=elsevierSingleColumn*pt, heightFig(elsevierSingleColumn*pt, aspectRatio=7/5)
doubleColumnFig=elsevierDoubleColumn*pt, heightFig(elsevierSingleColumn*pt, aspectRatio=7/5)
triFigure = elsevierOneColumnWidth*pt, heightFig(elsevierSingleColumn*pt, aspectRatio=7/5)

twoParallelFig = 539/2.5*pt, heightFig(539/2.5*pt)

# When exporting files
transparent=True
ext='pdf'
# matplotlib.use('pgf')
matplotlib.rcParams.update({
    'figure.autolayout': True,
    'pgf.texsystem': 'pdflatex',
    'text.usetex': True,
    'pgf.rcfonts': False,
    'savefig.transparent': transparent,
    'savefig.format': ext,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})

# Plot content
lineWidth=1.5
markerSize=3
matplotlib.rcParams.update({
    'axes.labelsize': 'small', # default 'medium'
    'figure.titlesize': 'medium',    # default 'large'
    'font.family': 'serif',
    'font.size': 13, # default 10
    'legend.fontsize': 'medium', # default 'medium',
    'legend.frameon': False,
    'lines.markersize': markerSize,
    'lines.markerfacecolor': 'none',
    'lines.linewidth': lineWidth,
    'xtick.labelsize': 'small', # default 'medium'
    'xtick.direction': 'in',
    'xtick.bottom': True,
    'xtick.top': True,
    'xtick.minor.visible': True,
    'ytick.labelsize': 'small', # default 'medium'
    'ytick.direction': 'in',
    'ytick.left': True,
    'ytick.right': True,
})

locmaj = matplotlib.ticker.LogLocator(base=10.0, subs=(1.0, ), numticks=100)
locmin = matplotlib.ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100)

# Funciones

def PM(nu):
    gamma = 1.4

    def ecuacion(M, nu):
        return (np.sqrt((gamma + 1)/(gamma - 1)) * np.arctan(np.sqrt((gamma - 1)/(gamma + 1) * (M**2 - 1))) - np.arctan(np.sqrt(M**2 - 1))) - nu*(np.pi/180)

    M3_inicial = 2.0

    M3 = fsolve(ecuacion, M3_inicial, args=(nu))

    return M3[0]

def nu_i(M):
        return (np.sqrt((gamma + 1)/(gamma -1))*np.arctan(np.sqrt((gamma - 1)/(gamma + 1) * (M**2 - 1))) - np.arctan(np.sqrt(M**2 - 1))) * (180/np.pi)

def asind(x):
    result = np.degrees(np.arcsin(x))
    return result

def tand(x):
    result = np.degrees(np.tan(x))
    return result

# Datos iniciales

M_e         = 2.5                                   
n           = 4                           
D_t         = 1.0
r           = D_t / 2  

gamma = 1.4

# Cálculos iniciales

Nu_e = nu_i(M_e)

theta_max = Nu_e / 2

n_nodos = int((2 + (n + 1)) * (n/2))
nodos = np.arange(n_nodos+1)

nodos_pared = np.zeros(n + 1, dtype=int)
nodos_pared[n] = n_nodos


for i in range(1, n):
    nodos_pared[n - i] = nodos_pared[n - i + 1] - (i + 1)

theta_inicial = theta_max - np.floor(theta_max)
incremento = (theta_max - theta_inicial) / (n-1)

x = np.zeros(n_nodos)
y = np.zeros(n_nodos)
x_pared = np.zeros_like(nodos_pared)
y_pared = np.zeros_like(nodos_pared)
x_centro = np.zeros(n)
y_centro = np.zeros_like(x_centro)

y[0] = r
x[0] = 0

# Inicializar arrays

theta = np.zeros(n_nodos + 1)
nu = np.zeros(n_nodos + 1)
mu = np.zeros(n_nodos + 1)

N_Mach = np.zeros(n_nodos + 1)

K_minus = np.zeros(n_nodos + 1)
K_plus = np.zeros(n_nodos + 1)

m_Cminus = np.zeros(n_nodos + 1)
m_Cplus = np.zeros(n_nodos + 1)


# Bucle principal

j = 1

for i in range(0,n_nodos):
    if i < nodos_pared[j+1]:
        if nodos_pared[j] == 0: # Todos los puntos realacionados con el punto A
            # Punto A
            theta[0] = theta_inicial + (i)*incremento
            nu[0] = theta[0]
            K_minus[0] = theta[0] + nu[0]
            K_plus[0] = -K_minus[0]
            N_Mach[0] = PM(nu[0])
            mu[0] = asind(1/N_Mach[0])

            # Para los demás puntos
            theta[i+1] = (K_minus[0] + K_plus[i])/2
            nu[i+1] = (K_minus[0] - K_plus[i])/2
            K_minus[i+1] = theta[i+1] + nu[i+1]
            K_plus[i+1] = theta[i+1] - nu[i+1]
            N_Mach[i+1] = PM(nu[i+1])
            mu[i+1] = asind(1/N_Mach[i+1])
               
            m_Cminus[i+1] = tand(((theta[0] - mu[0]) + (theta[i+1] - mu[i+1]))/2)

            if i == 0: # Punto 1, que también pertence a los de la pared
                m_Cplus[i+1] = - m_Cminus[i+1]
                y[i+1] = 0
                x[i+1] = -y[0] / m_Cminus[i+1]
                x_centro[i+1] = x[i+1]
            else: # Resto de puntos que tienen interacción con A
                m_Cplus[i+1] = tand(((theta[0] + mu[0]) + (theta[i+1] + mu[i+1]))/2)
                x[i+1] = (y[0] - y[i] + m_Cplus[i+1]*x[i] - m_Cminus[i+1]*x[0]) / (m_Cplus[i+1] - m_Cminus[i+1])
                y[i+1] = y[i] + m_Cplus[i+1]*(x[i+1] - x[i])

    #       else: # Todos los puntos independientes de A
    #            l = n - j
    #            K_minus[i+1] = K_minus[i-l]
    #            K_plus[i+1] = - K_minus[n + 3 - l]
    #            theta[i+1] = (K_minus[i+1] + K_plus[i+1]) / 2
    #            nu[i+1] = (K_minus[i+1] - K_plus[i+1]) / 2
    #            N_Mach[i+1] = PM(nu[i+1])
    #            mu[i+1] = asind(1/N_Mach[i+1])

    #            m_Cminus[i+1] = tand(((theta[i-l] - mu[i-l]) + (theta[i+1] - mu[i+1]))/2)

    #            if theta[i+1] == 0: # Puntos en la linea central
    #                 y[i+1] = 0
    #                 x[i+1] = x[i-l] - y[i-l] / m_Cminus[i+1]
    #                 m_Cplus[i+1] = -m_Cminus[i+1]
    #                 x_centro[i+1] = x[i+1]
    #            else:
    #                 m_Cplus = tand(((theta[i] + mu[i]) + (theta[i+1] + mu[i+1]))/2)
    #                 x[i+1] = (y[i-l] - y[i] + m_Cplus[i+1]*x[i] - m_Cminus[i+1]*x[i-l]) / (m_Cplus[i+1] - m_Cminus[i+1])
    #                 y[i+1] = [i] + m_Cplus[i+1]*(x[i+1] - x[i])

    #  elif i == nodos_pared[j+1]:  # Puntos del contorno
    #       K_minus[i+1] = K_minus[0]
    #       K_plus[i+1] = K_plus[i]
    #       theta[i+1] = (K_minus[i+1] + K_plus[i+1])/2
    #       nu[i+1] = (K_minus[i+1] - K_plus[i+1])/2
    #       N_Mach[i+1] = PM(nu[i+1])
    #       mu[i+1] = asind(1/N_Mach[i+1])



