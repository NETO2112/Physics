# -*- coding: utf-8 -*-
"""Tarefa-5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11l_CXkaoaoNiaPCzjYyxyUvDEpo0lyAN
"""

#coding:utf8
import numpy as np
import matplotlib.pyplot as plt
from random import random

nbins = 30
hist = []
M = int(1e4)
xmin,xmax=0,10

for i in range(M):
  hist.append(np.random.normal(loc=5,scale=2))

mu,sigma=5,2
x=np.linspace(0,10)
gau=np.exp(-((x-mu)**2/(2*sigma**2)))/(np.sqrt(2*np.pi)*sigma)

plt.hist(hist, bins=nbins,range=[xmin,xmax],density=True,edgecolor='#f000ff',color='#00ff00', label='30 bins')
plt.legend()
plt.plot(x,gau,color='#ff0000')
plt.title(r'Distribuição Gaussiana com $\mu$ = 5 e $\sigma$ = 2')
plt.xlabel('Densidade de Probabilidade')
plt.ylabel('x')
plt.savefig('Tarefa 5a.pdf')

nbins=25
hist=[]
M=int(1e6)
prob= lambda x: np.exp(-x)
for i in range(M):
  r1,r2=random(),random()
  x=8*r1
  y=r2
  if (y<prob(x)):
    hist.append(x)

plt.hist(hist, density=True,edgecolor='#f000ff',color='#00ff00',label='25 bins', log='true',bins=nbins)
plt.legend()
x=np.linspace(0,8)
plt.plot(x,prob(x),color='#ff0000')
plt.title(r'Método da Rejeição: p(x) = e$^{-x}$')
plt.ylabel('Densidade de Probabilidade')
plt.xlabel('x')
plt.savefig('Tarefa 5b.pdf')