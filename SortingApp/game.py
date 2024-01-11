import numpy
import pygame
import time
import random
from sorting import *


pygame.font.init()

SORTFONT=pygame.font.SysFont('comisans',25)
bg_color=(6,77,81)#tuple of our background colour
donebuttoncolor=(200,200,200)
UserInput=''   
        
pygame.init()
pygame.display.set_caption("Drag and drop")



class DraggableRect:
    def __init__(self,position,size,originalposition,colour=''):
        self.x=position[0]
        self.y=position[1]
        self.width=size[0]
        self.height=size[1]
        self.currentx=0
        self.originalpositionx=originalposition[0]
        self.originalpositiony=originalposition[1]
        self.colour=colour

    def draw(self,screen): 
        pygame.draw.rect(screen,self.colour,[self.x,self.y,self.width,self.height])   

    def draw_center(self,screen):
        pygame.draw.rect(screen,self.colour,[windowWidth/2,windowheight,15,windowheight])


    def setxcoordinate(self,xcor):
        self.x=xcor
    
    def setycoordinate(self,ycor):
        self.y=ycor

    def setoriginalx(self,origx):
        self.originalpositionx=origx

    def is_point_in_rectangle(self,position):
        if ((self.x<=position[0]) and (position[0]<=self.x+self.width)) and ((self.y<=position[1]) or (self.y>= position[1])) and ((position[1]<=self.y+self.height) or (position[1]>=self.y+self.height)):
            return(True)
        else:
            return(False)
        
    def setColour (self,newcolour):
        self.colour=newcolour


    def is_collided(self,array):
        for i in range(len(array)):
            if array[i]!=self:
                collision=False
                if self.is_point_in_rectangle([array[i].x,array[i].y]):
                    collision=True
                if self.is_point_in_rectangle([array[i].x+array[i].width,array[i].y]):
                    collision=True
                if self.is_point_in_rectangle([array[i].x,array[i].y+array[i].height]):
                    collision=True
                if self.is_point_in_rectangle([array[i].x+array[i].width,array[i].y+array[i].height]):
                    collision=True
                    
                if collision:
                    temp=array[i].originalpositionx
                    array[i].setxcoordinate(self.originalpositionx)
                    array[i].setxcoordinate(self.originalpositionx)
                    array[i].setoriginalx(array[i].x)
                    self.setoriginalx(temp) 
                    self.setxcoordinate(self.originalpositionx)
                    return True


class button(DraggableRect):
    def __init__(self, position, size, colour, ButtonText=''):
        super().__init__(position,size,colour)
        self.ButtonText = ButtonText
        if self.colour=='':
            self.colour=colour

    def render(self,window):
        #Call this method to draw the button on the screen

        pygame.draw.rect(window, self.colour, (self.x,self.y,self.width,self.height),0)    # Filled in rectangle
        pygame.draw.rect(window, (0,0,0) , (self.x,self.y,self.width,self.height),3)     #The border of the button 
        
        if self.ButtonText != '':
            
            textOnButton = SORTFONT.render(self.ButtonText, 1, (0,0,0))
            window.blit(textOnButton, (self.x + (self.width/2 - textOnButton.get_width()/2), (self.y + (self.height/2 - textOnButton.get_height()/2)))) #Center the text on the rendered rectangle

    def isMouseOver(self, mouseposition):
        # mousePos is the mouse position in a tuple of the (x,y) coordinates. Checking if the cursor is within the rectangle.
        if mouseposition[0] > self.x and mouseposition[0] < self.x + self.width:
            if mouseposition[1] > self.y and mouseposition[1] < self.y + self.height:
                return True
            
        return False

    def IsMouseNotOver(self,mouseposition):
        if mouseposition[0] < self.x and mouseposition[0] > self.x + self.width:
            if mouseposition[1] < self.y and mouseposition[1] > self.y + self.height:
                return True
      
                
         
class Position:
    def __init__(self,pos):
        self.mouseposition=pos
        self.x=pos[0]
        self.y=pos[1]
    
    
