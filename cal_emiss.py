# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 14:29:07 2021

@author: DELL
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def Emiss_PP(C, H, OY, RY):

    emiss = (275.1 + 14.8 + 801.7) * C * H / pow(10,6) # unit: tonne
    if RY - OY > 40:
        emiss = 0
    return emiss


def Emiss_BECCS(C,H,Sum_j_xij_kwh,Sum_j_DBxij, OY, RY):

    cofiringRatio = Sum_j_xij_kwh / (C*H)
    coalEmiss = (275.1 + 14.8 + 0.1* 801.7) * C * H * (1-cofiringRatio) / pow(10,6) 
    bio_processEmiss = (2.36 + 1.1 + 0.295 + 2.457) * Sum_j_xij_kwh / pow(10,6) + 0.009 * Sum_j_DBxij / pow(10,6)
    bio_absorb = 375.72 * Sum_j_xij_kwh * 0.9 / pow(10,6)  # capture 90% emission
    emiss = coalEmiss + bio_processEmiss - bio_absorb
    if RY - OY > 40:
        emiss = 0
    return emiss
