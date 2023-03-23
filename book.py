from tkinter import*
import tkinter.font as font
import mysql.connector 
class mysqlConfiguration():
     def __init__(self):
         print('constructor')
     def connect(self):
         self.myCon = mysql.connector.connect(
              host="localhost",
              user="root",
              password="shrusql@20")
         return self.myCon
     
     def create_database(self,db):
         mysqlobj = self.connect()
         cursor = mysqlobj.cursor()
         cursor.execute("create database " +db)
         cursor.execute("show Databases")
         records=cursor.fetchall()
         print('List of Databases present: ')
         print('-' * 20)
         for r in records:
             print(r)
             print('-' * 20)
         cursor.close()

     def close_connection(self):
          mysqlobj=self.connect()
          print('closing connection')
          mysqlobj.close()
          print('connection closed successfully')

     def create_table(self,db,table):
         mysqlobj=self.connect()
         cur=mysqlobj.cursor()
         cur.execute("Use " +db)
         print('Using Database ',db)
         cur.execute("create table if not exists " +table+ " (id\
                     INTEGER(100) NOT NULL AUTO_INCREMENT PRIMARY KEY,\
                     title text,author text,year integer,isbn integer)")
         print('table created successfully')
         cur.close()
     


class bookInventoryOperations(mysqlConfiguration):
     def addBook(self):
         print(self.title_text.get())
         print(self.author_name.get())
         print(self.year.get())
         print(self.isbn.get())
         self.insert(self.title_text.get(),self.author_name.get(),\
                     self.year.get(),self.isbn.get())
         self.list1.delete(0,END)
         self.clearEntrybox()
         self.list1.insert(0,'added successfully')


     def deleteBook(self):
         mysqlobj=self.connect()
         cur=mysqlobj.cursor()
         cur.execute("Use " + db)
         cur.execute("delete from " + table+ " WHERE id = %s" ,
                     (select_tup[0],))
         mysqlobj.commit()
         self.list1.delete(0,END)
         self.clearEntrybox()
         self.list1.insert(0, 'deleted successfully')
         cur.close()


     def updateBook(self):
        mysqlobj=self.connect()
        cur=mysqlobj.cursor()
        cur.execute("Use " + db)


        try:
             print(select_tup[0])
             cur.execute("update " + table+ " SET title=%s, author= %s ,year= %s, isbn= %s WHERE id= %s" ,
                    (self.title_text.get(),
                     self.author_name.get(),
                     self.year.get(),
                     self.isbn.get(), select_tup[0]))
             mysqlobj.commit()
             self.list1.delete(0,END)
             self.clearEntrybox()
             self.list1.insert(0, 'updated successfully')
             cur.close()
        except Exception as err:
            print('Please Select Book to update:',err)



     def clearEntrybox(self):
        self.title_text.delete(0,END)
        self.author_name.delete(0,END)
        self.year.delete(0,END)
        self.isbn.delete(0,END)
        self.list1.delete(0,END)

     def insert(self,title,author,year,isbn):
        try:
            mysqlobj=self.connect()
            cur=mysqlobj.cursor()
            cur.execute("Use " + db)
            query=" INSERT INTO " + table +\
                   ("(title,author,year,isbn) VALUES(%s, %s, %s,%s)")
            values=[(title,author,year,isbn)]
            cur.executemany(query,values)
            mysqlobj.commit()
            cur.close()
            print('inserted record successfully')
        except Exception as err:
           print('problem in insertion ...Please Check!!!',err)

     def get_selected_row(self,event):
        try:
            mysqlobj=self.connect()
            cur=mysqlobj.cursor()
            cur.execute("Use " + db)
            cur.execute("Select *from " + table)
            records=cur.fetchall()
            if len(records)==0:
                pass
            else:
                global select_tup
                self.index = self.list1.curselection()[0]
                select_tup = self.list1.get(self.index)
                print(select_tup[1])
                if (select_tup[1] in ['inserted','deleted','updated']):
                    return
                self.index = self.list1.curselection()[0]
                select_tup= self.list1.get(self.index)
                self.title_text.delete(0,END)
                self.title_text.insert(END, select_tup[1])
                self.author_name.delete(0,END)
                self.author_name.insert(END, select_tup[2])
                self.year.delete(0,END)
                self.year.insert(END, select_tup[3])
                self.isbn.delete(0,END)
                self.isbn.insert(END, select_tup[4])
        except IndexError:
          pass

     def showBooks(self):
        try:
            self.list1.delete(0,END)
            mysqlobj= self.connect()
            cur=mysqlobj.cursor()
            cur.execute("Use " + db)
            cur.execute("Select *From " + table)
            records= cur.fetchall()
            if len(records)==0:
                self.list1.insert(END, 'No records found')
            else:
                for rec in records:
                    self.list1.insert(END,rec)
                    print(rec)
        except Exception as e:
           print(e)



class  DisplayGUI(bookInventoryOperations):
     def __init__(self):
         window=Tk()

         self.l1 = Label(window,text ="Title", font='BOLD')
         self.l1.grid(row=0, column=0)

         self.l2=Label(window,text= "Author", font='BOLD')
         self.l2.grid(row=0,column=2)

         self.l3=Label(window,text="year", font='BOLD')
         self.l3.grid(row=1,column=0)

         self.l4=Label(window,text="ISBN",font='BOLD')
         self.l4.grid(row=1,column=2)

         self.title_text=Entry(window, width=30)
         self.title_text.grid(row=0,column=1)

         self.author_name=Entry(window, width=30)
         self.author_name.grid(row=0,column=3)

         self.year=Entry(window, width=30)
         self.year.grid(row=1, column=1)

         self.isbn=Entry(window, width=30)
         self.isbn.grid(row=1,column=3)

         self.list1=Listbox(window, height=6,width=40)
         self.list1.grid(row=2, column=0, rowspan=6, columnspan=2)
         self.list1.bind("<<ListboxSelect>>",\
                         self.get_selected_row)

         self.sb1=Scrollbar(window)
         self.sb1.grid(row=2, column=2, rowspan=6)

         self.list1.configure(yscrollcommand=self.sb1.set)
         self.sb1.configure(command=self.list1.yview)

         b1=Button(window, text="View All",\
                   width=25, command=self.showBooks, font='bold')
         b1.grid(row=2,column=3)

         self.b3=Button(window, text="Add Book",\
                        width=25, command=\
                        self.addBook, font='BOLD')
         self.b3.grid(row=4, column=3)


         self.b4=Button(window,text="Update Book",\
                        width=25, command=\
                        self.updateBook, font='BOLD')
         self.b4.grid(row=5, column=3)

         self.b5=Button(window,text="Clear Text Box",\
                        width=25, command=\
                        self.clearEntrybox , font='BOLD')
         self.b5.grid(row=7,column=3)

         self.b5=Button(window,text="Delete",\
                        width=25,command=\
                        self.deleteBook, font='BOLD')

         self.b5.grid(row=6,column=3)
         window.mainloop()

if __name__=='__main__':
    db= "Books_db"
    table= "book"
    conobj= mysqlConfiguration()
    conobj.create_database(db = "Books_db")
    conobj.create_table(db= "Books_db", table="book")
    DisplayGUI()
    conobj.close_connection()
    
                      
        
                     
        
        
