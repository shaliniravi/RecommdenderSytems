# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 15:24:22 2014

@author: Shalini
"""

import CSR
import timeit
import Transpose
import numpy as np
import Nonzero
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


#==============================================================================
# Remove bias from Training matrix and Finding the maximum and minimum ratings
#==============================================================================
 
maxR = max(training_matrix.value)
minR = min(training_matrix.value)
mean_value = np.mean(training_matrix.value)
bias_value = np.array(training_matrix.value)
bias_value =  (bias_value - mean_value).tolist()        
training_matrix.value = bias_value

#==============================================================================
# Transspose  
#==============================================================================

transpose_matrix = Transpose.TransposeMatrix(training_matrix.nrow,training_matrix.ncol,training_matrix.nzero)
transpose_matrix.transpose_mat(training_matrix.col_ind,training_matrix.row_ptr,training_matrix.value)

stop = timeit.default_timer()
print ("CSR and Transpose has been done")
print ("Time Taken for CSR and Transspose " ,stop - start)



#==============================================================================
# To find the column index and non zero value for each row  
#==============================================================================

nonzero_R = Nonzero.NonZero()
nonzero_R.valueAt(training_matrix.row_ptr,training_matrix.col_ind,training_matrix.value)
training_matrix.col_row = nonzero_R.col_row
training_matrix.value_row = nonzero_R.value_row
       
nonzero_T = Nonzero.NonZero()
nonzero_T.valueAt(transpose_matrix.row_ptr,transpose_matrix.col_ind,transpose_matrix.value)
transpose_matrix.col_row = nonzero_T.col_row
transpose_matrix.value_row = nonzero_T.value_row

#==============================================================================
# Part 2. Getting User Input for
# 1. K (the latent dimension), 
# 2. CP (the control parameter) 
# 3. maxIters (the maximum number of iterations allowed) and 
# 4. E - epsilon (the ratio of objective value change)
#==============================================================================

K = int(input("Enter the Latent Dimension(K) :"))
CP = float(input("Enter the value for Control Parameter (Lambda):"))
maxIters = int(input("Enter the the maximum number of iterations to be allowed :"))
Ep =float(input("Enter the value for Epsilon :"))

#==============================================================================
# Part 3. Initialize dense factor matrix P and Q with 1/k
#==============================================================================
start0 = timeit.default_timer()
P = np.empty((training_matrix.nrow,K))
P.fill(1/K)

Q = np.empty((training_matrix.ncol,K))
Q.fill(1/K)

#==============================================================================
# Part 4. Matrix  Factorization 
#==============================================================================
def LS_Closed(X,Y,kvalue,lvalue): 
    result = []
    for i in range(0,X.nrow):
        a = 0 
        f = 0
        I = np.identity(kvalue)
        for k,v in enumerate(X.col_row[i]):
            b = X.value_row[i][k] * np.array(Y[v-1])[np.newaxis]
            a = np.add(a,b)
            c = np.array(Y[v-1])[np.newaxis]
            e = c.transpose() * c
            f = np.add(f,e)      
        h = lvalue * I
        l = np.add(f,h) 
        g = np.dot(a,np.linalg.inv(l))
        result.append(g[0].tolist())
    return np.array(result)
    


func=[]
def func_cal(R,A,B,lampd_value):
    res = 0
    B =B.transpose()
    for i in range(0,R.nrow) :
        for k,v in enumerate(R.col_row[i]):
               b = R.value_row[i][k]         
               res = res + pow(b - np.dot(A[i,:],B[:,v-1]), 2)    
    final = res + lampd_value * ((np.square(A)).sum() + (np.square(B)).sum() ) 
    func.extend([final])        


for maxrun in range(0,maxIters):
    P = LS_Closed(training_matrix,Q,K,CP)
    Q = LS_Closed(transpose_matrix,P,K,CP)
    func_cal(training_matrix,P,Q,CP)
    if (maxrun > 0  and (abs(func[maxrun] - func[maxrun -1]) / func[maxrun -1] ) < Ep ):
        print ("Threshold Epsilon has been reached")
        break

      
            
stop0 = timeit.default_timer()     
 
#==============================================================================
# Part 5. Generate the recommendations - MSE and RMSE Calculations  
#==============================================================================

start1 = timeit.default_timer()

MSE = 0.0
RMSE = 0.0
fname1 = 'test.txt'

testing_matrix = CSR.CSR_format()
testing_matrix.file_open(fname1)

nonzero_R = Nonzero.NonZero()
nonzero_R.valueAt(testing_matrix.row_ptr,testing_matrix.col_ind,testing_matrix.value)
testing_matrix.col_row = nonzero_R.col_row
testing_matrix.value_row = nonzero_R.value_row


Q = Q.transpose()
for i in range(0,testing_matrix.nrow):
    for k,v in enumerate(testing_matrix.col_row[i]):
            pred = np.dot(P[i,:],Q[:,v-1]) + mean_value
            if pred > maxR:
                pred = maxR
            if pred < minR:
                pred = minR
            MSE = MSE + pow(testing_matrix.value_row[i][k]- pred, 2)
            
            
MSE = MSE / testing_matrix.nzero
RMSE = math.sqrt(MSE)

stop1 = timeit.default_timer()

time1 = stop0 - start0
time2 = stop1 - start1

print ("***********************************")
print ( "K  = " ,K)
print ( "Lambda = " ,CP)
print ( "Maximum Iterations  = " ,maxIters)
print ( "Epsilon = " ,Ep)
print ( "MSE = " ,MSE)
print ( "RMSE = " ,RMSE)
print (" Time Taken For Training Matrix =", time1)
print (" Time Taken For Testing Matrix =", time2)
print ("***********************************")

                                                                                                                                       

del(testing_matrix)
del(training_matrix)
del(transpose_matrix)
del(P)
del(Q)
del(nonzero_R)
del(nonzero_T)