class Window(Position):
    def __init__(self,size,position=[0,0]):
        super().__init__(position)
        self.size=size
        self.screen = pygame.display.set_mode(self.size)

    def width(self):
        return(self.size[0]) 

    def height(self):
        return(self.size[1])

    def initialize_game(self):  

        pygame.init()
        pygame.display.set_caption("sorting game")
        clock=pygame.time.Clock()

        return(clock)  
      


    def draw_grid(self,grid):
        for row in range(grid.rows):
            for column in range(grid.columns):
                value=grid.grid[row][column]
                color = grid.colors[value]
                pygame.draw.rect(self.screen,
                                 color,
                                 [(grid.margin + grid.cell_size[0]) * column + grid.margin + grid.mouseposition[0],
                                  (grid.margin + grid.cell_size[1]) * row + grid.margin + grid.mouseposition[1],
                                  grid.cell_size[0],
                                  grid.cell_size[1]])      
    
    
selected=None

def refresh(rects,screen,counter):
    screen.fill(bg_color)

    for i,rect in enumerate(rects):
        rect.draw(screen)

    greenbutton.render(screen)        #rendering the button

    text=SORTFONT.render(readpasstext(),1,'white')              #This will render our text continuously every time our screen refreshes
    Userinput=SORTFONT.render(UserInput,1,'white')

    screen.blit(text,(0,0))
    screen.blit(Userinput,(750,0))

    

    if counter<=0:      #Game
        II=SORTFONT.render(('Incorrect Insertion Sorts : {}'.format(str(InsertionSortIncorrect))),1,(255,255,255))
        IB=SORTFONT.render(('Incorrect Bubble Sorts : {}'.format(str(BubbleSortIncorrect))),1,(255,255,255))
        CB=SORTFONT.render(('Correct Bubble Sorts : {}'.format(str(BubbleSortCorrectCounter))),1,(255,255,255))
        CI=SORTFONT.render(('Correct Insertion Sorts : {}'.format(str(InsertionSortCorrectCounter))),1,(255,255,255))
       
        screen.fill(bg_color)
        screen.blit(II,(windowWidth/2+50,windowheight/2+200))
        screen.blit(IB,(windowWidth/2-350,windowheight/2+200))
        screen.blit(CB,(windowWidth/2-350,windowheight/2-200))
        screen.blit(CI,(windowWidth/2+50,windowheight/2-200))

        Done.render(screen)  # render the button if game over
        

windowWidth=1000
windowheight=700
r = random.randint(0, 255)
g = random.randint(0, 255)
b = random.randint(0, 255)
rand_color = (r, g, b)


def createvisualisation(length,mode):
    writeRandomized(length)
    array=readRandomized()
    blockwidth=windowWidth/len(array)
    newarr=[]
    for i in range(len(array)):
        newarr.append(DraggableRect([i*blockwidth,windowheight],[blockwidth-25,array[i]*20],[i*blockwidth,windowheight],rand_color))

    chooserandompass(mode)
    return newarr

def createvisualisation2(length,mode):
    writeRandomized(length)              #Writing random numbers to text file
    
    array=readRandomized()               # Read this file and creating an array to store these values
    blockwidth=windowWidth/(len(array)*2)   #equally spacing out blocks
    a=chooserandompass2(mode)
    newarr=[]

    for i in range(len(array)):
        newarr.append(DraggableRect([(i*blockwidth),windowheight],[blockwidth-25,array[i]*20],[i*blockwidth,windowheight],rand_color))

    lastxcor=newarr[-1].x+25    # storing the position of the last rendered rectangle so we can continue the viualisation process from that point


    for j in range(1,length+1):
        newarr.append(DraggableRect([j*blockwidth+lastxcor,windowheight],[blockwidth-25,a[j-1]*20],[j*blockwidth,windowheight],'white'))                # Creating the correct visualisation from the random on the right hand side of the screen starting from the last block rendered
    
    center=DraggableRect([(windowWidth/2),windowheight],[10,windowheight],[(windowWidth/2),windowheight],'black')             #This is the the wall which will split the screen
    newarr.append(center)

    return newarr  #return this array


def wait(how_long):
     time.sleep(how_long)

def reset():
    newarr=[]
    array=readRandomized()                             # reset config if CreateVisualisation() was called
    blockwidth=windowWidth/len(array)
    for i in range(len(array)):
       newarr.append(DraggableRect([i*blockwidth,windowheight],[blockwidth-25,array[i]*20],[i*blockwidth,windowheight],'red'))
    return newarr

