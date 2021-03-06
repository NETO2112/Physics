# -*- coding: utf-8 -*-
"""Tarefa7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S8Ey6nbOVM4K3cfW6Mr08KaopcZcq5Pz
"""

'''
gduarte@home-vm
Created on 18-ago-2021
'''

# coding:utf8
from collections import OrderedDict
import matplotlib.pyplot as plt
from numba import jit, int64, float64
from numba.experimental import jitclass
import numpy as np
ranf = np.random.rand

spec = {'L': int64, 'N': int64, 't_mcs': int64,
        'T': float64, 'h': float64,
        '_u': int64[:], '_d': int64[:],
        '_l': int64[:], '_r': int64[:],
        'lattice': int64[:],}

@jitclass(OrderedDict(spec))
class Ising2D:
    '''
    Metropolis algorithm implementation of a
    2-dimensional Ising model with periodic 
    boundary conditions.
    
    Parameters
    ----------
    L : int
        Size of the lattice.
    temp : float, optional
        Temperature of the lattice. Default is 2.
    initial : int, optional
        Initial conditions:
            -1 : all spins down   
             0 : random spins
            +1 : all spins up (default)
    '''
    def __init__(self, L, temp=2., initial=+1):
        self.L = L
        self.N = L*L
        self.T = temp
        self.t_mcs = 0
        self.h = 0
        self.set_initial(initial)
        self._set_indices()

    def _set_indices(self):
        u = np.empty(self.N, dtype=int64) 
        d = np.empty(self.N, dtype=int64) 
        l = np.empty(self.N, dtype=int64) 
        r = np.empty(self.N, dtype=int64) 
        L = self.L
        for i in range(self.N):
            y = i%L; x = (i-i%L)//L
            u[i] = (y + ((x+L-1)%L)*L)
            d[i] = (y + ((x+1)%L)*L)
            l[i] = ((y+L-1)%L + x*L)
            r[i] = ((y+1)%L + x*L)
        self._u = u
        self._d = d
        self._l = l
        self._r = r

    def set_initial(self, ci):
        if (abs(ci) == 1):
            self.lattice = np.array([ci for _ in range(self.N)])
        elif (ci == 0):
            self.lattice = np.array([1 if (ranf()>.5) else -1 for _ in range(self.N)])
        else:
            raise ValueError(
            """ci must be:
                  -1 : all spins down
                   0 : random spins
                  +1 : all spins up""")

    def set_temp(self, temp):
        self.T = temp

    def set_field(self, field):
        self.h = field

    def calc_energy(self):
        s = 0
        for i in range(self.N):
            d = self._d[i]
            r = self._r[i]
            s -= self.lattice[i] * (self.lattice[d] + self.lattice[r])
        return s

    def calc_magn(self):
        s = 0
        for i in range(self.N):
            s += self.lattice[i]
        return s

    def flip_spin(self, i):
        l = self._l[i]
        r = self._r[i]
        u = self._u[i]
        d = self._d[i]
        d_energy = (self.lattice[u] + self.lattice[d] + self.lattice[l] + self.lattice[r] + self.h)
        d_energy *= 2. * self.lattice[i]
        if (d_energy <= 0.) | (ranf() < np.exp(-d_energy/self.T)):
            self.lattice[i] *= -1
            return 1
        else: return 0

    def mc_step(self):
        for t in range(self.N):
            i = int(ranf() * self.N)
            self.flip_spin(i)
        self.t_mcs += 1
        return self.t_mcs

L = 50

#ferro_default = Ising2D(L)
#ferro_neg = Ising2D(L, initial=-1)
para1 = Ising2D(L, temp=1.5, initial=0)
para2 = Ising2D(L, temp=2.27, initial=0)
para3 = Ising2D(L, temp=3., initial=0)

ferr1 = Ising2D(L, temp=1.5, initial=-1)
ferr2 = Ising2D(L, temp=2.27, initial=-1)
ferr3 = Ising2D(L, temp=3., initial=-1)

