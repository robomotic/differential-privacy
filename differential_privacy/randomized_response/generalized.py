#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class implements the generalized randomized response.

Papers used as reference:

@inproceedings{Wang2016UsingRR,
  title={Using Randomized Response for Differential Privacy Preserving Data Collection},
  author={Yue Wang and Xintao Wu and Donghui Hu},
  booktitle={EDBT/ICDT Workshops},
  year={2016}
}

"""

__version__ = '0.1.0'
__author__ = 'Paolo Di Prodi <paolo@robomotic.com>'
__all__ = []

import math
import warnings
from typing import Dict, Tuple, Sequence

class GeneralRandomizedResponse():
    '''
    Suppose there are n individuals C_1,...,C_n and each individual C_i has a private binary value x_i in {0,1} regarding
    a sensitive binary attribute X. To ensure privacy, each individual C_i sends to the untrusted curator a modified version
    y_i of the x_i. Using the randomized response, the server can collect perturbed data from individuals.

    '''

    def __init__(self,p_00:float=.5,p_01:float=.5,p_10:float=.5,p_11:float=.5)->None:
        '''
        Constructor where p_uv= P[y_i = u | x_i = v] and u,v in {0,1} denotes the probability that the random output
        is u when the real attribute value x_i for C_i is v; here p_uv in (0,1).
        The sum of probabilities for each colum and row is 1.

        :param p_00: P[y_i = 0 | x_i = 0]
        :param p_01: P[y_i = 0 | x_i = 1]
        :param p_10: P[y_i = 1 | x_i = 0]
        :param p_11: P[y_i = 1 | x_i = 1]
        '''

        # check probability bounds
        if p_00>1.0 or p_00<0.0:
            raise Exception('Probability must be within range [0,1]')
        if p_01>1.0 or p_01<0.0:
            raise Exception('Probability must be within range [0,1]')
        if p_10>1.0 or p_10<0.0:
            raise Exception('Probability must be within range [0,1]')
        if p_11>1.0 or p_11<0.0:
            raise Exception('Probability must be within range [0,1]')

        # check that everything sums to 1
        if p_00 + p_01 != 1.0:
            raise Exception('Probability must sum to 1')
        if p_10 + p_11 != 1.0:
            raise Exception('Probability must sum to 1')

        if p_00 == p_11 == 1.0:
            warnings.warn('This is equivalent to direct questioning')

        # P is a 2x2 design matrix row by row
        self._P = [[p_00,p_01],[p_10,p_11]]

    def set_optimal_utility(self,eps:float)->None:
        '''
        Set optimal design matrix based on epsilon parameter
        :param eps: the epsilon parameter
        :return: None
        '''

        p_00 = p_11 = math.exp(eps)/(1+ math.exp(eps))
        p_01 = p_10 = 1/(1+ math.exp(eps))

        # change P
        self._P = [[p_00,p_01],[p_10,p_11]]

    def check_eps_privacy(self,eps:float,tol:float=0)->bool:
        '''
        Check that the design matrix is eps-differentially private
        :param eps: the epsilon parameter
        :return: true if satisfied
        '''

        if eps < 0.0: raise Exception('Epsilon cannot be negative')

        if self._P[0][1] == .0:
            p = float("inf")
        else:
            p = self._P[0][0] / self._P[0][1]

        if self._P[1][0] == .0:
            q = float("inf")
        else:
            q = self._P[1][1] / self._P[1][0]

        if max(p,q) <= math.exp(eps)+tol: return True
        else: return False

    def get_P_X_mass(self,pi_0:float=None,pi_1:float=None)->Dict[str, float]:
        '''

        :param pi_0: true proportion of individuals without sensitive attribute
        :param pi_1: true proportion of individuals with sensitive attribute
        :return:
        '''
        mass = {'P(Y=0)':None,'P(Y=1)':None}

        if pi_0 is not None: pi_1 = 1.0 - pi_0
        if pi_1 is not None: pi_0 = 1.0 - pi_1

        mass['P(Y=0)'] = pi_0 * self._P[0][0] + pi_1 * self._P[0][1]
        mass['P(Y=1)'] = pi_1 * self._P[1][1] + pi_0 * self._P[1][0]

        return mass

    def get_unbiased_mean_estimator(self,lambda_0:float=None,lambda_1:float=None)->Dict[str, float]:
        '''
        We use pi_0 (pi_1) to describe the true proportion of value 0 (1)
        We use pihat_0 (pihat_1) to described the unbiased estimator for pi_0 (pi_1)
        We use lambda_0 (lambda_1) to describe the observed proportion of value 0 (1)

        :return: A dictiionary with he unbiased estimators pihat_0, pihat_1
        '''

        _ = {'pihat_0':None,'pihat_1':None}
        if lambda_0 is not None:
            if lambda_0 >=.0 and lambda_0<=1.0:
                _['pihat_0'] = (self._P[0][0] - 1.0 )/ (2* self._P[0][0] -1) + lambda_0/(2* self._P[0][0] -1)
            else: raise Exception('This is not a probability')

        if lambda_1 is not None:
            if lambda_1 >= .0 and lambda_1 <= 1.0:
                _['pihat_1'] = (self._P[0][0] - 1.0 )/ (2* self._P[0][0] -1) + lambda_1/(2* self._P[0][0] -1)
            else: raise Exception('This is not a probability')

        return _

    def get_unbiased_variance_estimator(self):
        pass







