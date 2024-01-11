
from tkinter import*
from tkinter import ttk,messagebox
import numpy
from database import class_attempts, delete_Player, query_database_Player, query_database_Points,graphing,sum_of_Classes,sum_of_sorting
from matplotlib import pyplot as plt

def guiPlayer():

    root=Tk()                            # Creating a new instance of a tkinter surface
    root.title('GUI Player Database')
    root.geometry('1000x500')


    def select_record():
        selected=ViewDatabaseTable.focus()                 #selecting a specific record
        if selected=='':
            messagebox.showerror('Error','Select a record')
        else:

            values=ViewDatabaseTable.item(selected,'values')

            Individual_Scores=graphing(values[0])    # getting all records of games played by the id number corresponding to the record selected (Values[0])
            if len(Individual_Scores)==0:
                messagebox.showerror('Error','This player has not played any games yet')       #  we can't graph the data if there is no data values to plot

            else:
                xcor=[]
                ycor=[]
                ycor2=[]

                for i in range(len(Individual_Scores)):
                    xcor.append(i)  # getting the x values to represent their game number e.g game 1 ,2 ,3 ,4 etc rather than using their game id which may not be in order
                    b=list(Individual_Scores[i])
                    ycor.append(b)
                print(xcor)

                for i in range(len(Individual_Scores)):
                    ycor2.append(ycor[i][3])          # grabbing all the scores for each game played
                print(ycor2)
                
                plt.plot(xcor,ycor2)
                plt.xlabel('Number of games played')   #Title x cor
                plt.ylabel('Score')                     # Title y cor
                plt.title('The performance of {} from class {}'.format(Individual_Scores[0][0],Individual_Scores[0][1]))  # string concatenation 
                plt.show()

    
    def view_class_analytics(graph):
        classes=['12SV','12SD','13AG','13TA']
        xcor=[]
        ycor=[]
        newarr=[]
        for i in range(len(classes)):
            newarr.append(sum_of_Classes(classes[i]))
        
        for j in range(len(newarr)):
            xcor.append(newarr[j][0])
            if graph=='average':
                ycor.append(newarr[j][1]/class_attempts(classes[j]))
            else:
                ycor.append(newarr[j][1])
        print(xcor)
        print(ycor)

        plt.bar(xcor,ycor)
        plt.xlabel('Classes')
        if graph=='average':
            plt.ylabel('AVG Score')
            plt.title('Average Class Performance')
        else:
            plt.ylabel('Total Class Score')
            plt.title('Accumulated Class Performance')

        plt.show()
    

    def accumulated():
        view_class_analytics('accumulated')

    def average():
        view_class_analytics('average')
        


    def view_sorting_analytics():
        lists=[]
        for i in range(0,4):
            lists.append(sum_of_sorting()[0][i])
        print(lists)
        
        X = ['INSERTION SORT','BUBBLE SORT']
        INSERTION = lists[0:2]
        BUBBLE = lists[2:4]
        
        X_axis = numpy.arange(len(X))
        
        plt.bar(X_axis - 0.2, INSERTION, 0.4, label = 'TOTAL CORRECT')
        plt.bar(X_axis + 0.2, BUBBLE, 0.4, label = 'TOTAL INCORRECT')
        
        plt.xticks(X_axis, X)
        plt.xlabel("TYPE")
        plt.ylabel("NUMBER OF RIGHT/WRONG")
        plt.title("SORTING ALGORITHM ANALYTICS")
        plt.legend()
        plt.show()

    

    def delete_record():
        selected=ViewDatabaseTable.focus()
        if selected=='':
            messagebox.showerror('Error','Select a record')
        else:

            values=ViewDatabaseTable.item(selected,'values')
            delete_Player(values[0])
            root.destroy()
            guiPlayer()


        
    Style=ttk.Style()
    
    Style.configure('Treeview',background='#138F89',foreground='#138F89', rowheight=25,fieldbackground='#D3D3D3')
    Style.map('Treeview',background=[('selected','#138F89')])
    tree_frame=Frame(root)  # setting our frame to this window
    tree_frame.pack(pady=10)
    tree_scroll=Scrollbar(tree_frame)

    tree_scroll.pack(side=RIGHT,fill=Y)

    ViewDatabaseTable=ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode='extended')
    ViewDatabaseTable.pack()

    tree_scroll.config(command=ViewDatabaseTable.yview)
    ViewDatabaseTable['columns']=('PLAYERID','USERNAME','EMAIL','CLASS','PASSWORD HASH')

    ViewDatabaseTable.column('#0',width=0,stretch=NO)
    ViewDatabaseTable.column('PLAYERID',anchor=CENTER,width=140)
    ViewDatabaseTable.column('USERNAME',anchor=CENTER,width=140)
    ViewDatabaseTable.column('EMAIL',anchor=CENTER,width=180)                 # identifieng the columns in the Player Table
    ViewDatabaseTable.column('CLASS',anchor=CENTER,width=140)
    ViewDatabaseTable.column('PASSWORD HASH',anchor=CENTER,width=140)
   

    ViewDatabaseTable.heading('#0', text= "" ,anchor=CENTER)
    ViewDatabaseTable.heading('PLAYERID', text= "PLAYERID" ,anchor=CENTER)        #  Labelling rhe columns in the player table
    ViewDatabaseTable.heading('USERNAME', text= "USERNAME" ,anchor=CENTER)
    ViewDatabaseTable.heading('EMAIL', text= "EMAIL" ,anchor=CENTER)
    ViewDatabaseTable.heading('CLASS', text= "CLASS" ,anchor=CENTER)
    ViewDatabaseTable.heading('PASSWORD HASH', text= "PASSWORD HASH" ,anchor=CENTER)
  

    ViewDatabaseTable.tag_configure('oddrows', background='white')
    ViewDatabaseTable.tag_configure('evenrows',background='lightblue')                     # we want to alternate the rows so we can distinguish between two rows. making it easier

    button_frame=LabelFrame(root,text='Analytics')
    button_frame.pack(fill='x',expand='no',padx=10,pady=50)
    

    PlayerAnalytics=Button(button_frame,text='Player analytics',command=select_record)
    PlayerAnalytics.grid(row=0,column=1,padx=60,pady=10)

    AvgClassPerformance=Button(button_frame,text='Average Class Analytics',command=average)
    AvgClassPerformance.grid(row=0,column=2,padx=60,pady=10)

    AccumulatedClassPerformance=Button(button_frame,text='Accumulated Class analytics ',command=accumulated)
    AccumulatedClassPerformance.grid(row=0,column=3,padx=60,pady=10)

    SortingAnalytics=Button(button_frame,text='Sorting analytics',command=view_sorting_analytics)
    SortingAnalytics.grid(row=0,column=4,padx=60,pady=10)

    SortingAnalytics2=Button(button_frame,text='Delete Record',command=delete_record)
    SortingAnalytics2.grid(row=2,column=2,padx=60,pady=10)
    
    


    query_database_Player(ViewDatabaseTable)
    root.mainloop()

