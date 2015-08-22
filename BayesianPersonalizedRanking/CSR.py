

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 09:35:45 2014

@author: Shalini
"""


class CSR_format:
    
    def __init__(self):

        self.nrow =0
        self.ncol =0
        self.nzero =0
        self.value =[]
        self.row_ptr = [1]
        self.col_ind = []
        self.value_row =[]
        self.each_row_count= []
        self.rated =[]
        
         
    def file_open(self,fname):
      with open(fname) as f:  
        line = next(f)
        line = line.split()
        line = [int(i) for i in line]
        self.nrow = line[0]
        self.ncol = line[1]
        self.nzero = line[2]
                        
        for line in f:
            countr = 1
            line = line.split() 
            line = [int(i) for i in line]
            for x in range(len(line)):
               if x%2 != 0:
                    self.value.extend([line[x]])
                    self.col_ind.extend([line[x-1]])
            countr =countr+ len(self.value)
            self.row_ptr.extend([countr])


      m = 0
      n = 0

      for y in range(len(self.row_ptr) -1):
        value_count = self.row_ptr[y+1] - self.row_ptr[y]
        self.each_row_count.extend([value_count])
                            
      for i in range(len(self.each_row_count)):
            n = self.row_ptr[i]+self.each_row_count[i] -1
            m = self.row_ptr[i] -1  
            self.rated.extend([self.col_ind[m:n]])
            
      
      
      
    
           