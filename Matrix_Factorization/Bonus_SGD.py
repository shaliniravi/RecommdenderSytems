# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 16:26:59 2014

@author: Shalini
"""


import CSR
import timeit
import numpy as np
import math

print ("Matrix Factorization")


#==============================================================================
# Part 1. CSR 
#==============================================================================
start = timeit.default_timer()
print ("File open...")

fname = 'train.txt'

training_matrix = CSR.CSR_format()
training_matrix.file_open(fname)


maxR = max(training_matrix.value)
minR = min(training_matrix.value)
mean_value = np.mean(training_matrix.value)
bias_value = np.array(training_matrix.value)
bias_value =  (bias_value - mean_value).tolist()        
training_matrix.value = bias_value


def elementAT(matrix,row_num,col_num):
 for y in range(matrix.row_ptr[row_num],matrix.row_ptr[row_num+1]):
     if (matrix.col_ind[y-1] == col_num):
         return matrix.value[y-1]
 return 0       
     
#==============================================================================
# Part 2. Getting User Input for
# 1. K (the latent dimension), 
# 2. CP (the control parameter) 
# 3. maxIters (the maximum number of iterations allowed) and 
#==============================================================================

K = int(input("Enter the Latent Dimension(K) :"))
CP = float(input("Enter the value for Control Parameter (Lambda):"))
maxIters = int(input("Enter the the maximum number of iterations to be allowed :"))


#==============================================================================
# Part 3. Initialize dense factor matrix P and Q with 1/k
#==============================================================================


P = np.empty((training_matrix.nrow,K))
P.fill(1/K)

Q = np.empty((training_matrix.ncol,K))
Q.fill(1/K)

#==============================================================================
# Part 4. Matrix  Factorization  - SGD
#==============================================================================

def MH_SGD(R, W, H, kvalue, maxIteration, lvalue, alpha):
    for maxrun in range(0,maxIteration):
        for i in range(0,R.nrow):
           for j in range(0,R.ncol):
               val =elementAT(R,i,j+1)
               val_new = 0
               if val > 0:
                 for xy in range(0, kvalue):
                   val_new = val_new + np.dot(W[i,xy],H[j,xy])
                 eui = val - val_new
                 for yx in range(0, kvalue):
                     W[i,yx] = W[i,yx] + alpha * (eui * H[j][yx] - lvalue * W[i][yx])
                     H[j,yx] = H[j,yx] + alpha * (eui * W[i][yx] - lvalue * H[j][yx])
    return W, H.transpose()           
  

new_P, new_Q = MH_SGD(training_matrix, P, Q, K, maxIters ,CP,alpha = 0.00009)



#==============================================================================
# Part 5. Generate the recommendations - MSE and RMSE Calculations  
#==============================================================================

MSE = 0.0
RMSE = 0.0
fname1 = 'test.txt'

testing_matrix = CSR.CSR_format()
testing_matrix.file_open(fname1)


pred = np.dot(new_P,new_Q)

for i in range(0,testing_matrix.nrow):
    for j in range (0,testing_matrix.ncol):
            rating = elementAT(testing_matrix,i,j+1) 
            if rating > 0:
                prediction = pred[i][j] + mean_value
                if prediction > maxR:
                    prediction = maxR
                if prediction < minR:
                    prediction = minR
                MSE = MSE + pow(rating- prediction, 2)
            
            
MSE = MSE / testing_matrix.nzero
RMSE = math.sqrt(MSE)


print ("*********Bonus SGD **************************")
print ( "K  = " ,K)
print ( "Lambda = " ,CP)
print ( "Maximum Iterations  = " ,maxIters)
print ( "MSE = " ,MSE)
print ( "RMSE = " ,RMSE)
print ("***********************************")


del(testing_matrix)
del(training_matrix)
del(new_P)
del(new_Q)