__author__ = 'Shalini'


import CSR
import math as mt
import timeit
import hit_ratio
import os


col_ind =[]
row_ptr= [1]
nzero =0
ncol=0
nrow = 0
value=[]
new_col_ind=[]
new_row_ptr=[1]
new_value=[]
each_row_count =[]
col_row= []


print ("Item based Recommndation is in process...... please wait")

Kmost = input("Enter a number for K:")
N = input("Enter a number for N:")
print ("Choose a Similarity")
print ("1. Cosine")
print ("2. Jaccard")

type_sim = input("Enter a number (1 or 2):")


output = raw_input("Enter a name for output file:")
######### Part 1 ############################ ###############################################
  
start = timeit.default_timer()
print ("File open...")

fname = 'train1.txt'

training_matrix = CSR.CSR_format(nrow,ncol,nzero,value,row_ptr,col_ind,each_row_count,col_row)
training_matrix.file_open(fname)

#transpose_matrix =transpose_mat.Transpose(new_row_ptr,new_col_ind,new_value,ncol,nrow,nzero)

#transpose_matrix.transpose_data(training_matrix.col_ind,training_matrix.row_ptr,training_matrix.value)

y =1
each_column_count =[]
new_row_ptr =[1] 

#Transpose
print "Transpose"       
for x in range(1,training_matrix.ncol+1):
    each_column_count.extend([training_matrix.col_ind.count(x)])
    y = y +training_matrix.col_ind.count(x)
    new_row_ptr.extend([y]) 
 
new_col_ind = [0]*training_matrix.nzero
count_flag = [0]*training_matrix.ncol
new_value =  [0]*training_matrix.nzero

for i in range(0,training_matrix.nrow):
    m= training_matrix.row_ptr[i] -1
    n = training_matrix.row_ptr[i+1] -1 
    for j in range(m,n):
        count = training_matrix.col_ind[j]
        z = new_row_ptr[count-1] -1
        x = count_flag[count -1]
        new_col_ind[z+x] = i +1 
        new_value[z+x] = training_matrix.value[j]  
        count_flag[count-1] = count_flag[count-1] +1


###############################################################################################################

Cosine_value_dict={}
cos_sim =[]

def new_list_row(new_col_row2,new_value_row2):
            out = {}
            for k,v in zip(new_col_row2,new_value_row2):
                    out[k] = v
            return out

def row_list(new_col_row2,new_value_row2):
            return [new_list_row(new_col_row2,new_value_row2) for (new_col_row2,new_value_row2) in zip(new_col_row2,new_value_row2)]
        
 
        
print "Similarity Calculations"
new_value_row = []
m = 0
n = 0
for i in range(0,training_matrix.ncol):
    n = each_column_count[i] + n
    new_value_row.extend([new_value[m:n]])
    m = each_column_count[i] +m

new_col_row = []    
for i in range(len(each_column_count)):
        n = new_row_ptr[i]+each_column_count[i] -1
        m = new_row_ptr[i] -1  
        new_col_row.extend([new_col_ind[m:n]])    


if(type_sim ==1):
        new_col_row2 = new_col_row[:]
        new_value_row2 = new_value_row[:]       
        new_col_value = row_list(new_col_row2,new_value_row2)
        
        #if(type_sim ==1):
        
        for i in range(0, len(new_col_value)):
            temp_dict ={}    
            temp_list = []
            for j in range(0, len(new_col_value)):
                count =0
                if new_col_value[i] == new_col_value[j]:
                    pass
                if new_col_value[i] != new_col_value[j]:  
                    value1 =len(new_col_value[i].values())          
                    value2 =len(new_col_value[j].values())
                    for key in new_col_value[i]:
                        if key in new_col_value[j]:
                            count = count + 1
                # print "Sum of similar rating = ",count
                if count > 0:     
                    cos_val = count/(mt.sqrt(value1)*mt.sqrt(value2))
                    #print "Cosine =", float("{0:.3f}".format(cos_val))
                    cosine_value = float("{0:.3f}".format(cos_val))             
                    temp_dict.update({j+1 :cosine_value})
                    temp_list.append([j+1,cosine_value])
                Cosine_value_dict.update({i+1:temp_dict})
            cos_sim.append(temp_list)

if(type_sim ==2):
        
        ncol_list = range(1,training_matrix.ncol+1)
        new_rem_list =[]
        
        
        for v in new_col_row:
          new_rem_list.append(list(set(ncol_list) - set(v)))
                    
        
        for i in range(0,len(new_value_row)):
            for ky in new_rem_list[i]:
                new_value_row[i].insert(ky-1,0)

        new_col_row2 = [ncol_list]*training_matrix.ncol
        new_value_row2 = new_value_row[:]       
        new_col_value = row_list(new_col_row2,new_value_row2)
        
        
        def intersect(list1, list2):
            """ returns the intersection of two lists """
            return [x & y for x,y in zip(list1, list2)]
        
        def union(list1, list2):
            """ returns the union of two lists """
            return [x | y for x,y in zip(list1, list2)]
        
        
        for i in range(0, len(new_col_value)):
            temp_dict ={}    
            temp_list = []
            for j in range(0, len(new_col_value)):
                count =0
                if new_col_value[i] == new_col_value[j]:
                    pass
                if new_col_value[i] != new_col_value[j]:  
                    value1 =sum(intersect(new_col_value[i].values(), new_col_value[j].values()))  
                    value2 =sum(union(new_col_value[i].values(), new_col_value[j].values()))    
                    cos_val = (float(value1)/value2)
                    #print "Cosine =", float("{0:.3f}".format(cos_val))
                    cosine_value = float("{0:.3f}".format(cos_val))             
                    temp_dict.update({j+1 :cosine_value})
                    temp_list.append([j+1,cosine_value])
                Cosine_value_dict.update({i+1:temp_dict})
            cos_sim.append(temp_list)
        
        
