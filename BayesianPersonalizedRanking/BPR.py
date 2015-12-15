# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 20:58:36 2014

@author: Shalini
"""

import CSR
import timeit
import numpy as np
from numpy import random
import sys
import Purchased_items_new
import math
import hit_ratio

print ("BPR with Matrix Factorization")


#==============================================================================
# Part 1. CSR 
#==============================================================================
start = timeit.default_timer()

train = 'train1.txt'

training_matrix = CSR.CSR_format()
training_matrix.file_open(train)

test = 'test1.txt'

testing_matrix = CSR.CSR_format()
testing_matrix.file_open(test)

print ("Training and Test matrix has been loaded")

#==============================================================================
# Based on the user input read / initalize the P and Q matrices
#==============================================================================

print("Select method of loading P and Q :")
print("1. File")
print("2. Initialize P and Q with mean 0 and SD 0.1")
type = input("Enter readPQ or initPQ :")


#==============================================================================
# If the type is readPQ then read the matrix from the file
#==============================================================================
if type=='readPQ':
    pname = input("Enter filename for P as (Pfile xxx) xxx = filename :")
    qname = input("Enter filename for Q as (Qfile xxx) xxx = filename :")
    pname = pname[6:]
    qname = qname[6:]
   # print ("P name", pname)
   # print ("Q name", qname)
   # a = os.path.dirname(os.path.realpath(__file__))
    #f1 = os.path.join(a,pname)
    #f2 = os.path.join(a,pname)
    
    
#==============================================================================
# Loading P and Q matrix from files
#==============================================================================    
    
    flag = False
    P = np.loadtxt(pname)
    Q = np.loadtxt(qname)
    
#==============================================================================
# Checking the size of the P and Q matrix is correct or not    
#==============================================================================
    if (training_matrix.nrow == P.shape[0] and training_matrix.ncol == Q.shape[0] and P.shape[1] == Q.shape[1]):
      K = P.shape[1]
      print ("P and Q matrices are Loaded ")
      flag = True
                 
    if(flag == False):
         print("The P/Q file size is not correct")
         sys.exit()
     
#==============================================================================
# If the type is initPQ then each entry of the matrix should be drawn from
 #   a normal distribution with mean 0 and standard deviation 0.1.
#==============================================================================
if type=='initPQ':  
    K = int(input("Enter the value for K:"))       
    P = random.normal(0, 0.1, (training_matrix.nrow,K))    
    Q = random.normal(0, 0.1, (training_matrix.ncol,K)) 
    print ("P and Q matrices are Loaded ")
    
prediction_old= np.dot(P, Q.T) 

#==============================================================================
# Find the unreated items of each user from the Training matrix to find HR and AHR
#==============================================================================
N = int(input("Enter the value for N:"))
alpha =  float(input("Enter the value for Alpha:"))
lambdau = float(input("Enter the value for Lambda u:"))
lambdai = float(input("Enter the value for Lambda i:"))
lambdaj = float(input("Enter the value for Lambda j:"))

rating = Purchased_items_new.Recommendations_new()
rating.hr_ahr(training_matrix,prediction_old,N)
hit_calc_old = hit_ratio.Hit(rating.Top_N_recommendtions,testing_matrix.rated,training_matrix.nrow)
hit_calc_old.hit_calculation()
print(" K =", K," Alpha =", alpha,"Lambda u =", lambdau,"Lambda i = ", lambdai," Lambda j =", lambdaj," HR =", float("{0:.4f}".format(hit_calc_old.HR)), " AHR =", float("{0:.4f}".format(hit_calc_old.AHR)))



def sigmoid(x):
    dinominator = 1 + math.exp(-x)
    return (1.0/dinominator)


def part1(x1,y1,z1):
  Q_i = Q[y1] 
  Q_j =  Q[z1] 
  rui = np.dot(P[x1],Q_i.T)
  ruj = np.dot(P[x1],Q_j.T)
  ruij = rui - ruj
  term = sigmoid(ruij) - 1
  return term

def P_update(x2,y2,z2):
    term1 = part1(x2,y2,z2)
    term2 = np.subtract(Q[y2],Q[z2])
    term3 = 2 * lambdau * P[x2]
    tmp_p = term1 * term2
    temp_part =np.add(tmp_p ,term3)  
    final_part = alpha * temp_part  
    return np.subtract(P[x2],final_part)
    
def Q_update_Purchased(x3,y3,z3):
    qi_term1 = part1(x3,y3,z3)
    qi_term2 = qi_term1 * P[x3]
    qi_term3 = 2 * lambdai * Q[y3]
    qi_temp_term = np.add(qi_term2 , qi_term3) 
    qi_final_part = alpha * qi_temp_term  
    return np.subtract(Q[y3],qi_final_part) 

def Q_update_notPurchased(x4,y4,z4):
    qj_term1 = part1(x4,y4,z4)
    qj_term2 = qj_term1 * (-P[x4])
    qj_term3 = 2 * lambdaj * Q[z4]
    qj_temp_term =np.add( qj_term2 , qj_term3) 
    qj_final_part = alpha * qj_temp_term 
    return np.subtract(Q[z4],qj_final_part)    
    
sample ='samples_ml100k_0.02_0.005_0.005_0.005_k25.txt'    

ns = 0
with open(sample) as f:  
 start = timeit.default_timer()
 for line in f:     
   pu,qi,qj = [int(s) for s in line.split()] 
   ns = ns+1
   P[pu] = P_update(pu,qi,qj)  
   Q[qi] = Q_update_Purchased(pu,qi,qj)
   Q[qj] = Q_update_notPurchased(pu,qi,qj)
   if (ns % (training_matrix.nzero * 100) ) == 1:
       prediction = np.dot(P,Q.T)  
       rating_one = Purchased_items_new.Recommendations_new()
       rating_one.hr_ahr(training_matrix,prediction,N)
       hit_calc = hit_ratio.Hit(rating_one.Top_N_recommendtions,testing_matrix.rated,training_matrix.nrow)
       hit_calc.hit_calculation()
       stop = timeit.default_timer()
       print(" K =", K," Alpha =", alpha,"Lambda u =", lambdau,"Lambda i = ", lambdai," Lambda j =", lambdaj,"HR =",float("{0:.4f}".format(hit_calc.HR)), " AHR =", float("{0:.4f}".format(hit_calc.AHR)),"Learning time = ", float("{0:.4f}".format(stop-start)))
  
      