# Contagem de tempo
step_list1 = []
step_list2 = []
step_list3 = []

step_list1f = []
step_list2f = []
step_list3f = []

# Medidas de Energia
e_para1 = [] 
e_para2 = []
e_para3 = []

e_ferr1 = [] 
e_ferr2 = []
e_ferr3 = []

# Medidas de Magnetiza????o
m_para1 = []
m_para2 = []
m_para3 = []

m_ferr1 = []
m_ferr2 = []
m_ferr3 = []

for t in range(2000):

  step_list1.append(para1.mc_step())
  e_para1.append(para1.calc_energy()/(L*L))
  m_para1.append(para1.calc_magn()/(L*L))
  step_list1f.append(ferr1.mc_step())
  e_ferr1.append(ferr1.calc_energy()/(L*L))
  m_ferr1.append(ferr1.calc_magn()/(L*L))

  step_list2.append(para2.mc_step())
  e_para2.append(para2.calc_energy()/(L*L))
  m_para2.append(para2.calc_magn()/(L*L))
  step_list2f.append(ferr2.mc_step())
  e_ferr2.append(ferr2.calc_energy()/(L*L))
  m_ferr2.append(ferr2.calc_magn()/(L*L))

  step_list3.append(para3.mc_step())
  e_para3.append(para3.calc_energy()/(L*L))
  m_para3.append(para3.calc_magn()/(L*L))
  step_list3f.append(ferr3.mc_step())
  e_ferr3.append(ferr3.calc_energy()/(L*L))
  m_ferr3.append(ferr3.calc_magn()/(L*L))

"""# Gr??ficos de mesmo L variando T para paramag e ferromag"""

plt.figure(1, figsize=[10,6])
plt.plot(step_list1, e_para1,color='red', label=f'T = {para1.T}')
plt.plot(step_list2, e_para2,color='green', label='T cr??tica')
plt.plot(step_list3, e_para3,color='blue', label=f'T = {para3.T}')
plt.legend()
plt.xlabel('$t$')
plt.ylabel('$e$')
#plt.title(r'Gr??fico da energia pelo tempo ')
plt.savefig('1.png')

plt.figure(2, figsize=[10,6])
plt.plot(step_list1, m_para1,color='red', label=f'T = {para1.T}')
plt.plot(step_list2, m_para2,color='green', label='T cr??tica')
plt.plot(step_list3, m_para3,color='blue', label=f'T = {para3.T}')
plt.legend()
plt.xlabel('$t$')
plt.ylabel('$m$')
plt.savefig('2.png')

plt.figure(3, figsize=[10,6])
plt.plot(step_list1f, e_ferr1,color='red', label=f'T = {ferr1.T}')
plt.plot(step_list2f, e_ferr2,color='green', label='T cr??tica')
plt.plot(step_list3f, e_ferr3,color='blue', label=f'T = {ferr3.T}')
plt.legend()
plt.xlabel('$t$')
plt.ylabel('$e$')
plt.savefig('3.png')

plt.figure(4, figsize=[10,6])
plt.plot(step_list1f, m_ferr1,color='red', label=f'T = {ferr1.T}')
plt.plot(step_list2f, m_ferr2,color='green', label='T cr??tica')
plt.plot(step_list3f, m_ferr3,color='blue', label=f'T = {ferr3.T}')
plt.legend()
plt.xlabel('$t$')
plt.ylabel('$m$')
plt.savefig('4.png')

L = 50

#ferro_default = Ising2D(L)
#ferro_neg = Ising2D(L, initial=-1)
para1 = Ising2D(L, temp=2., initial=0)
para2 = Ising2D(L, temp=2., initial=0)
para3 = Ising2D(L, temp=2., initial=-1)

# Contagem de tempo
step_list1 = []
step_list2 = []
step_list3 = []

# Medidas de Energia
e_para1 = [] 
e_para2 = []
e_para3 = []

# Medidas de Magnetiza????o
m_para1 = []
m_para2 = []
m_para3 = []

