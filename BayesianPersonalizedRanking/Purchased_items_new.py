# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 00:21:51 2014

@author: Shalini
"""


class Recommendations_new:
    def __init__(self):
        self.HR_val = 0
        self.AHR_val = 0
        self.Top_N_recommendtions = []

    

    
    def sorting(self,listA):
       return [sorted(a, key=lambda p: -p[1]) for a in listA]
       
    
    def topN(self,listA,index):
        for i in range(0,len(listA)):
            listA[i] = listA[i][0:index]
        return listA 
    

    def hr_ahr(self,training_matrix,pred,N):

        for key, value in enumerate (training_matrix.rated):
             for item in value:
                 pred[key][item-1] = float('-inf')

        recommednation_list = []         
        for key1, value1 in enumerate(pred):
            temp_list=[]
            for k ,val in enumerate(value1):
                if val != float('-inf'):
                  temp_list.append([k, val])
            recommednation_list.append(temp_list)
        
        candidates = self.sorting(recommednation_list) 
        new_candidates = candidates[:]
        self.Top_N_recommendtions = self.topN(new_candidates,N)
        
        
       
