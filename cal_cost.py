# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 11:15:06 2022

@author: vicke
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def LCOE_PP(C, H, operateYear, retrofitYear):

    lcoe = 0.0
    
    if retrofitYear - operateYear >= 40: 
        lcoe = 0.0
        
    else: 
        r = 1 + 0.08  # rate
        lifespan = 40        
        
        Cap_PP = 3274 * C # CAPEX = 3274 $/kw
        OM_PP = (41.66 + 31.35) * C   # O & M = 41.66 + 31.35 $/kw
        Fuel_PP = C * H * 11.45 / pow(10,6)  # coal price = 11.45/MWh
        Debt_PP = Cap_PP * 0.0 # debt rate = 10% 
        D_PP = 0.05 * Cap_PP # depricition rate = 5%
        
        Elec = C * H
        r = 1 + 0.05
        lifespan = 40
        
        LF_0 = 0
        LF_1 = 0
        # lcoeFrame = np.zeros(shape = (lifespan, 2))
        for i in range(lifespan):
            cost_i = 0
            if i == 0:
                cost_i = (Cap_PP + OM_PP + Fuel_PP + Debt_PP) / pow(r, i+1)
            if i < 10 and i > 0:
                cost_i = (OM_PP + Fuel_PP + Debt_PP) / pow(r, i+1)
            if i >= 10 and i < lifespan-1:
                cost_i = (OM_PP + Fuel_PP) / pow(r, i+1)
            if i == lifespan - 1:
                cost_i = (OM_PP + Fuel_PP - D_PP) / pow(r, i+1)
                
            LF_0 += cost_i
            LF_1 += Elec / pow(r, i+1)

        lcoe = LF_0/LF_1      

    return lcoe


def LCOE_BECCS(C, H, Sum_j_xij_kwh, Sum_j_DBxij, Dccs, operateYear, retrofitYear):
    
    lcoe = 0.0
    
    if retrofitYear - operateYear >= 40:
        lcoe = 0.0
    
    else:
        Cap_PP = 3274 * C # CAPEX = 3274 $/kw
        OM_PP = (41.66 + 31.35) * C   # O & M = 41.66 + 31.35 $/kw
        Fuel_PP = C * H * 11.45 / pow(10,3)  # coal price = 11.45/MWh
        Debt_PP = Cap_PP * 0.0 # debt rate = 10% 
        D_PP = 0.05 * Cap_PP # depricition rate = 5%
        
        Cap_BE = 327.2 * C
        OM_BE = (18.85+27.5) * C
        Fuel_BE = (10.3 + 6.15 + 6.75) * C * H/pow(10,3) + Sum_j_DBxij * 0.065 / pow(10,3)
        Debt_BE = Cap_BE * 0.0
        D_BE = Cap_BE * 0.05
        
        Cap_CCS = 1559.75 * C
        Emiss_CO2 = C * H * 0.801 / pow(10,3)  # 0.801 t/MWh
        OM_CCS = Emiss_CO2 * (40 + 17.39) + Emiss_CO2 * Dccs * 0.1195
        Debt_CCS = 0.0 * Cap_CCS
        D_CCS = 0.05 * Cap_CCS
        
        add_Cap = Cap_BE + Cap_CCS
        add_OM = OM_BE + OM_CCS
        Fuel_BE_PPpart = C * H * 11.45 / pow(10,3) - Sum_j_xij_kwh * 11.45 / pow(10,3)
        add_Fuel =  Fuel_BE_PPpart + Fuel_BE - Fuel_PP # coal reduction cost and biomass cost
        add_Debt = Debt_BE + Debt_CCS
        add_D = D_BE + D_CCS
    
        Elec = C * H
        r = 1 + 0.05
        lifespan = 40
        
        retrofit_i = retrofitYear - operateYear -1 # 发生改造的i 
        
        # lcoeFrame = np.zeros(shape = (lifespan, 2))
        LF_0 = 0
        LF_1 = 1
        for i in range(lifespan):
            cost_i = 0
            if i == 0:
                cost_i = (Cap_PP + OM_PP + Fuel_PP + Debt_PP) / pow(r, i+1)
            if i < 10 and i > 0:
                cost_i = (OM_PP + Fuel_PP + Debt_PP) / pow(r, i+1)
            if i >= 10 and i < lifespan-1:
                cost_i = (OM_PP + Fuel_PP) / pow(r, i+1)
            if i == lifespan - 1:
                cost_i = (OM_PP + Fuel_PP - D_PP) / pow(r, i+1)
    
            
            # 判断改造情况
            if i < retrofit_i:
                cost_i = cost_i        
            if i == retrofit_i:  # 改造第一年
                cost_i = cost_i + (add_Cap + add_OM + add_Fuel + add_Debt) / pow(r, i+1)
            if i < (retrofit_i + 10) and i > retrofit_i:
                cost_i = cost_i + (add_OM + add_Fuel + add_Debt) / pow(r, i+1)
            if i >= (retrofit_i + 10) and i < lifespan - 1:
                cost_i = cost_i + (add_OM + add_Fuel) / pow(r, i+1)
            if i == lifespan - 1:
                cost_i = cost_i + (add_OM + add_Fuel - add_D) / pow(r, i+1)
    
            LF_0 += cost_i
            LF_1 += Elec / pow(r, i+1)
            # lcoeFrame[i][0] = cost_i
            # lcoeFrame[i][1] = Elec / pow(r, i+1)
        
        # sumFrame = np.sum(lcoeFrame , axis = 0)
        # lcoe = sumFrame[0] / sumFrame [1]
    
        lcoe = LF_0/LF_1
    
    return lcoe