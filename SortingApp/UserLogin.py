from tkinter import *
from tkinter import messagebox
from database import*
from GUIDatabase import guiPlayer
from menu import menu
import re



def folding(concat_ascii, foldLength):

    stringNum = concat_ascii
    done = False                                # This will make sure that the while loop continues running
    newarr = []
    while stringNum and not done:
        if len(stringNum) > foldLength:          #If our string length is greater than the amount we split the string by then we split the by our foldlength
                                                 # we keep doing this until the length of the string is less than the fold length for which we will exit out of the while loop
            newsplit = stringNum[:foldLength]  
        else:
            newsplit = stringNum                   #Otherwise it will remain the same
        newarr.append(int(newsplit))                     
        if foldLength > len(stringNum):
            done = True                                          # if there is a remainder when we completed our foldlength, then the rest of our string will be of length remainder
        stringNum = stringNum[foldLength:]          
    total = sum(newarr)                               #add the values after the split
    return total       #return the total


def passwordhash(word,foldLength):
    emptystr=''
    for i in range(len(word)):                       # give a word as the input and convert each letter to its ascii value
        emptystr=emptystr+str(ord(word[i]))          # concatenate the string version of each integer
    print(emptystr)
    calculate=folding(emptystr,foldLength)            # do the fold length on this concatenated string
    return calculate   


def Valid_email(email):
  pattern = re.compile(r'(^[a-zA-Z0-9_.!$&]+@[a-zA-Z]+\.[a-zA-Z]+$)')
  check = pattern.search(email)
  if check== None:    
      messagebox.showwarning('warning','Not a valid email address')
      return False
  else:
      return True

def valid_username(username):
    if len(username)<4:
        messagebox.showwarning('warning','UserName needs to be longer')
        return False
    else:
        username.lower()
        return True

def valid_password(password):
    if password==0:
        messagebox.showwarning('warning','Password needs to be longer')
        return False
    else:
        return True

def valid_class(Class):
    classes=['12SV','12SD','13AG','13TA']
    if Class not in classes:
        messagebox.showwarning('Warning','Make sure you have put the correct class')
        return False
    else:
        return True
      
def clear():
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    Email_entry.delete(0,END)
    Class_entry.delete(0,END)
    Email_entry.insert(0, placeholder_text)
    Class_entry.insert(0, placeholder_text)

def sending_data():
  username_info = Username.get()
  PassLength=len(Password.get())
  password_info = passwordhash(Password.get(),2)
  Class_info=Class.get()
  email_info=Email.get()

  
  if valid_username(username_info):
        if valid_password(PassLength): 
            if Valid_email(email_info):
               if valid_class(Class_info):
                    if NotExistingRecord(username_info,password_info):
                        add_record(username_info,email_info,Class_info,password_info)
                        clear()
                        guiPlayer()

                    else:
                        messagebox.showerror('','There is a record of similar details:Enter different Username or Password')
  else:
    clear()


color="#213141"
# Creating a new instance - Class Tk()  Tkinter Frame
myUserLoginWindow = Tk()
myUserLoginWindow.geometry("650x550")
myUserLoginWindow.title("Validation and Registration")
main_title = Label(text = "Sorting algorithm interactive game", font = ("Cosmic sans", 14), bg = "turquoise", fg = "black", width = "500", height = "2")
main_title.pack()
myUserLoginWindow.config(background = color)


# Get and store data from users from those texboxes
Username = StringVar()
Password = StringVar()      # passing a string input to each textbox
Email=StringVar()
Class=StringVar()

username_entry = Entry(textvariable = Username, width = "100")
password_entry = Entry(textvariable = Password, width = "100",  show = "*")    # When we type our text in this box the actual letters will be hidden and will be replaced by * 
                                                                               #Protecting important user details to be seen by others
Email_entry = Entry(textvariable = Email, width = "100")
Class_entry = Entry(textvariable = Class, width = "100")          


#These will define the label fields by adding headers above each texbox

username_label = Label(text = "Username", bg = color,font=('comicsans','10','bold'),foreground='white')
username_label.place(x = 20, y = 70)                                                                            

password_label = Label(text = "Password", bg = color,font=('comicsans','10','bold'),foreground='white')
password_label.place(x = 20, y = 130)

Email_label = Label(text = "Email Address", bg = color,font=('comicsans','10','bold'),foreground='white')
Email_label.place(x = 20, y = 190   )

Class_label = Label(text = "Class", bg = color,font=('comicsans','10','bold'),foreground='white')
Class_label.place(x = 20, y = 250)




placeholder_text = 'Not applicable if logging in'
Email_entry.insert(0, placeholder_text)
Class_entry.insert(0, placeholder_text)


def clear_entry(event, boxentry):
    boxentry.delete(0, END)              #Clearing the entry field


Email_entry.bind("<Button-1>", lambda event: clear_entry(event, Email_entry))         # When the mouse button is clicked this will call the clear entry function to remove placeholders
Class_entry.bind("<Button-1>", lambda event: clear_entry(event, Class_entry))         

 
username_entry.place(x = 20, y = 100)
password_entry.place(x = 20, y = 160)
Email_entry.place(x = 20, y = 220)
Class_entry.place(x = 20, y = 280)

def QUIT():
    myUserLoginWindow.destroy()



attempts=1
def compare(USERNAME):
    connection=sqlite3.connect('project1.db')
    cursor=connection.cursor()
    cursor.execute('''SELECT PLAYERID,PASSWORD_HASH FROM PLAYER WHERE USERNAME=(?)''',(USERNAME,))              
                                                                                                             
    result=cursor.fetchall()                                                       #querying for all password hashes from a given user name because there could be multiple users with the same one                                             
    PHresult=([f[1] for f in result])                                         
    return PHresult
      

def User_Login():
    global attempts
    username_info = Username.get()
    password_info = passwordhash(Password.get(),2)
    passwordhashcheck=(compare(username_info))
    
    if len(passwordhashcheck)==0:
        print('non existing record')
        attempts+=1
        messagebox.showwarning('attempts','you have {} attempts left'.format(4-attempts))
        if attempts==4:
            QUIT()
            attempts=1
        else:
            clear()
            
    else:

        i=0
        found=False
        while found==False and i<len(passwordhashcheck):
            if password_info==passwordhashcheck[i]:                  #Linear search of all the hashed passwords collected from the SQL query
                print('user is found')

                username_entry.delete(0, END)
                password_entry.delete(0, END)
                Email_entry.delete(0,END)
                Class_entry.delete(0,END) 

                id=getPlayerID(passwordhashcheck[i],username_info)
                menu(id) 
                found=True

            else:
                i=i+1
        if found==False:                                                                           #This function will be called once the submit button is pressed
            print('user not found')
            attempts+=1
            messagebox.showwarning('attempts','you have {} attempts left'.format(4-attempts))
            username_entry.delete(0, END)
            password_entry.delete(0, END)
            Email_entry.delete(0,END)
            Class_entry.delete(0,END) 

            if attempts==4:
                QUIT()
                attempts=1 

# Submit Button
submit_btn = Button(myUserLoginWindow,text = "LOGIN", width = "30", height = "2", command = User_Login, bg = "green",font=('comicsans','10','bold'),foreground='white')
submit_btn.place(x = 400, y = 400)


register = Button(myUserLoginWindow,text = "REGISTER ", width = "30", height = "2", command = sending_data, bg = "red",font=('comisans','10',' bold'),foreground='white')
register.place(x = 0, y = 400)

myUserLoginWindow.mainloop()