#############################################################################################

def sorting(list):
   return [sorted(a, key=lambda p: -p[1]) for a in list]

def similar_items(listA,index):
    for i in range(0,len(listA)):
       if len(listA[i]) < index:
         pass
       if len(listA[i]) >= index:
        listA[i] = listA[i][0:index]
    return listA 

print "K nearest Calculations"
# Knearest calculations
        
K_neighbors = sorting(cos_sim)     # sorting the cosine similarity


#Based on the user input K - get only K items from the sorted list
K_similar_item_new = similar_items(K_neighbors,Kmost) 
stop = timeit.default_timer()
print  "TIME for CSR , Transpose, Similarity Calculations and K nearest",stop - start           
        

########### Part 2 ######################################################################
#        
###Find unrated items for each user  
##
###Each user's Rated Items        

def unrated_list(list2):
  unrate = {}
  for key, val in list2:
    if unrate.get(key, float('-inf')) < val:
        unrate[key] = val

  return [[key, val] for key, val in unrate.items()]



def not_rated_items(list1, list2):
    result = []
    for element in list1:
        if element not in list2:
            result.append(element)
    return result


start1 = timeit.default_timer()



not_rated = range(1, training_matrix.ncol+1)  

col_row_new = training_matrix.col_row[:]

for i in range(0,len(training_matrix.col_row)):
   col_row_new[i] = not_rated_items(not_rated,training_matrix.col_row[i])      # User's Unrated Items
#              



#==============================================================================

new_arr =[]        
# Un rated K most Similar Item for each user
for k, item in enumerate(training_matrix.col_row):
       a = []
       for i in range(0 ,len(K_similar_item_new)) :
          for value in item:
            if i == value -1:
                for item1 in K_similar_item_new[i]:
                  for unratd in col_row_new[k]:
                      if unratd == item1[0]:
                          a.append(item1)
       new_arr.append(a)               
              
# Candiadate Set for each user                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
for i in range(0, len(new_arr)) :
    new_arr[i] = unrated_list(new_arr[i])
                                                                                                                            

#Item id of Candidate set
K_most_similar_unrated = [[item[0] for item in subl] for subl in new_arr]
        
################################################################################



def sum_rating(value):
    if value:
        return value
    else:
        return 0


recommender_items =[]
for i in range(0,len(K_most_similar_unrated)):
    d ={}
    aa = []
    for key in K_most_similar_unrated[i]:
        cos_v = 0.0
        c =0.0
        d = Cosine_value_dict.get(key)
        for key2 in training_matrix.col_row[i]:
            c = sum_rating(d.get(key2))
            cos_v =cos_v + c
        cos_v = float("{0:.3f}".format(cos_v))
        aa.append([key,cos_v])
    recommender_items.append(aa)

recommender_items_sorted = sorting(recommender_items)                                                                                                                   

recommender_items_sorted_N = similar_items(recommender_items_sorted,N) 

print "The Recommendations has been made "


with open("{}\{}.txt".format(os.path.dirname(os.path.abspath(__file__)), output), "w") as my_file: 
#with open("D:\\MS(CIS)\\Sem2\RS\\Assignment\\", "w") as my_file:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
 for j in range(1, training_matrix.nrow+1):
   my_file.write(str(j))  
   for item_val in recommender_items_sorted_N[j-1]:                  
        my_file.write(" ")
        my_file.write(str(item_val[0]))
        my_file.write(" ")
        my_file.write(str(item_val[1]))
   my_file.write("\n")      


stop1 = timeit.default_timer()
print "TIME for Top N recommendations",stop1 - start1


###################################################################

start2 = timeit.default_timer()
print "Hit Calculation is in Progress"


value_test = []
row_ptr_test =[1]
col_ind_test =[]
col_row_test =[]
each_row_count_test =[]
value_count1 = 0





fname1 = 'test1.txt'
test_matrix = CSR.CSR_format(nrow,ncol,nzero,value_test,row_ptr_test,col_ind_test,each_row_count_test,col_row_test)
test_matrix.file_open(fname1)

#######################################################################################################

hit_calc = hit_ratio.Hit(recommender_items_sorted_N,test_matrix.col_row,training_matrix.nrow)
hit_calc.hit_calculation()


stop2 = timeit.default_timer()
print "Metric Calcualtions",stop2 - start2



