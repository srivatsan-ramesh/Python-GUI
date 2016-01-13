try:
    import os,shutil
    from urllib2 import urlopen
    from cStringIO import StringIO
    from Tkinter import *
    import tkMessageBox
    from PIL import Image,ImageTk
except ImportError:
    raise ImportError('Install the required modules')
top = Tk()
top.title("STUDENT DETAILS")
data = 'data.txt'
menu = Menu()

def selected_details(l):
    def foo():
        stored_details(l)
    return foo

def refresh_menu():
    global menu
    try:
        with open(data) as f:
            lines = f.read().splitlines()
        menu.destroy()
        if len(lines)!=0:
            menu = Menu(top)
            top.config(menu = menu)
            submenu = Menu(menu)
            menu.add_cascade(label = 'Offline Data', menu = submenu)
            for l in lines:
                submenu.add_command(label = l, command = selected_details(l))
    except:
        print(0)

refresh_menu()
topframe = Frame(top)
topframe.pack()
bottomframe = Frame(top)


def save_details(img, s, roll):
    try:
        if not os.path.exists(roll):
            os.makedirs(roll)
        text_file = open(roll + '/' + roll + '.txt', "w")
        text_file.write("%s" % s)
        text_file.close()
        output = open(roll + '/' + roll + '.jpg',"wb")
        output.write(img)
        output.close()

        try:
            with open(data) as f:
                lines = f.read().splitlines()
            lines.index(roll)
        except:
            with open(data, "a") as myfile:
                myfile.write(roll+'\n')
        tkMessageBox.showinfo("Success", "Data Saved")
        refresh_menu()
        stored_details(roll)
    except:
        tkMessageBox.showerror("Error", "Error Saving Data")

def remove_details(roll):
    try:
        shutil.rmtree(roll)
        with open(data) as f:
            lines = f.read().splitlines()
        lines.remove(roll)
        f = open(data,'w')
        for item in lines:
            f.write("%s\n" % item)
        f.close()
        tkMessageBox.showinfo("Success", "Data Removed")
        refresh_menu()
        display_details(roll)
    except:
        tkMessageBox.showerror("Error", "Error Removing Data")

def get_from_tag(st, tag):
    return st.split('<'+tag+'>',1)[1].split('</'+tag+'>',1)

def display_details(inp):
    global bottomframe
    st=''
    try:
        st = urlopen("https://www.iitm.ac.in/students/sinfo/" + inp).read()
        if st=='':
            tkMessageBox.showerror("Error", "Error Retrieving Data From Internet")
        try:
            s = ''
            st = get_from_tag(st, 'table')[0]
            cont = get_from_tag(st, 'tr')
            s += 'NAME : '+get_from_tag(cont[0], 'strong')[0]
            st = cont[1]
            while st!='':
                cont = get_from_tag(st, 'tr')
                cont_td = get_from_tag(cont[0], 'td')
                s += '\n\n' + cont_td[0] + ' : '+ get_from_tag(cont_td[1],'td')[0]
                st = cont[1]
            image_url = "https://photos.iitm.ac.in/byroll.php?roll=" + inp.upper()
            u = urlopen(image_url)
            raw_data = u.read()
            u.close()
            image_file = Image.open(StringIO(raw_data))
            photo_image = ImageTk.PhotoImage(image_file)

            bottomframe.destroy()
            bottomframe = Frame(top)
            bottomframe.pack(side = BOTTOM)
            L1 = Label(bottomframe, image = photo_image)
            L1.grid(rowspan = 2, padx = (30,30), pady = (30,30))
            L2 = Label(bottomframe, text = s, justify = LEFT)
            L2.grid(row = 0, column = 1, padx = (10,10), pady = (10,10))
            B = Button(bottomframe, text ="SAVE", command = lambda :save_details(raw_data, s, inp.upper()))
            B.grid(row=1, column = 1, padx = (10,10), pady = (10,10) )
            top.mainloop()
        except:
            tkMessageBox.showerror('Error', 'Invalid Roll Number')
            bottomframe.destroy()
    except:
        tkMessageBox.showerror('Error', 'Check your Internet Connection')
        bottomframe.destroy()

def stored_details(roll):
    global bottomframe
    s = ''
    image_file = Image.open(roll+'/'+roll+'.jpg')
    photo_image = ImageTk.PhotoImage(image_file)
    with open(roll+'/'+roll+'.txt') as f:
        s = f.read()
    bottomframe.destroy()
    bottomframe = Frame(top)
    bottomframe.pack(side = BOTTOM)

    L1 = Label(bottomframe, image = photo_image)
    L1.grid(rowspan = 2, padx = (30,30), pady = (30,30))
    L2 = Label(bottomframe, text = s, justify = LEFT)
    L2.grid(row = 0, column = 1, padx = (10,10), pady = (10,10))
    B = Button(bottomframe, text ="REMOVE", command = lambda: remove_details(roll))
    B.grid(row=1, column = 1, padx = (10,10), pady = (10,10) )
    top.mainloop()

L1 = Label(topframe, text="ROLL NO ")
L1.pack( side = LEFT, fill = X)
E1 = Entry(topframe, bd =0)
E1.pack(side = LEFT, fill = X)

def helloCallBack():
    s = E1.get()
    if s == '':
        tkMessageBox.showwarning('Error', 'Enter Roll Number')
    else:
        try:
            with open(data) as f:
                lines = f.read().splitlines()
            lines.index(s.upper())
            stored_details(s.upper())
        except:
            display_details(s)
B = Button(topframe, text ="Submit", command = helloCallBack)

B.pack(side = LEFT, fill = X)

def func(event):
    helloCallBack()
top.bind('<Return>', func)
top.mainloop()
