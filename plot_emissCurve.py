# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 10:20:54 2021

@author: DELL
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
from matplotlib.colors import BoundaryNorm

# ------------------------------------- load data ---------------------------------
ppEmiss_BAU = pd.read_excel('data/ppData_emiss_Bminus.xlsx').loc[:,['emiss_pp']]
ppCost_BAU = pd.read_excel('data/ppData_cost_Bminus.xlsx').loc[:,'lcoe']
# ppDbf = pd.read_excel('data/data01b_devData/dev_ppData/ppDbf.xlsx')

pp_BAU = pd.concat([ppEmiss_BAU, ppCost_BAU] , axis=1)
pp_BAU['endYear'] = pp_BAU.loc[:,'Year'] + 40
ppEmiss_BplusTplus = pd.read_csv('data/minEmiss_B+T+.csv')
ppEmiss_BplusTminus = pd.read_csv('data/minEmiss_B+T-.csv')
ppEmiss_BminusTplus = pd.read_csv('data/minEmiss_B-T+.csv')
ppEmiss_BminusTminus = pd.read_csv('data/minEmiss_B-T-.csv')

# ----------------------------------- yearly result ----------------------------------
emissYearRecord=pd.DataFrame(columns=['year','BAU','B+T+', 'B+T-', 'B-T+', 'B-T-'])

for year in range(1989,2060):
    emissYearly_origin = 0
    emissYearly_BplusTplus = 0
    emissYearly_BplusTminus = 0
    emissYearly_BminusTplus = 0
    emissYearly_BminusTminus = 0
    for i in range(pp_BAU.shape[0]):
        emiss_origin = pp_BAU.loc[i,'emiss_pp'] 
        emiss_BplusTplus = ppEmiss_BplusTplus.loc[i,'emiss']
        emiss_BplusTminus = ppEmiss_BplusTminus.loc[i,'emiss']
        emiss_BminusTplus = ppEmiss_BminusTplus.loc[i,'emiss']
        emiss_BminusTminus = ppEmiss_BminusTminus.loc[i,'emiss']
        
        beginYear = pp_BAU.loc[i,'Year']
        endYear = pp_BAU.loc[i,'endYear']
        
        if year > beginYear and year < endYear:
            emissYearly_origin = emissYearly_origin + emiss_origin
            emissYearly_BplusTplus = emissYearly_BplusTplus + emiss_BplusTplus
            emissYearly_BplusTminus = emissYearly_BplusTminus + emiss_BplusTminus
            emissYearly_BminusTplus = emissYearly_BminusTplus + emiss_BminusTplus
            emissYearly_BminusTminus = emissYearly_BminusTminus + emiss_BminusTminus           
            
    emissYearRecord.at[year-1989]=[year,emissYearly_origin/pow(10,9),emissYearly_BplusTplus/pow(10,9),emissYearly_BplusTminus/pow(10,9),emissYearly_BminusTplus/pow(10,9),emissYearly_BminusTminus/pow(10,9)]

# ----------------------------------print data and results --------------------------------
# yearly emission
tmp = emissYearRecord.copy()
tmp.loc[:36,'B+T+'] = tmp.loc[:36,'BAU']
tmp.loc[:36,'B+T-'] = tmp.loc[:36,'BAU']
tmp.loc[:36,'B-T+'] = tmp.loc[:36,'BAU']
tmp.loc[:36,'B-T-'] = tmp.loc[:36,'BAU']
# tmp.to_excel('../data/data01b_devData/dev05a_Plot_emissCurve/yearlyEmiss.xlsx', sheet_name='yearlyEmiss')

# carbon reduction in 2025
reduce1y_BplusTplus = tmp.loc[37,'B+T+'] - tmp.loc[37,'BAU']
reduce1y_BplusTminus = tmp.loc[37,'B+T-'] - tmp.loc[37,'BAU']
reduce1y_BminusTplus = tmp.loc[37,'B-T+'] - tmp.loc[37,'BAU']
reduce1y_BminusTminus = tmp.loc[37,'B-T-'] - tmp.loc[37,'BAU']

