from tkinter import*
from GUIDatabase import guiPlayer, guiPoints
from bubblesort import visualiser
from database import*
from game import run
import pygame


class player:
    def __init__(self,id,IC,II,BC,BI):
        self.id = id
        self.IC = IC  # INSERTION CORRECT
        self.II = II  # INSERTION INCORRECT
        self.BC = BC  # BUBBLE CORRECT
        self.BI = BI  # BUBBLE INCORRECT

    def average(self):
        average=((self.IC+self.BC)/(self.IC+self.BC))*10
        return round(average,2)


def scored(II,BI,IC,BC):
    if (II+BI)==0:
        return((IC+BC)*10)+1
    else:
        score=((IC+BC)/(II+BI))*10
        return round(score)

    

def menu(id):
    color="#213141"
    mywindow = Tk()
    mywindow.geometry("650x550")

    mywindow.title("Menu")
    mywindow.config(background = color)

    def Randomized_Competitive():
        pygame.display.init()
        scores=run('Randomized_Competitive')
        add_record_to_points(id,scores[0],scores[1],scores[2],scores[3],scored(scores[0],scores[1],scores[2],scores[3]))
        mywindow.destroy()
        menu(id)
        
    
    def Practice_Bubble():
        pygame.display.init()
        run('Practice_Bubble')
        

    def Practice_Insertion():
        pygame.display.init()
        run('Practice_Insertion')


    main_title = Label(mywindow,text = "Menu Screen", font = ("comicsans", 14), bg = "turquoise", fg = "black", width = "500", height = "2")
    main_title.pack()

    sub_title=Label(mywindow,text = "Welcome {}".format(get_username(id)), font = ("Comicsans", 14), bg = "turquoise", fg = "black", width = "200", height = "2")
    sub_title.pack()
        
    play = Button(mywindow,text = "Randomized Competitive", width = "30", height = "2", command = Randomized_Competitive, bg = "green",font=('comicsans','10','bold'),foreground='white')                   # This button will open the Competitive Mode. 
    play.place(x = 0, y = 100)

    Practice_Bubble_sorting = Button(mywindow,text = "Practice Bubble Sorting", width = "30", height = "2", command = Practice_Bubble, bg = "green",font=('comicsans','10','bold'),foreground='white')         # This button will open the Practice Randomized sort Mode
    Practice_Bubble_sorting.place(x = 0, y = 200)

    Practice_Insertion_sorting = Button(mywindow,text = "Practice Insertion Sorting", width = "30", height = "2", command = Practice_Insertion, bg = "green",font=('comicsans','10','bold'),foreground='white')  # This button will open the Practice Insertion sort Mode
    Practice_Insertion_sorting.place(x = 0, y = 300)

    Visualiser = Button(mywindow,text = "Visualiser", width = "30", height = "2", command = visualiser, bg = 'green',font=('comicsans','10','bold'),foreground='white')     # This button will open the visualiser
    Visualiser.place(x = 0, y = 400)

   
    LeaderBoard = Label(mywindow,text ='Highest Scores Top 5',background='black',font=('comicsans','10','bold'),foreground='White',height=22,width=25,anchor='n')
    LeaderBoard.place(x=450, y=100)


    def top_5():
        a=gettop5()
        if len(a)<=0:
            a=a[0:len(a)]
        else:
            newarr=[]
            for i in range(len(a)):
                newarr.append(Label(mywindow,text ='{}. {} {} score :{}'.format(i+1,a[i][0],a[i][1],a[i][2]),background='Black',font=('comicsans','10','bold'),foreground='White',height=2,width=25,anchor='w'))
            
            for j in range(len(a)):
                newarr[j].place(x=450,y=150+(j*50))




    mywindow.mainloop()

menu(1)


