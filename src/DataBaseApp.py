import tkinter as tk
from tkinter import ttk
import sqlite3




#__init__() is a function like constructor in java
#Python dunder methods, magic methods

class Contacts:

    db_filename = 'contacts.db' #database 
    def __init__(self,root): #constructor
        self.root = root #self means this
        self.create_gui()
        #styling treeview and headings
        ttk.Style = ttk.Style()
        ttk.Style.configure("Treeview",font=('helvetica',10))
        ttk.Style.configure("Treeview.Heading",font=('helvetica',12,'bold'))

    def execute_db_query(self,query,parameters=()): #execute database
        with sqlite3.connect(self.db_filename) as conn: #connect to database, passing name of the database
            print(conn) # conn as alias
            print(' You have successfully connected to the Database')
            cursor = conn.cursor() # cursor is for interact with a database from python
            query_result = cursor.execute(query,parameters) # execute the query
            conn.commit() # necessary
        return query_result
    
    def create_gui(self): #all funtions
        self.create_left_icon()
        self.create_label_frame()
        self.create_message_area()
        self.create_tree_view()
        self.create_scrollbar()
        self.create_bottom_buttons()
        self.view_contacts()

    def create_left_icon(self): #create left icon
        
        photo = tk.PhotoImage(file = 'logo.gif') #PhotoImage class is for displaying the image 
        label = tk.Label(root,image=photo) #label contains an image
        label.image = photo #for displaying the image
        label.grid(row = 0, column=0) #position of the image
    

    def create_label_frame(self): #create label frame
        #????should i always write like self.root or can i just write root in some cases????
        #????sticky means direction????
        labelframe = tk.LabelFrame(self.root,text='Create a new contact',bg="peach puff",fg="black",font="helvetica 13") #Create a new label
        labelframe.grid(row=0,column=1,padx=8,pady=8,sticky='ew')
        tk.Label(labelframe,text='Name:',bg="thistle",fg="black").grid(row=1, column=1,sticky=tk.W,pady=2,padx=15)
        self.namefield = tk.Entry(labelframe) #where we enter the name, Entry means we are adding this to our labelframe
        self.namefield.grid(row=1,column=2,sticky=tk.W,pady=5,padx=2)
        tk.Label(labelframe,text='Email:',bg="RosyBrown2",fg="black").grid(row=2, column=1, sticky=tk.W, pady=2, padx=15)
        self.emailfield = tk.Entry(labelframe)
        self.emailfield.grid(row=2,column=2,sticky=tk.W,pady=5,padx=2)
        tk.Label(labelframe,text='Number:',bg="MistyRose2",fg="black").grid(row=3,column=1,sticky=tk.W,pady=2,padx=15)
        self.numfield = tk.Entry(labelframe)
        self.numfield.grid(row=3,column=2,sticky=tk.W,pady=5,padx=2)
        #????why does it have black frame and why activebackground is not working????
        tk.Button(root,text='Add Contact',command=self.on_add_contact_button_clicked,activebackground="lavender",bg= "white",fg="black").grid(row=2,column=1,padx=5,pady=5) #command is what will button do when we clicked on

    def create_message_area(self): #display messages
        self.message = tk.Label(text='',fg="bisque")
        self.message.grid(row=3,column=1)

    def create_tree_view(self): #
        self.tree = ttk.Treeview(height=10,columns=("email","number"))    
        self.tree.grid(row=6,column=0,columnspan=3)
        self.tree.heading("#0",text="Name",anchor=tk.W)
        self.tree.heading("email",text="Email Address",anchor=tk.W)
        self.tree.heading("number",text="Contact Number",anchor=tk.W)

    def create_scrollbar(self): 
        self.scrollbar = tk.Scrollbar(orient = 'vertical', command = self.tree.yview)
        self.scrollbar.grid(row=6,column=3,rowspan=10,sticky='sn')

    def create_bottom_buttons(self): #new buttons for delete and edit the data
        tk.Button(text='Delete Selected',command=self.on_delete_contact_button_clicked,bg="white",fg="black").grid(row=8,column=0,sticky=tk.E,pady=10,padx=20)
        tk.Button(text='Modify Selected',command=self.on_modify_selected_button_clicked,bg="white",fg="black").grid(row=8,column=1,sticky=tk.E)

    def open_modify_window(self): # it will open when you click modify button
        name = self.tree.item(self.tree.selection())['text'] # selecting datas from database
        old_number = self.tree.item(self.tree.selection())['values'][1]
        self.transient = tk.Toplevel() # this line allows me to open new window associated with our main window 
        self.transient.title('Update Contact')
        tk.Label(self.transient,text = 'Name: ').grid(row=0,column=1)
        tk.Entry(self.transient,textvariable=tk.StringVar(self.transient,value=name),state='readonly').grid(row=0,column=2)
        tk.Label(self.transient,text = 'Old Contact Number: ').grid(row=1,column=1)
        tk.Entry(self.transient,textvariable=tk.StringVar(self.transient,value=old_number),state='readonly').grid(row=1,column=2)

        tk.Label(self.transient, text = 'New Phone Number: ').grid(row=2,column=1)
        new_phone_number_entry_widget = tk.Entry(self.transient)
        new_phone_number_entry_widget.grid(row=2,column=2)

        tk.Button(self.transient,text='Update Contact',command=lambda: self.modify_contact(new_phone_number_entry_widget.get(),old_number,name)).grid(row=3,column=2,sticky=tk.E)

        self.transient.mainloop() # it will work until we enter to the exit

    def modify_contact(self,newphone,old_phone,name): # update contact
        query = 'UPDATE contacts_list SET number =? WHERE number =? and name=?' 
        parameters = (newphone,old_phone,name)
        self.execute_db_query(query,parameters)
        self.transient.destroy() # close modify window
        self.message['text'] = 'Phone number of {} modified.'.format(name)
        self.view_contacts() # fetch all datas again

    def on_modify_selected_button_clicked(self):
        self.message['text'] = ''
        try: 
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a contact to modify'
            return
        self.open_modify_window()


    def on_add_contact_button_clicked(self): # each time add button clicked this method will be called
        
        # we already control whether there is blank contact or not in new_contacts_validated function so there is no need to do here
        
        # self.message['text'] = '' # ???? why are we doing this
        # try:
        #     self.tree.item(self.tree.selection())['values'][0]
        # except IndexError as e:
        #     self.message['text'] = 'Please write information about this contact'
        #     return
        self.add_new_contact()
    
    def on_delete_contact_button_clicked(self):
        self.message['text'] = '' # ???? why are we doing this
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a contact to delete'
            return
        self.delete_contacts() #call actual function

        
    def add_new_contact(self): #adding new contact
        if self.new_contacts_validated():
            query = 'INSERT INTO contacts_list VALUES(NULL,?,?,?)' # inserting to the database, representing each column as a question mark
            parameters = (self.namefield.get(),self.emailfield.get(),self.numfield.get())
            self.execute_db_query(query,parameters) # function call
            self.message['text'] = 'New Contact {} added'.format(self.namefield.get())
            self.namefield.delete(0,tk.END)
            self.emailfield.delete(0,tk.END)
            self.numfield.delete(0,tk.END)
        else:
            self.message['text'] = 'name, email and number cannot be blank'

        self.view_contacts()

    def new_contacts_validated(self): # if the input is entered 
        return len(self.namefield.get()) != 0 and len(self.emailfield.get()) != 0 and len(self.numfield.get()) != 0
    
    def view_contacts(self): 
        items = self.tree.get_children() # used to return items
        for item in items:
            self.tree.delete(item) #????
        query = 'SELECT * FROM contacts_list ORDER BY name desc' 
        contact_entries = self.execute_db_query(query)
        for row in contact_entries:
            self.tree.insert('',0,text=row[1],values=(row[2],row[3]))

    def delete_contacts(self): # deleting the contacts
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM contacts_list WHERE name = ?'
        self.execute_db_query(query, (name,))
        self.message['text'] = 'Contact {} deleted'.format(name)
        self.view_contacts()

if __name__ == '__main__': #main method
    root = tk.Tk() #Tk(a tkinter package) creates the window , root is a window
    root.title('Contact List') #adding title to the window
    application = Contacts(root)
    root.mainloop() #execute __main__ method     