def reset2():
    newarr=[]
    LHS=readRandomized()
    RHS=PostSort()
                                                                      #  # reset config if CreateVisualisation2() was called
    blockwidth=windowWidth/(len(LHS)*2)
    for i in range(len(LHS)):
       newarr.append(DraggableRect([i*blockwidth,windowheight],[blockwidth-25,LHS[i]*20],[i*blockwidth,windowheight],'red'))  # REDRAW THE LEFT HAND SIDE OF THE SCREEN
    lastxcor=newarr[-1].x+25

    for j in range(1,len(RHS)+1):
        newarr.append(DraggableRect([j*blockwidth+lastxcor,windowheight],[blockwidth-25,RHS[j-1]*20],[j*blockwidth,windowheight],'white'))    # REDRAW RIGHT HAND SIDE OF THE SCREEN
    
    center=DraggableRect([(windowWidth/2),windowheight],[10,windowheight],[(windowWidth/2),windowheight],'black')
    newarr.append(center)

    return newarr  



def checkUserConfig(array):
    newarr=sorted(array,key=lambda e:(e.x))  #Sorting the objects by the attributes

    y=numpy.loadtxt('PassArray.txt')
    i=0

    flag=True
    while flag and i <=len(y)-1:
        if newarr[i].height==y[i]*20:           # Checking if the height of the rectangles = to the values in the pass array
            i=i+1
        else:                            
                                     
             for i,rect in enumerate(newarr):
                newarr[i].setColour((255,0,0))      #change colour of rectangles to red
                 
             flag=False                # This will tell us that the user has got the configuration wrong

    return flag           #If flag was true througout the while loop, The user has got the answer correct.


def CheckerB(input_val):
    with open('PassNumber.txt','r') as f1:
        passval=f1.read()                                 # This is the checker Function for the bubble sort to compare the user input to the pass number that was stored in the text file
        if input_val==passval:           #check the value of the pass
            return True                 # User has typed in the correct pass
        else:
            return False       #User has typed the incorrect pass
    
def checkerI(input_val):

    if len(input_val)==0:
        input_val=0

    with open('PassNumber.txt','r') as f1:       # This is the checker Function for the bubble sort to compare the user input to the pass number that was stored in the text file
        passval=f1.read()
        if input_val==passval:
            return True
        else:
            a= readRandomized()             #read the text file containing randomly written numbers
            duparr=Insertion_Sort_Passes(a)      # grab all the passes from the values of the text file

            indexduplicates=list_duplicates(duparr,PostSort())       #Check for duplicates in the array that constructed the right hand side of the screen (the array that corresponds to the pass number generated by choose random pass())

            print(indexduplicates)           #print all duplicates to check if there are any
            i=0
            while i <len(indexduplicates):
                if int(input_val)==int(indexduplicates[i]):               #linear search to see if User Input matches a pass number in the duplicates array
                    return True
                else:
                    i=i+1
    return False        


greenbutton=button([850,0],[150,75], "green","CHECK")
Done=button([0,0],[150,50], donebuttoncolor, 'DONE')

def timer(rects):
    counter=len(rects)*5
    return counter


BubbleSortCorrectCounter=0
InsertionSortCorrectCounter=0
BubbleSortIncorrect=0
InsertionSortIncorrect=0

temp1=0
temp2=0
temp3=0
temp4=0

def placeText(screen,font, TEXT, colour, x, y):
    text = font.render(TEXT, 1, colour)
    screen.blit(text, (x, y))