# cumulative carbon emission
cumCarbon = np.cumsum(tmp, axis = 0)
cum_BplusTplus = (cumCarbon.loc[70,'BAU'] - cumCarbon.loc[70,'B+T+']) / cumCarbon.loc[70,'BAU']
cum_BplusTminus = (cumCarbon.loc[70,'BAU'] - cumCarbon.loc[70,'B+T-']) / cumCarbon.loc[70,'BAU']
cum_BminusTplus = (cumCarbon.loc[70,'BAU'] - cumCarbon.loc[70,'B-T+']) / cumCarbon.loc[70,'BAU']
cum_BminusTminus = (cumCarbon.loc[70,'BAU'] - cumCarbon.loc[70,'B-T-']) / cumCarbon.loc[70,'BAU']
# cumCarbon.to_excel('../data/data01b_devData/dev05a_Plot_emissCurve/cumEmiss.xlsx', sheet_name='cumEmiss')

# sum emission after retrofit year
sum_BplusTplus = np.sum(tmp.loc[37:70,'B+T+'])
sum_BplusTminus = np.sum(tmp.loc[37:70,'B+T-'])
sum_BminusTplus = np.sum(tmp.loc[37:70,'B-T+'])
sum_BminusTminus = np.sum(tmp.loc[37:70,'B-T-'])

print('negative carbon emission in 2025: B+T+:%.3f,B+T-:%.3f;B-T+:%.3f;B-T-:%.3f' % (tmp.loc[37,'B+T+'], tmp.loc[37,'B+T-'], tmp.loc[37,'B-T+'], tmp.loc[37,'B-T-']))
print('sum carbon emission since 2025: B+T+:%.1f,B+T-:%.1f;B-T+:%.1f;B-T-:%.1f' % (sum_BplusTplus, sum_BplusTminus, sum_BminusTplus, sum_BminusTminus))
print('cumulative emiss decline percentage: B+T+:{:.1%}; B+T-:{:.1%}; B-T+:{:.1%}; B-T-:{:.1%}' .format(cum_BplusTplus, cum_BplusTminus, cum_BminusTplus, cum_BminusTminus))
print('total carbon reduction: B+T+:%.1f,B+T-:%.1f;B-T+:%.1f;B-T-:%.1f' % (reduce1y_BplusTplus, reduce1y_BplusTminus, reduce1y_BminusTplus, reduce1y_BminusTminus))

# ---------------------------------- plot results -----------------------------------
fig, ax = plt.subplots(dpi=300)
ax.plot(tmp.loc[:,'year'], tmp.loc[:,'BAU'], color = 'black')
ax.plot(tmp.loc[:,'year'], tmp.loc[:,'B-T-'], color = 'red', alpha = 0.8)
ax.plot(tmp.loc[:,'year'], tmp.loc[:,'B+T-'], color = 'orange', alpha = 0.8)
ax.plot(tmp.loc[:,'year'], tmp.loc[:,'B-T+'], color = 'green', alpha = 0.8)
ax.plot(tmp.loc[:,'year'], tmp.loc[:,'B+T+'], color = 'blue')
ax.plot(tmp.loc[:,'year'], tmp.loc[:,'BAU'], color = 'black')
ax.set_ylabel('carbon emissions (Gt)')
labels = ['BAU', 'B-T-', 'B+T-', 'B-T+', 'B+T+']
plt.legend(labels, loc=1, frameon=False, ncol=1, labelspacing=0.3, fontsize=8)
plt.axhline(y=0, color = 'black')

# -------------------------- count technical type ---------------------
scenarioDict = {'B+T+': ppEmiss_BplusTplus, 'B+T-':ppEmiss_BplusTminus,'B-T+':ppEmiss_BminusTplus,'B-T-':ppEmiss_BminusTminus}
scenarioName = ['B+T+', 'B+T-', 'B-T+', 'B-T-']

for i in scenarioName:
    tmp = scenarioDict[i].groupby('techType').count().loc[:,'ID']
    print(i,tmp/np.sum(tmp))    

# --------------------------- economic cost -----------------------
# dataframe: capacity, hours, origin lcoe, B+T+, B+T-, B-T+, B-T-
# tmp = pd.concat([pp_BAU.copy(),scenarioDict['B+T+'].loc[:,'Capacity_kw':'hours']],axis = 1)

tmp = pp_BAU.copy()
for i in scenarioName:
    tmp_a = pd.DataFrame(np.array(scenarioDict[i].loc[:,'lcoe']),columns=[i])
    tmp = pd.concat([tmp,tmp_a],axis =1)

for i in scenarioName:
    strName = 'addCost' + i
    tmp[strName] = tmp['Capacity_k'] * tmp['hours'] * (tmp[i]- tmp['lcoe'])
    print(i,np.sum(tmp[strName])/pow(10,8))

a = tmp.describe().loc['min':'max','B+T+':'B-T-']
plt.boxplot(a)
