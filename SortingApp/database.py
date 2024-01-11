from operator import add
import sqlite3

from numpy import record


connection=sqlite3.connect('project1.db')
cursor=connection.cursor()

query1=('''CREATE TABLE IF NOT EXISTS PLAYER
           ( PLAYERID     INTEGER     PRIMARY KEY,
             USERNAME      TEXT         NOT NULL,
             EMAIL_ADDRESS TEXT         NOT NULL,
             CLASS         CHAR(4)      NOT NULL,
             PASSWORD_HASH INTEGER      NOT NULL);''')

connection.execute(query1)

connection.commit()
connection.close()


connection=sqlite3.connect('project1.db')
cursor=connection.cursor() 

query2=('''CREATE TABLE IF NOT EXISTS POINTS
          ( GAMEID                INTEGER            PRIMARY KEY,
            PLAYERID              INTEGER             NOT NULL,
            INSERTION_CORRECT     INTEGER             NOT NULL,
            INSERTION_INCORRECT   INTEGER             NOT NULL,
            BUBBLE_CORRECT        INTEGER             NOT NULL,
            BUBBLE_INCORRECT      INTEGER             NOT NULL,
            SCORE                 INTEGER             NOT NULL,
            FOREIGN KEY(PLAYERID) REFERENCES PLAYER(PLAYERID));''')

connection.execute(query2)
connection.close()


def query_database_Player(treebase):
    connection=sqlite3.connect('project1.db')
    cursor=connection.cursor()
    cursor.execute('SELECT*FROM PLAYER')
    records=cursor.fetchall()
    count=0

    for record in records:
        if count%2==0:
            treebase.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('evenrows'))

        else: 
            treebase.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('oddrows',))
        
        count+=1
    


def query_database_Points(treebase):
    connection=sqlite3.connect('project1.db')
    cursor=connection.cursor()
    cursor.execute('SELECT*FROM POINTS')
    records=cursor.fetchall()
    count=0

    for record in records:
        if count%2==0:
            treebase.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6]),tags=('evenrow'))

        else: 
            treebase.insert(parent='',index='end',iid=count,text='',values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6]),tags=('oddrow',))
        
        count+=1
 

def add_record(USERNAME,EMAIL_ADDRESS,CLASS,PASSWORDHASH):
    connection=sqlite3.connect('project1.db')
    cursor=connection.cursor()
    cursor.execute("INSERT INTO PLAYER (USERNAME,EMAIL_ADDRESS,CLASS,PASSWORD_HASH) VALUES (?,?,?,?)",(USERNAME,EMAIL_ADDRESS,CLASS,PASSWORDHASH))
    connection.commit()
    connection.close()

def add_record_to_points(PLAYERID,INSERTION_CORRECT,INSERTION_INCORRECT,BUBBLE_CORRECT,BUBBLE_INCORRECT,SCORE):
    connection=sqlite3.connect('project1.db')
    connection.execute('PRAGMA foreign_keys=ON')
    cursor=connection.cursor()
    cursor.execute('''INSERT INTO POINTS (PLAYERID,INSERTION_CORRECT,INSERTION_INCORRECT,BUBBLE_CORRECT,BUBBLE_INCORRECT,SCORE) VALUES (?,?,?,?,?,?)'''
    ,[PLAYERID,INSERTION_CORRECT,INSERTION_INCORRECT,BUBBLE_CORRECT,BUBBLE_INCORRECT,SCORE])
    connection.commit()
    connection.close()


def delete_Player(id):
        connection=sqlite3.connect('project1.db')
        cursor=connection.cursor()
        cursor.execute('DELETE FROM PLAYER WHERE PLAYERID=(?)',(id))
        connection.commit()
        connection.close() 


def TRUNCATE():
    connection=sqlite3.connect('project1.db')
    cursor=connection.cursor()
    cursor.execute('DELETE FROM PLAYER')
    cursor.execute('DELETE FROM POINTS;')
    
    connection.commit()
    connection.close()


def drop():
    connection=sqlite3.connect('project1.db')
    connection.execute('DROP TABLE PLAYER')
    connection.execute('DROP TABLE POINTS')
    connection.commit()
    connection.close()