for t in range(2000):

  step_list1.append(para1.mc_step())
  e_para1.append(para1.calc_energy()/(L*L))
  m_para1.append(para1.calc_magn()/(L*L))

  step_list2.append(para2.mc_step())
  e_para2.append(para2.calc_energy()/(L*L))
  m_para2.append(para2.calc_magn()/(L*L))

  step_list3.append(para3.mc_step())
  e_para3.append(para3.calc_energy()/(L*L))
  m_para3.append(para3.calc_magn()/(L*L))

plt.figure(5, figsize=[10,6])
plt.plot(step_list1, e_para1,color='red', label=f'T = {para1.T}')
plt.plot(step_list2, e_para2,color='green', label=f'T = {para2.T}')
plt.plot(step_list3, e_para3,color='blue', label=f'T = {para3.T}')
plt.legend()
plt.xlabel('$t$')
plt.ylabel('$e$')
plt.savefig('5.png')

plt.figure(6, figsize=[10,6])
plt.plot(step_list1, m_para1,color='red', label=f'T = {para1.T}')
plt.plot(step_list2, m_para2,color='green', label=f'T = {para2.T}')
plt.plot(step_list3, m_para3,color='blue', label=f'T = {para3.T}')
plt.legend()
plt.xlabel('$t$')
plt.ylabel('$m$')
plt.savefig('6.png')

L = 50
L2 = 10

#ferro_default = Ising2D(L)
#ferro_neg = Ising2D(L, initial=-1)
para1 = Ising2D(L, temp=1.5, initial=0)
para2 = Ising2D(L2, temp=1.5, initial=0)

# Contagem de tempo
step_list1 = []
step_list2 = []


# Medidas de Energia
e_para1 = [] 
e_para2 = []


# Medidas de Magnetiza????o
m_para1 = []
m_para2 = []


for t in range(600):

  step_list1.append(para1.mc_step())
  e_para1.append(para1.calc_energy()/(L*L))
  m_para1.append(para1.calc_magn()/(L*L))

  step_list2.append(para2.mc_step())
  e_para2.append(para2.calc_energy()/(L2*L2))
  m_para2.append(para2.calc_magn()/(L2*L2))

plt.figure(7, figsize=[10,6])
plt.plot(step_list1, e_para1,color='red', label=f'L = {para1.L}')
plt.plot(step_list2, e_para2,color='green', label=f'L = {para2.L}')
plt.legend()
plt.xlabel('$t$')
plt.ylabel('$e$')
plt.savefig('7.png')

plt.figure(8, figsize=[10,6])
plt.plot(step_list1, m_para1,color='red', label=f'L = {para1.L}')
plt.plot(step_list2, m_para2,color='green', label=f'L = {para2.L}')
plt.legend()
plt.xlabel('$t$')
plt.ylabel('$m$')
plt.savefig('8.png')

L = 50
L2 = 10

#ferro_default = Ising2D(L)
#ferro_neg = Ising2D(L, initial=-1)
para1 = Ising2D(L, temp=2.1, initial=0)
para2 = Ising2D(L2, temp=2.1, initial=0)

# Contagem de tempo
step_list1 = []
step_list2 = []


# Medidas de Energia
e_para1 = [] 
e_para2 = []


# Medidas de Magnetiza????o
m_para1 = []
m_para2 = []


for t in range(10000):

  step_list1.append(para1.mc_step())
  e_para1.append(para1.calc_energy()/(L*L))
  m_para1.append(para1.calc_magn()/(L*L))

  step_list2.append(para2.mc_step())
  e_para2.append(para2.calc_energy()/(L2*L2))
  m_para2.append(para2.calc_magn()/(L2*L2))

plt.figure(9, figsize=[10,6])
plt.plot(step_list1, m_para1,color='red', label=f'L = {para1.L}')
plt.plot(step_list2, m_para2,color='green', label=f'L = {para2.L}')
plt.legend()
plt.xlabel('$t$')
plt.ylabel('$m$')
plt.savefig('9.png')