def main_program_loop(window,screen,clock,rects,mode):

    input_active=True

    global UserInput 

    global InsertionSortCorrectCounter
    global InsertionSortIncorrect
    global BubbleSortCorrectCounter
    global BubbleSortIncorrect

    global temp1
    global temp2
    global temp3
    global temp4

    if mode=='Randomized_Competitive':
        counter=7
        SORTFONT2=pygame.font.SysFont('comicsans',35) #creating a new font surface
        text=SORTFONT2.render('{} seconds left'.format(str(counter)),True,(255,255,255))  #this will be our text
        timer_event=pygame.USEREVENT+1
        pygame.time.set_timer(timer_event,1000)
    else:
        counter=1                    
        SORTFONT2=pygame.font.SysFont('comicsans',35)
        text16=SORTFONT2.render('{} seconds left'.format(str(counter)),True,(255,255,255))
        timer_event=pygame.USEREVENT+1
        pygame.time.set_timer(timer_event,1000)
    
    selected=None
    done = False
    time_fr=0 #1/60 sec


    while not done:  
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                temp1=InsertionSortCorrectCounter
                temp2=InsertionSortIncorrect
                temp3=BubbleSortCorrectCounter
                temp4=BubbleSortIncorrect

                BubbleSortCorrectCounter=0
                InsertionSortCorrectCounter=0
                BubbleSortIncorrect=0
                InsertionSortIncorrect=0

                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()

                for i,rect in enumerate(rects):
                    if mousepos[0]>rect.x and mousepos[0]<rect.x+rect.width and mousepos[1]>rect.y and mousepos[1]<rect.y+rect.height:
                        selected=i
                        offset_x = rect.x - event.pos[0]
                        rect.setoriginalx(rect.x)

                if check_state() or check_State2():       #This will check if the program has called the create Visualisation 2 function
                    if mousepos[0] > windowWidth/2:
                        selected=None                


                if greenbutton.isMouseOver(mousepos):             #Checking if the mouse is over the button when the mouse is clicked
                    greenbutton.setColour((255,0,0))

                    if check_state() :                      #IF Create Visualisation 2 is called   we check for the user input
                        if CheckerB(UserInput):
                            text=SORTFONT2.render('{} seconds left'.format(str(counter)),1,(255,255,255))
                            for i in range(len(rects)):
                                rects[i].setColour((0,255,0))
                            print('correct')
                        
                        else:
                            for i in range(len(rects)):
                                rects[i].setColour((255,0,0))
                            print('incorrect')

                    elif check_State2():
                        if checkerI(UserInput):
                            text=SORTFONT2.render('{} seconds left'.format(str(counter)),1,(255,255,255))
                            for i in range(len(rects)):
                                rects[i].setColour((0,255,0))
                            print('correct')
                        
                        else:
                            for i in range(len(rects)):
                                rects[i].setColour((255,0,0))
                            print('incorrect')

                    else:

                        if checkUserConfig(rects):               # This will will called if the the function is checkUserConfig 
                            text=SORTFONT2.render('{} seconds left'.format(str(counter)),1,(255,255,255))
                            for i in range(len(rects)):
                                rects[i].setColour((0,255,0))
                            print('correct')
                    
                        else:
                            for i in range(len(rects)):
                                rects[i].setColour((255,0,0))
                            print('incorrect')

                if Done.isMouseOver(mousepos):

                    temp1=InsertionSortCorrectCounter
                    temp2=InsertionSortIncorrect
                    temp3=BubbleSortCorrectCounter
                    temp4=BubbleSortIncorrect

                    BubbleSortCorrectCounter=0
                    InsertionSortCorrectCounter=0
                    BubbleSortIncorrect=0
                    InsertionSortIncorrect=0

                    done=True
                     

            elif event.type==timer_event: 
                if mode=='Randomized_Competitive':
                    counter-=1           # decrement the timer by 1 so it does increment the program
                else:
                    counter+=1  # increment timer by 1 so it never reaches zero which terminates the program
                text=SORTFONT2.render('{} seconds left'.format(str(counter)),1,(255,255,255))
                
                if counter <= 0:
                    text1=SORTFONT2.render(('GAME OVER'),1,(255,255,255))
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                for i,rect in enumerate(rects):
                    if mousepos[0]>rect.x and mousepos[0]<rect.x+rect.width and mousepos[1]>rect.y and mousepos[1]<rect.y+rect.height:
                        selected=i
                        offset_x = rect.x - event. pos[0]
            
                selected = None
                greenbutton.setColour((0,255,0))

                if greenbutton.isMouseOver(mousepos):
                    if check_state():
                        if CheckerB(UserInput):
                            
                            BubbleSortCorrectCounter+=1
                            wait(0.5)
                            state=['C1','C2']
                            state=random.choice(state)
                            if state=='C1':
                                rects=createvisualisation(random.randrange(5,12),mode)
            
                            else:
                                rects=createvisualisation2(random.randrange(5,12),mode)
                            counter=counter+10
                        
                        else:
                            BubbleSortIncorrect+=1
                            wait(0.5)
                            rects=reset2()

                    elif check_State2():
                        if checkerI(UserInput):
                            InsertionSortCorrectCounter+=1
                            wait(0.5)
                            state=['C1','C2']    #Randomly choose between createvisualisation() and create visualisation2
                            state=random.choice(state)
                            if state=='C1':
                                rects=createvisualisation(random.randrange(5,16),mode)
            
                            else:
                                rects=createvisualisation2(random.randrange(5,16),mode)
                            counter=counter+10
                        
                        else:
                            InsertionSortIncorrect+=1
                            wait(0.5)
                            rects=reset2()
                    else:

                        if checkUserConfig(rects):
                            with open ('SortingType.txt','r') as f1:
                                a=f1.read()
                            if a=='BUBBLE SORT TO PASS':
                                BubbleSortCorrectCounter+=1
                            if a=='INSERTION SORT TO PASS':
                                InsertionSortCorrectCounter+=1

                            wait(0.5)
                            state=['C1','C2']
                            state=random.choice(state)
                            if state=='C1':
                                rects=createvisualisation(random.randrange(5,16),mode)
            
                            else:
                                rects=createvisualisation2(random.randrange(5,16),mode)
                            counter=counter+10

                        else:

                            with open ('SortingType.txt','r') as f1:
                                a=f1.read()
                            if a=='BUBBLE SORT TO PASS':
                                BubbleSortIncorrect+=1
                            else:
                                InsertionSortIncorrect+=1

                            wait(0.5)
                            rects=reset()

                    UserInput=''


            
            if event.type == pygame.KEYDOWN and input_active and (check_state() or check_State2()):         # Checks if the create Visualisation 2 function is called and a key on the key board is pressed.
                if event.key == pygame.K_RETURN:
                    if CheckerB(UserInput) or checkerI(UserInput):           #if the user presses the enter button these functions will check the user input and compare to the value in the passNumber.txt file
                        print('correct')
                    else:
                        print('incorrect')
                    UserInput=''
                    rectangles=reset()
                    

                elif event.key == pygame.K_BACKSPACE:
                    UserInput =  UserInput[:-1]
                else:
                    input_active=True
                    UserInput += event.unicode

            

            elif event.type == pygame.MOUSEMOTION:
                
                for i,rect in enumerate(rects):
                    if selected==i :
                        rect.setxcoordinate(event.pos[0]+offset_x)
                        if check_state() or check_State2():                #check if the program has called the create visualisation 2 function by reading the text files
                            if rect.x>windowWidth/2-rect.width-1:
                                rect.setxcoordinate(windowWidth/2-rect.width-1)   #This will prevent any blocks from being dragged over the wall that is centerd onto the screen. Setting our x coordinate if it tries to pass through to be placed before the wall 

                    if rect.x<0:
                        rect.setxcoordinate(0)          #our normal boundary wall conditions placed on the rectangles so they don't go out of screen

                    if rect.y<0:
                        rect.setycoordinate(0)

                    if rect.x>windowWidth-rect.width:
                            rect.setxcoordinate(windowWidth-rect.width)

                    if rect.y>windowheight-rect.height:
                        rect.setycoordinate(windowheight-rect.height) 
            
            pygame.display.flip()
            pygame.event.pump()
                    

       
        if mode=='Randomized_Competitive':
            if counter>0:
                screen.blit(text,(550,0)) 
            else:
                screen.blit(text1,(windowWidth/2-75,windowheight/2))
        
        
        pygame.display.flip()   
          
        clock.tick(60)
        pygame.display.flip()
        time_fr+=1
        
        if time_fr%1==0:
            refresh(rects,screen,counter)
            for i,rect in enumerate(rects):
                rect.is_collided(rects)

                    
        pygame.display.flip() 
        
def run(mode):
    window=Window([windowWidth,windowheight])
    clock = window.initialize_game()
    main_program_loop(window,pygame.display.set_mode([windowWidth,windowheight]),clock,createvisualisation(random.randrange(5,16),mode),mode)
    pygame.display.quit()
    print(temp1,temp2,temp3,temp4)
    return (temp1,temp2,temp3,temp4)


run('Randomized_Competitive')

