# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 16:24:16 2017

@author: tetsuya
"""

import numpy as np

def likelihood(img, px, py, obj_value, Np, sigma2 = 0.01):
    likelihood_arr = []
    for i in range(Np):
        b = (img[py[i],px[i]][0] - obj_value[0]) / 255.0
        g = (img[py[i],px[i]][1] - obj_value[1]) / 255.0
        r = (img[py[i],px[i]][2] - obj_value[2]) / 255.0
        likelihood = np.exp(-(r ** 2 + g ** 2 + b ** 2 ) / (2 * sigma2))
        likelihood_arr.append(likelihood)
    return likelihood_arr