#------------------------------------------------------------------------------------------------------------------------------------------

def guiPoints():

    root=Tk()
    root.title('GUI Points Database')
    root.geometry('1000x500')

    Style=ttk.Style()
    
    Style.configure('Treeview',background='#D3D3D3',foreground='black', rowheight=25,fieldbackground='#D3D3D3')
    Style.map('Treeview',background=[('selected','#347083')])

    tree_frame=Frame(root)
    tree_frame.pack(pady=10)
    tree_scroll=Scrollbar(tree_frame)

    tree_scroll.pack(side=RIGHT,fill=Y)
    ViewDatabaseTable=ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode='extended')         # scroll bar will appear if the number of records exceed the frame height
    ViewDatabaseTable.pack()

    tree_scroll.config(command=ViewDatabaseTable.yview)
    ViewDatabaseTable['columns']=('GAMEID','PLAYERID','INSERTION CORRECT','INSERTION INCORRECT','BUBBLE CORRECT','BUBBLE INCORRECT','SCORE')      # the column names that i ha defined in the database


    ViewDatabaseTable.column('#0',width=0,stretch=NO)
    ViewDatabaseTable.column('GAMEID',anchor=CENTER,width=140)
    ViewDatabaseTable.column('PLAYERID',anchor=CENTER,width=140)
    ViewDatabaseTable.column('INSERTION CORRECT',anchor=CENTER,width=140)
    ViewDatabaseTable.column('INSERTION INCORRECT',anchor=CENTER,width=140)
    ViewDatabaseTable.column('BUBBLE CORRECT',anchor=CENTER,width=140)
    ViewDatabaseTable.column('BUBBLE INCORRECT',anchor=CENTER,width=140)
    ViewDatabaseTable.column('SCORE',anchor=CENTER,width=140)
   


    ViewDatabaseTable.heading('#0', text= "" ,anchor=CENTER)
    ViewDatabaseTable.heading('GAMEID', text= "GAMEID" ,anchor=CENTER)
    ViewDatabaseTable.heading('PLAYERID', text= "PLAYERID" ,anchor=CENTER)
    ViewDatabaseTable.heading('INSERTION CORRECT', text= "INSERTION CORRECT" ,anchor=CENTER)
    ViewDatabaseTable.heading('INSERTION INCORRECT', text= "INSERTION INCORRECT" ,anchor=CENTER)
    ViewDatabaseTable.heading('BUBBLE CORRECT', text= "BUBBLE CORRECT" ,anchor=CENTER)
    ViewDatabaseTable.heading('BUBBLE INCORRECT', text= "BUBBLE INCORRECT" ,anchor=CENTER)
    ViewDatabaseTable.heading('SCORE', text= "SCORE" ,anchor=CENTER)
    
  

    ViewDatabaseTable.tag_configure('oddrow', background='white')
    ViewDatabaseTable.tag_configure('evenrow',background='lightblue')              # alternate the colours to distinguish each row when selecting a record

    query_database_Points(ViewDatabaseTable)

    root.mainloop()

guiPlayer()