def compare(USERNAME):
    connection=sqlite3.connect('project1.db')
    cursor=connection.cursor()
    cursor.execute('''SELECT PLAYERID,PASSWORD_HASH FROM PLAYER WHERE USERNAME=(?)''',(USERNAME,))
    result=cursor.fetchall()
    PHresult=([f[1] for f in result])
    return PHresult
      
def getPlayerID(Hashedpassword,USERNAME):
    connection=connection=sqlite3.connect('project1.db')
    cursor=connection.cursor()
    cursor.execute('''SELECT PLAYERID FROM PLAYER WHERE PASSWORD_HASH=(?) AND USERNAME=(?)''',(Hashedpassword,USERNAME))
    result=cursor.fetchone()
    connection.commit()
    connection.close()
    return result[0]

                
def NotExistingRecord(Username,Password):
    connection=connection=sqlite3.connect('project1.db')
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM PLAYER WHERE USERNAME=(?) AND PASSWORD_HASH=(?)",(Username,Password))
    result=cursor.fetchall()
    connection.commit()
    connection.close()
    if len(result)==0:
        return True
    else:
        return False
    

def get_username(id):
    connection=sqlite3.connect('project1.db')
    cursor=connection.cursor()
    cursor.execute("SELECT USERNAME FROM PLAYER WHERE PLAYERID=(?)",(str(id)))  # SQL  QUERY TO GET THE USERNAME
    result=cursor.fetchall()
    username=([f[0] for f in result])
    connection.commit()
    connection.close()
    return username[0]


def graphing(myid):
    connection=sqlite3.connect('project1.db')
    connection.execute('PRAGMA foreign_keys=ON')               # this is to let the sqlite 3 know that we are now using foreign key
    cursor=connection.cursor()
    cursor.execute('''SELECT USERNAME,CLASS,GAMEID,SCORE FROM PLAYER INNER JOIN POINTS
            ON PLAYER.PLAYERID = POINTS.PLAYERID
            WHERE PLAYER.PLAYERID=(?);''',(str(myid)))
    
   
    result = cursor.fetchall()              # fethching all the games played by this specific user along with username gameid, class and score
    
    connection.commit()
    connection.close()
    return result
    
def gettop5():
    connection=sqlite3.connect('project1.db')
    connection.execute('PRAGMA foreign_keys=ON')
    cursor=connection.cursor()
    cursor.execute('''SELECT USERNAME,CLASS,SCORE FROM PLAYER INNER JOIN POINTS
            ON PLAYER.PLAYERID = POINTS.PLAYERID
            WHERE PLAYER.PLAYERID=POINTS.PLAYERID ORDER BY POINTS.SCORE DESC;''')

    result = cursor.fetchmany(5)
    
    connection.commit()
    connection.close()
    return result


def sum_of_Classes(Class):
    
    connection=sqlite3.connect('project1.db')
    connection.execute('PRAGMA foreign_keys=ON')
    cursor=connection.cursor()
    cursor.execute('''SELECT CLASS,SUM(SCORE) FROM PLAYER INNER JOIN POINTS
            ON PLAYER.PLAYERID = POINTS.PLAYERID
            WHERE CLASS=(?);''',(Class,))                           

    result = cursor.fetchall()
    if result[0][0]==None:
        result[0]=('{}'.format(Class),0)
        
    connection.commit()
    connection.close()
    return result[0]

def sum_of_sorting():
     connection=sqlite3.connect('project1.db')
     cursor=connection.cursor()
     cursor.execute('''SELECT SUM(INSERTION_CORRECT),SUM(BUBBLE_CORRECT),SUM(INSERTION_INCORRECT),SUM(BUBBLE_INCORRECT) FROM POINTS''')
     result=cursor.fetchall()
     connection.commit()
     connection.close()
     return result


def class_attempts(Class):
    connection=sqlite3.connect('project1.db')
    connection.execute('PRAGMA foreign_keys=ON')
    cursor=connection.cursor()
    cursor.execute('''SELECT CLASS,GAMEID FROM PLAYER INNER JOIN POINTS
            ON PLAYER.PLAYERID = POINTS.PLAYERID
            WHERE CLASS=(?);''',(Class,))
    result=cursor.fetchall()
    a=len(result)
    if a==0:
        a=1
    connection.commit()
    connection.close()
    return a


print(graphing(1))