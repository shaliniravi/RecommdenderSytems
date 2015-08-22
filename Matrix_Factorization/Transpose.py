# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 09:37:18 2014

@author: Shalini
"""

class TransposeMatrix:
    
    def __init__(self,nrow,ncol,nzero):
    
        
        self.ncol=nrow
        self.nrow =ncol
        self.nzero = nzero
        self.value =[]
        self.row_ptr = [1]
        self.col_ind = []
        self.col_row =[]
        self.value_row =[]
       # self.each_column_count= []

        
    def transpose_mat(self,col_ind_old,row_ptr_old,value_old):
        y =1      
        for x in range(1,self.nrow+1):
            #self.each_column_count.extend([col_ind.count(x)])
            y = y +col_ind_old.count(x)
            self.row_ptr.extend([y]) 
        
        self.col_ind =[0]* self.nzero
        count_flag = [0]*self.nrow
        self.value = [0]*self.nzero
        
        for i in range(0,self.ncol):
            m= row_ptr_old[i] -1
            n = row_ptr_old[i+1] -1 
            for j in range(m,n):
                count = col_ind_old[j]
                z = self.row_ptr[count-1] -1
                x = count_flag[count -1]
                self.col_ind[z+x] = i +1 
                self.value[z+x] = value_old[j]  
                count_flag[count-1] = count_flag[count-1] +1
    
            