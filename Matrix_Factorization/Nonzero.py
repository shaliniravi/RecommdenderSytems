# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 16:55:23 2014

@author: Shalini
"""

class NonZero:
    def __init__(self):
        self.col_row =[]
        self.value_row =[]
        
        
    def valueAt(self,row_ptr,col_ind,value):
        for i in range (1,len(row_ptr)):
            a =[]
            b =[]
            for j in range (row_ptr[i-1],row_ptr[i]):
                a.extend([col_ind[j-1]])
                b.extend([value[j-1]])
            self.col_row.append(a) 
            self.value_row.append(b)