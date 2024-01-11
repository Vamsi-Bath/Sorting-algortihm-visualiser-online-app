import random
from functools import reduce 
from operator import mul
import numpy


def reshape(lst, shape):
    if len(shape) == 1:
        return lst
    n = reduce(mul, shape[1:])
    return [reshape(lst[i*n:(i+1)*n], shape[1:]) for i in range(len(lst)//n)]

def Bubble_Sort_Passes(array):

    n=len(array)
    swapped=True
    newarr=[]                             # creating a new array
    newlist=[]
    while n>0 and swapped==True:            # This will loop contiuously until no swaps in the array has been made
        swapped=False 
        n-=1
        for index in range(0,n):
            if array[index]>array[index+1]:
                temp=array[index]
                array[index]=array[index+1]
                array[index+1]=temp
                swapped=True                           # exit loop if 1 swap has been made
                                           
        newarr.extend(array)                               # ADD the current pass at this stage and add it to the new array we have created
    newarr=reshape(newarr,(len(array),len(array)))                              

    for i in newarr:
        if i not in newlist:               # Remove any Duplicate passes
            newlist.append(i)
    return newlist                        # Return Value


def Insertion_Sort_Passes(array):
  passes=[]                                # Creating a new array
  for i in range(0, len(array)):
    newarray=array
    index = array[i] 
    while i > 0 and index < array[i - 1]:    
                     
      array[i] = array[i - 1]                 #Swapping the items around

      i = i - 1                           #Swappinfg
      array[i] = index
    passes.extend(newarray)                                   # add the current pass and add it to the new array we have created
           
  passes=reshape(passes,((len(array),len(array),len(array))))                  # converting 1D TO 2d
  passes=passes[0][1:]                  #Duplicate is created at the start
  return passes




def writeRandomized(length):
    with open("Random_Array.txt", "w" ) as afile:      #    This function will generate a random array for us to use and write it in a text file called random array
        for i in range(length):
            line = str(random.randint(1, 30))    # our values should between (1,30)
            afile.write(line)
            afile.write('\n')
       

def readRandomized():
    with open('Random_Array.txt','r') as afile:                      # This Function will read the contents of the file we have just written to
        alist = [int(line.rstrip()) for line in afile] 
    return list(alist)



def chooserandompass(mode):                       # We will choose our gamemode which will be passed as a string 

    ReadArray=readRandomized()         #Store what's is written in the Random_Array text file 

    if mode=='Practice_Bubble':   #<---example game mode
        with open('SortingType.txt','w') as f3:
                PassCollect=Bubble_Sort_Passes(ReadArray)
                idx, val = {i: PassCollect[i] for i in [random.randrange(len(PassCollect))]}.popitem()
                f3.write('BUBBLE SORT TO PASS')
                
        
    elif mode=='Practice_Insertion':
        with open('SortingType.txt','w') as f3:     # We are writing to a new text file called sortingType Which will specify what type of sorting algorithm we will use
                PassCollect=Insertion_Sort_Passes(ReadArray)
                idx, val = {i: PassCollect[i] for i in [random.randrange(len(PassCollect))]}.popitem()
                f3.write('INSERTION SORT TO PASS')  # This is the text that will be written to this text file.   specifed by the sorting type
         
    elif mode == 'Randomized_Competitive':       #This is our randomized mode
        
        sortlist=['I','B']                        # Randomly choose between bubble sort or insertion sort.
        PassCollect=random.choice(sortlist)
        with open('SortingType.txt','w') as f3:
            if PassCollect=='I':
                PassCollect=Insertion_Sort_Passes(ReadArray)
                idx, val = {i: PassCollect[i] for i in [random.randrange(len(PassCollect))]}.popitem()            # This idx will return the index of what pass has been randomly selected
                f3.write('INSERTION SORT TO PASS')

            if PassCollect=='B':
                PassCollect=Bubble_Sort_Passes(ReadArray)
                idx, val = {i: PassCollect[i] for i in [random.randrange(len(PassCollect))]}.popitem()
                f3.write('BUBBLE SORT TO PASS')  

    print("index {} pass {}" .format(idx+1, val))
    
    with open('PassNumber.txt','w') as f1:            # creating a textfile to store our pass number
        f1.write(str(idx+1))           # we will write the pass number to this text file

    numpy.savetxt('PassArray.txt', val)              # creating another textfile which will store the the array that has been randomly chosen from the collection of passes
    
    return val                    # to check if everything is running correctly, i will return the index and value in a tuple anc check.  After, i am just going to return val


def chooserandompass2(mode):

    ReadArray=readRandomized()
    if mode=='Practice_Bubble':
        with open('SortingType.txt','w') as f3:
                PassCollect=Bubble_Sort_Passes(ReadArray)
                idx, val = {i: PassCollect[i] for i in [random.randrange(len(PassCollect))]}.popitem()
                f3.write('TYPE WHAT PASS THIS IS: BUBBLE (RIGHT SIDE)')
                
        
    elif mode=='Practice_Insertion':
        with open('SortingType.txt','w') as f3:
                PassCollect=Insertion_Sort_Passes(ReadArray)
                idx, val = {i: PassCollect[i] for i in [random.randrange(len(PassCollect))]}.popitem()
                f3.write('TYPE WHAT PASS THIS IS: INSERTION (RIGHT SIDE)')
        
    elif mode == 'Randomized_Competitive':
        
        sortlist=['I','B']
        PassCollect=random.choice(sortlist)
        with open('SortingType.txt','w') as f3:
            if PassCollect=='I':
                PassCollect=Insertion_Sort_Passes(ReadArray)
                idx, val = {i: PassCollect[i] for i in [random.randrange(len(PassCollect))]}.popitem()
                f3.write('TYPE WHAT PASS THIS IS: INSERTION (RIGHT SIDE)')

            if PassCollect=='B':
                PassCollect=Bubble_Sort_Passes(ReadArray)
                idx, val = {i: PassCollect[i] for i in [random.randrange(len(PassCollect))]}.popitem()
                f3.write('TYPE WHAT PASS THIS IS: BUBBLE (RIGHT SIDE)')  
    

    print("index {} pass {}" .format(idx+1, val))
    with open('PassNumber.txt','w') as f1:
       f1.write(str(idx+1))
       numpy.savetxt('PassArray.txt', val)
    
    return val



def readpasstext():
    with open('PassNumber.txt','r') as f1:
        d=f1.read()
    with open ('SortingType.txt','r') as f3:
        x=f3.read()

    if x=='TYPE WHAT PASS THIS IS: BUBBLE (RIGHT SIDE)':
        return '{}'.format(x)
    
    elif x=='TYPE WHAT PASS THIS IS: INSERTION (RIGHT SIDE)':
        return '{}'.format(x)
    else:
        return '{} {}'.format(x,d)
    
def PostSort():
    arr=[]
    with open('PassArray.txt','r') as afile:
        alist = [(line.rstrip()) for line in afile] 

    for i in range(len(alist)):
        value=str(alist[i])
        value2=value. replace(',','.')
        value2=float(value2)
        arr.append(int(value2))
    
    return arr
    


def check_state():
    with open('SortingType.txt','r') as f1:
        a=f1.read()
        if a =='TYPE WHAT PASS THIS IS: BUBBLE (RIGHT SIDE)':
            return True
    
def check_State2():
    with open('SortingType.txt','r') as f1:
        a=f1.read()
        if a =='TYPE WHAT PASS THIS IS: INSERTION (RIGHT SIDE)':
            return True


def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    newloc=[]
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    for i in range(0,len(locs)):
        newloc.append(locs[i]+1)
    return newloc