L = 50

#ferro_default = Ising2D(L)
#ferro_neg = Ising2D(L, initial=-1)
#para1 = Ising2D(L, initial=0)
#para2 = Ising2D(L, initial=0)

# Contagem de tempo
step_list1 = []
step_list2 = []


# Medidas de Energia
e_para1 = [] 
e_para2 = []


# Medidas de Magnetiza????o
m_para1 = []
m_para2 = []

# Temperaturas

Te_0 = 2.2
Ta_0 = 0.0
dT = 1e-3

Ta_list = []
Te_list = []
'''
while Te > dT:

  Ta = Ta + dT
  Te = Te - dT

  Ta_list.append(Ta)
  Te_list.append(Te)

  para1 = Ising2D(L, temp=Ta, initial=-1)
  para2 = Ising2D(L, temp=Te, initial=-1)

  step_list1.append(para1.mc_step())
  e_para1.append(para1.calc_energy()/(L*L))
  m_para1.append(para1.calc_magn()/(L*L))

  step_list2.append(para2.mc_step())
  e_para2.append(para2.calc_energy()/(L*L))
  m_para2.append(para2.calc_magn()/(L*L))

  #print(m_para2)
  #print(Te)
'''
for t in range(2199):

  Ta = Ta_0 + (t+1)*dT
  Te = Te_0 - (t+1)*dT

  Ta_list.append(Ta)
  Te_list.append(Te)

  para1 = Ising2D(L, temp=Ta, initial=-1)
  para2 = Ising2D(L, temp=Te, initial=-1)

  step_list1.append(para1.mc_step())
  e_para1.append(para1.calc_energy()/(L*L))
  m_para1.append(para1.calc_magn()/(L*L))

  step_list2.append(para2.mc_step())
  e_para2.append(para2.calc_energy()/(L*L))
  m_para2.append(para2.calc_magn()/(L*L))

plt.figure(10, figsize=[10,6])
plt.plot(Ta_list, m_para1)
plt.plot(Te_list, m_para2)
#plt.plot(step_list1, m_para1,color='red', label=f'L = {para1.L}')
#plt.plot(step_list2, m_para2,color='green', label=f'L = {para2.L}')
#plt.legend()
#plt.xlabel('$t$')
#plt.ylabel('$m$')
plt.savefig('fig10.pdf')

L = 50
N = L**2 
Ta = 2.2

dT = 1e-3
#dT = -1e-3

#ferro_default = Ising2D(L)
para1 = Ising2D(L, initial=0)
para2 = Ising2D(L, initial=0)
nferro1 = Ising2D(L, initial=1)
nferro2 = Ising2D(L, initial=1)

# Contagem de tempo
step_list1 = []
step_list2 = []
step_list3 = []
step_list4 = []

# Medidas de Magnetiza????o
m_para1 = []
m_para2 = []
m_ferro1 = []
m_ferro2 = []

# Medidas de Temperatura
T_para1 = []
T_para2 = []
T_ferro1 = []
T_ferro2 = []

for t in range(22):

  # Variando a Temperatura
  Ta = Ta + dT

  step1 = para1.mc_step()
  step2 = para2.mc_step()
  step3 = nferro1.mc_step()
  step4 = nferro2.mc_step()

  step_list1.append(step1)
  m_para1.append(para1.calc_magn() / N)
  T_para1.append(para1.set_temp(T))

  step_list2.append(step2)
  m_para2.append(para2.calc_magn() / N)
  #T_para2.append(para2.set_temp(T) / N)

  step_list3.append(step3)
  m_ferro1.append(nferro1.calc_magn() / N)
  #T_nferro1.append(nferro1.set_temp(T) / N)

  step_list4.append(step4)
  m_ferro2.append(nferro2.calc_magn() / N)
  #T_nferro2.append(nferro2.set_temp(T) / N)
  print(T_para1)

plt.figure(11, figsize=[10,6])
#plt.plot(Ta_list, m_para1)
plt.plot(T_para1, m_para1)