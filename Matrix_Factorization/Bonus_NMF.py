# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 16:26:59 2014

@author: Shalini
"""


import CSR
import timeit
import numpy as np
import math
import Nonzero

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
#mean_value = np.mean(training_matrix.value)
#bias_value = np.array(training_matrix.value)
#bias_value =  (bias_value - mean_value).tolist()        
#training_matrix.value = bias_value
  
nonzero_R = Nonzero.NonZero()
nonzero_R.valueAt(training_matrix.row_ptr,training_matrix.col_ind,training_matrix.value)
training_matrix.col_row = nonzero_R.col_row
training_matrix.value_row = nonzero_R.value_row
            
     
#==============================================================================
# Part 2. Getting User Input for
# 1. K (the latent dimension), 
# 2. CP (the control parameter) 
# 3. maxIters (the maximum number of iterations allowed) and 
#==============================================================================

K = int(input("Enter the Latent Dimension(K) :"))
CP = float(input("Enter the value for Control Parameter (Lambda):"))
maxIters = int(input("Enter the the maximum number of iterations to be allowed :"))
Ep =float(input("Enter the value for Epsilon :"))

#==============================================================================
# Part 3. Initialize dense factor matrix P and Q with 1/k
#==============================================================================

P = np.empty((training_matrix.nrow,K))
P.fill(1/K)

Q = np.empty((training_matrix.ncol,K))
Q.fill(1/K)

#==============================================================================
# Part 4. Matrix  Factorization  - Non Negative MF
#==============================================================================
                 
def func_cal(X,A,B,beta,Kval):
 res = 0
 for i in range(0,X.nrow):
     for k,v in enumerate(X.col_row[i]):
       val = X.value_row[i][k]
       if val > 0:
            res = res + pow(val - np.dot(A[i,:],B[:,v-1]), 2)
            for x in range(0,Kval):
                res = res + (beta/2) * ( pow(A[i][x],2) + pow(B[x][v-1],2) )
 return res

def MF_NFM(R, W, H, kvalue, maxIteration, lvalue, beta): 
    H = H.transpose()
    for maxrun in range(0,maxIteration):
        for i in range(0,R.nrow):
             for k,v in enumerate(R.col_row[i]):
               val = R.value_row[i][k]
               if val > 0:
                    val_new = val - np.dot(W[i,:],H[:,v-1])
                    for xy in range(0,K):
                        W[i][xy] = W[i][xy] + lvalue * (2 * val_new * H[xy][v-1] - beta * W[i][xy])
                        H[xy][v-1] = H[xy][v-1] + lvalue * (2 * val_new * W[i][xy] - beta * H[xy][v-1])
    
         
        if func_cal(R,W,H,beta,kvalue) < Ep:
            break
    return W, H
 
new_P, new_Q = MF_NFM(training_matrix, P, Q, K, maxIters ,CP,beta = 0.5)



#==============================================================================
# Part 5. Generate the recommendations - MSE and RMSE Calculations  
#==============================================================================

MSE = 0.0
RMSE = 0.0
fname1 = 'test.txt'

testing_matrix = CSR.CSR_format()
testing_matrix.file_open(fname1)

nonzero_R = Nonzero.NonZero()
nonzero_R.valueAt(testing_matrix.row_ptr,testing_matrix.col_ind,testing_matrix.value)
testing_matrix.col_row = nonzero_R.col_row
testing_matrix.value_row = nonzero_R.value_row


pred = np.dot(new_P,new_Q)

for i in range(0,testing_matrix.nrow):
       for k,v in enumerate(testing_matrix.col_row[i]):
                rating = testing_matrix.value_row[i][k] 
                prediction = np.dot(new_P[i,:],new_Q[:,v-1]) 
                if prediction > maxR:
                    prediction = maxR
                if prediction < minR:
                    prediction = minR
                MSE = MSE + pow(rating - prediction, 2)
            
            
MSE = MSE / testing_matrix.nzero
RMSE = math.sqrt(MSE)


print ("**************Bonus NMF *********************")
print ( "K  = " ,K)
print ( "Lambda = " ,CP)
print ( "Maximum Iterations  = " ,maxIters)
print ( "MSE = " ,MSE)
print ( "RMSE = " ,RMSE)
print ("***********************************")



