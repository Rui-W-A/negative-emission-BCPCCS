# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 11:07:43 2021

@author: DELL
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cal_cost as cost
import cal_emiss as emiss

def calAddCost(lcoe_BAU,lcoe_retro,capacity,hours):
    return (lcoe_retro - lcoe_BAU) * capacity * hours

labels = ['B-T-','B+T-','B-T+','B+T+']
tmp_ppOri = pd.read_excel('data/ppDbf.xlsx')
colorsName={'B+T+':'blue','B+T-':'orange','B-T+':'green','B-T-':'red'}

unitAbatementDict = {}
marketTax = 70.6 * 1.07

fig, ax = plt.subplots(figsize=[12,8], dpi=300)
plt.axhline(y = 50 * 0.15, color = 'crimson',ls='--',lw=3, alpha = 0.5)
plt.axhline(y = 70.6 * 1.07, color = 'dodgerblue', ls='--', lw=3, alpha=0.5) 

for scenarioName in labels:
    
    tmp = pd.read_excel('data/minEmiss_%s.xls' % scenarioName)
    tmp['coal_g_kwh'] = tmp_ppOri['coal_g_kWh']
    
    # BAU emission
    tmp['emiss_BAU'] = tmp.apply(lambda tmp: emiss.Emiss_PP(tmp['Capacity_kw'], tmp['hours'],2020,2020), axis = 1)
    
    
    # emission reduction
    tmp['reducedEmiss'] = tmp['emiss_BAU'] - tmp['emiss']
    
    # retrofit cost (lcoe_BAU - lcoe_改造) * Capacity * hours
    tmp['lcoe_BAU'] = tmp.apply(lambda tmp: cost.LCOE_PP(tmp['Capacity_kw'], tmp['hours'], 2000,2040),axis=1)
    tmp['addCost'] = tmp.apply(lambda tmp: calAddCost(tmp['lcoe_BAU'], tmp['lcoe'], tmp['Capacity_kw'], tmp['hours']), axis=1)
    
    # Unit emission reduction cost
    tmp['unitCarbonCost'] = tmp['addCost'] / tmp['reducedEmiss']
    
    # sort
    tmp1 = tmp.sort_values('unitCarbonCost', ascending=True)
    
    # cumulative emission
    tmp1['cumEmiss'] = tmp1['reducedEmiss'].cumsum()
            
    # plot results
    ax.scatter(tmp1['cumEmiss']/pow(10,9), tmp1['unitCarbonCost'],label=scenarioName,marker='o',color='white',edgecolors=colorsName[scenarioName],s=150,linewidths=0.5)
    # record the results
    recordData = pd.DataFrame([tmp1['cumEmiss']/pow(10,9), tmp1['unitCarbonCost']])
    unitAbatementDict.update({scenarioName:recordData})
    
    # count how many number smaller than target tax
    carbon_tmp = tmp['unitCarbonCost'].copy()
    carbon_tmp1 = carbon_tmp[carbon_tmp < marketTax]
    
    num = carbon_tmp1.count()
    numperCent = num/4536
    print('%s: number:%d, percent:%s' % (scenarioName,num, numperCent))
    
   
ax.legend(fontsize=15,loc='upper left',frameon=False)
plt.ylabel('Unit carbon abatement cost ($ / tonne)',fontsize=15)
plt.xlabel('Carbon reduction amount (Gt)',fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

