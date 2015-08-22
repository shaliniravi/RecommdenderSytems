__author__ = 'Shalini'


class CSR_format:
    
    def __init__(self,nrow,ncol,nzero,value,row_ptr,col_ind,each_row_count,col_row):

        self.nrow =nrow
        self.ncol =ncol
        self.value =value
        self.row_ptr = row_ptr
        self.col_ind = col_ind
        self.each_row_count= each_row_count
        self.col_row =col_row
        
         
    def file_open(self,fname):
      with open(fname) as f:  
        line = next(f)
        line = line.split()
        line = [int(i)for i in line]
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
            self.col_row.extend([self.col_ind[m:n]])
            
 
    
           