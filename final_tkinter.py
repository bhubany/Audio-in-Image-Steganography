import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image,ImageTk
import sqlite3
import hashlib,sys,math

# Database
DB_FILE="my_db.db"
conn=''
cursor=''
def connect1():
    global conn
    try:
        conn = sqlite3.connect(DB_FILE)
        print("Connect database successfully")
    except:
        print("Error : ", sys.exc_info()[0])
    finally:
        conn.close()
connect1()

def create_table1():
    global conn, cursor
    sql="""
        CREATE TABLE IF NOT EXISTS user_details(
           user_id INTEGER PRIMARY KEY AUTOINCREMENT,
           user_name char (40),
           user_email CHAR(40) NOT NULL ,
           user_username CHAR(20) NOT NULL ,
           user_hash_password CHAR(32),
           user_password CHAR(20)
        );
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        print("Create table successfully")
    except:
        print("Error : ", sys.exc_info()[0])
    finally:
        cursor.close()
        conn.close()
create_table1()

# Inserting User Details Into Database
is_inserted=''
def insert_into_db(full_name,email,username,password):
    global cursor, conn,is_inserted
    # Hasing Password
    hash_pwd = hashlib.md5(password.encode())
    hash_pwd = hash_pwd.hexdigest()
    # Inserting
    checked=''
    sql = """SELECT * FROM user_details"""

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows)
    print(len(rows))
    check_already_reg="""SELECT * FROM user_details WHERE user_email=? AND user_username=?"""
    # cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))
    insert = """INSERT INTO user_details( user_name, user_email, user_username, user_hash_password, user_password) values(?, ?,?,?,?)"""
    values = (full_name,email,username,hash_pwd,password)
    check_value=(email,username,)
    # print("From insert into = ",full_name,email,username,hash_pwd,password)
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute(check_already_reg,check_value)
            rows = cursor.fetchall()
        except:
            rows=''
        for row in rows:
            print(row)
        print("Try Runnings")
        if len(rows)==0:
            cursor.execute(insert, values)
            conn.commit()
            is_inserted = "inserted"
        else:
            is_inserted = "already_registered"
    except:
        is_inserted = "error_occurs "
        print("Except Runs")
        print("Error : ", sys.exc_info()[0])
    finally:
        cursor.close()
        conn.close()
        return is_inserted


# GUI and Main Programming
class main_window (tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        walpaper=Image.open("Images/Final_Walpaper.jpg")
        walpaper = walpaper.resize((800, 500))
        photo=ImageTk.PhotoImage(walpaper)
        imgLabel=tk.Label(self,image=photo)
        imgLabel.image=photo
        imgLabel.place(x=0,y=0)

        # Header
        header=tk.Label(self,text="AUDIO STEGNOGRAPHY",font=("Terminal",30),bg="#1d60af",fg="white")
        header.place(x=150,y=100)
        # Login
        loginBtn=tk.Button(self,text="Login",font=("Terminal",15),bg="#1d60af",fg="white",bd=5,command=lambda: controller.show_frame(login_page))
        loginBtn.place(x=300,y=350)

        def register():
            window=tk.Tk()
            window.config(bg="deep sky blue")
            window.resizable(0,0)
            window.title("Register")
            # Full Name
            l1 = tk.Label(window, text="Full Name: ", font=("Arial Bold", 15), bg="deep sky blue",fg="#1d60af")
            l1.place(x=10, y=20)
            t1 = tk.Entry(window, width=40, bd=5)
            t1.place(x=200, y=20)
            # Email
            l2=tk.Label(window, text="Email: ",font=("Arial Bold",15),bg="deep sky blue",fg="#1d60af")
            l2.place(x=10, y=55)
            t2=tk.Entry(window, width=40,bd=5)
            t2.place(x=200,y=55)

            l3 = tk.Label(window, text="Username: ", font=("Arial Bold", 15), bg="deep sky blue",fg="#1d60af")
            l3.place(x=10, y=85)
            t3 = tk.Entry(window, width=40, bd=5,)
            t3.place(x=200, y=85)

            l4 = tk.Label(window, text="Password: ", font=("Arial Bold", 15), bg="deep sky blue",fg="#1d60af")
            l4.place(x=10, y=115)
            t4 = tk.Entry(window, width=40, bd=5, show="*")
            t4.place(x=200, y=115)

            l5 = tk.Label(window, text="Password: ", font=("Arial Bold", 15), bg="deep sky blue",fg="#1d60af")
            l5.place(x=10, y=145)
            t5 = tk.Entry(window, width=40, bd=5, show="*")
            t5.place(x=200, y=145)

            # Verifying Data for Sign Up
            def signup():
                if t1.get()!="" and t2.get()!="" and t3.get()!="" and t4.get()!="" and t5.get()!="":
                    if t4.get()==t5.get():
                        is_inserted=insert_into_db(full_name=t1.get(),email=t2.get(),username=t3.get(),password=t4.get())
                        if is_inserted=="inserted":
                            messagebox.showinfo("Sucess ","You have Been registered Sucessfully")
                        elif is_inserted =="already_registered":
                            messagebox.showinfo("Registered","Already Registered try loging")
                            window.destroy()
                        elif is_inserted=="error_occurs":
                            messagebox.showerror("Error ","Error occurs Try Again Later")
                        else:
                            messagebox.showerror("Error ","Error Occurs try again Later")
                    else:
                        messagebox.showerror("Error occurs: ","Both password doesnot matched")
                else:
                    messagebox.showerror("Error occurs: ","Please fill up all fields!")
                    window.destroy()


            sign_up_btn=tk.Button(window,text="Sign Up",font=("Arial Bold",15),bg="dark Green",fg="white",command=signup,bd=5)
            sign_up_btn.place(x=320,y=185)
            window.geometry("470x250")
            window.mainloop()

        # Register
        regBtn = tk.Button(self, text="Register", font=("Terminal", 15), bg="#1d60af", fg="white",bd=5,command=register)
        regBtn.place(x=400, y=350)

class login_page (tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        walpaper = Image.open("Images/Final_Walpaper.jpg")
        walpaper = walpaper.resize((800, 500))
        photo = ImageTk.PhotoImage(walpaper)
        imgLabel = tk.Label(self, image=photo)
        imgLabel.image = photo
        imgLabel.place(x=0, y=0)


        border=tk.LabelFrame(self,text="Login",bg='ivory',bd=10, font=("Arial",20))
        border.pack(fill="both",expand="yes",padx = 100, pady =100)

        # For Login
        l1=tk.Label(border, text="Username", font =("Terminal",15),bg="ivory")
        l1.place(x=50,y=80)
        t1=tk.Entry(border,width=30, bd= 5)
        t1.place(x=180, y=80)

        l2 = tk.Label(border, text="Password",font=("Terminal", 15),bg="ivory")
        l2.place(x=50, y=120)
        t2 = tk.Entry(border, width=30, bd=5, show="*")
        t2.place(x=180, y=120)

        back_button=tk.Button(border, text="Back",font=("Terminal",15),bg="dark blue",fg="white",bd=5,command=lambda : controller.show_frame(main_window))
        back_button.place(x=80,y=180)

        def verify():
            global conn, cursor
            email=t1.get()
            password=t2.get()
            hash_pwd = hashlib.md5(password.encode())
            hash_pwd = hash_pwd.hexdigest()
            sql = """SELECT * FROM user_details WHERE user_username=? AND user_hash_password=?"""
            value=(email,hash_pwd)
            try:
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute(sql,value)
                rows = cursor.fetchall()
                if len(rows) != 0:
                    controller.show_frame(user_profile)
                else:
                    messagebox.showerror("Error ","Username or Password didnot matched")
            except:
                print("Error : ", sys.exc_info()[0])
            finally:
                cursor.close()
                conn.close()
        b1=tk.Button(border,text="Submit",font=("Terminal",15),command=verify,bg="dark green",fg="white",bd=5)
        b1.place(x=350,y=180)

class user_profile(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        walpaper = Image.open("Images/Final_Walpaper.jpg")
        walpaper = walpaper.resize((800, 500))
        photo = ImageTk.PhotoImage(walpaper)
        imgLabel = tk.Label(self, image=photo)
        imgLabel.image = photo
        imgLabel.place(x=0, y=0)

        Label = tk.Label(self, text="USER PROFILE", font=("Arial Bold", 30),bg="deep sky blue",fg="white")
        Label.place(x=230, y=100)
        Button = tk.Button(self, text="Generate Image", font=("Arial", 15),bg="#20cc00",fg="white",bd=5, command=lambda: controller.show_frame(generate_page))
        Button.place(x=200, y=400)
        Button = tk.Button(self, text="Extract Audio", font=("Arial", 15),bg="#6529fb",fg="white",bd=5,command=lambda: controller.show_frame(extract_page))
        Button.place(x=450, y=400)

prev_stat_checker = ''
listx=[]
enter_pwd=''
pwd_box=''
password = ''
final_pwd=''
filename=''
class generate_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global filename
        walpaper = Image.open("Images/Final_Walpaper.jpg")
        walpaper = walpaper.resize((800, 500))
        photo = ImageTk.PhotoImage(walpaper)
        imgLabel = tk.Label(self, image=photo)
        imgLabel.image = photo
        imgLabel.place(x=0, y=0)

        def select_audio():
            global filename
            filename = filedialog.askopenfilename(initialdir="Y:/Minor Project/project/dc_test/",title="Select audio file",filetypes=(("wav files", "*.wav*"),("all files","*.*")))

            file_label = tk.Label(self, text=filename, bg="light blue", font=("Terminal", 10), fg="white")
            file_label.place(x=20, y=112)
            print(filename)
            # audio_filename=filename

        # Select Audio
        select_btn = tk.Button(self, text="Select Audio", font=("Terminal", 15), command=select_audio,bg="deep sky blue", fg="white")
        select_btn.place(x=600, y=110)

        # Set password
        set_pwd=tk.Label(self,text="Set password :",font=("Arial Bold",15),bg="dark blue",fg="white")
        set_pwd.place(x=250,y=150)
        # print("outside = ",filename)
        def selected_pwd(event):
            global enter_pwd , pwd_box,prev_stat_checker
            clic_res=clicked.get()
            if clic_res == "Yes":
                enter_pwd = tk.Label(self, text="Enter Password :",bg="deep sky blue",font=("Terminal",15),fg="white")
                enter_pwd.place(x=250, y=200)
                pwd_box=tk.Entry(self,width=30,bd=5)
                pwd_box.place(x=450,y=200)
            else:
                if prev_stat_checker=="Yes":
                    enter_pwd.destroy()
                    pwd_box.destroy()
            prev_stat_checker =clic_res
        clicked = tk.StringVar()
        clicked.set("No")
        drop = tk.OptionMenu(self,clicked,"Yes","No",command=selected_pwd)
        drop.place(x=450,y=150)

        # Start Generating Image

        def proceed_to_generate_image():
            global listx,password,final_pwd
            listx = [0]
            print("inside proceed =",filename)
            # print(listx)

            # For password
            if clicked.get()=="Yes":
                password = pwd_box.get()
                if password!="":
                    hash_pwd = hashlib.md5(password.encode())
                    hash_pwd = hash_pwd.hexdigest()
                    password_in_int = int(hash_pwd, 16)
                    # Checking int length of password
                    if (len(str(password_in_int))) == 38:
                        final_pwd = "0" + str(password_in_int)
                    else:
                        final_pwd = str(password_in_int)
                    for char in final_pwd:
                        listx.append(int(char))  # Appending values in list
                    print("Length = ",len(listx),"val = ",listx)
                else:
                    messagebox.showerror("Error","Enter password or select no to password")
            else:
                for char in range(1,40):
                    listx.append(0)
                print("Length = ",len(listx),"val = ",listx)
            # audio_file=audio_filename
            # For audio
            print("before checking = ",filename.lower())
            if filename.lower().endswith(('.wav')):
                with open(filename, "rb") as org_f:
                    org_bin = org_f.read()
                    org_f.close()
                binary_file=org_bin
                for i in range(0, len(binary_file)):
                    listx.append(binary_file[i])
                    i += 1

                # is extra bit added
                value_added = 0
                for i in range(0, 2):
                    if (len(listx) % 3) != 0:
                        listx.append(255)
                        value_added = value_added + 1
                    else:
                        pass
                listx[0] = value_added

                # Creating Image using RGB pattern
                lengthOfStr2 = len(listx)
                actual_length = lengthOfStr2 / 3
                w_h = math.sqrt(actual_length)
                width = height = int(w_h + 1)
                print(" Height = ", height, " Width = ", width)

                # Generating Image
                image1 = Image.new('RGBA', (height, width))

                i = 0
                for x in range(height):
                    for y in range(width):
                        if (i + 3) <= len(listx):
                            image1.putpixel((x, y), (listx[i], listx[i + 1], listx[i + 2], 255))
                            i = i + 3
                image1.save('generated image/final_test_image1.png')
                print("Image generated sucessfully")
                messagebox.showinfo("Sucess","Image has been generated sucessfully")
                # print("Length = ",len(listx),"val = ",listx)
            else:
                messagebox.showerror("Error","Please Select Wav File")

        proceed_btn=tk.Button(self, text="Proceed",font=("Terminal",15),command=proceed_to_generate_image,bg="deep sky blue",fg="white",bd=5)
        proceed_btn.place(x=370,y=280)
        Label = tk.Label(self, text="Image Generator from Audio", font=("Arial Bold", 30), bg="sky blue",
                         fg="dark Green")
        Label.place(x=100, y=30)
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(login_page),
                           bg="orange", fg="White", bd=5)
        Button.place(x=100, y=400)
        Button = tk.Button(self, text="Back", font=("Arial", 15), command=lambda: controller.show_frame(user_profile),
                           bg="orange", fg="White", bd=5)
        Button.place(x=650, y=400)

image_filename=''
password_list=[]
value_list=[]
final_audio_value=[]
pixel_count=0
count=0
pixel3=()
status_checker=False
class extract_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # global image_filename
        walpaper = Image.open("Images/Final_Walpaper.jpg")
        walpaper = walpaper.resize((800, 500))
        photo = ImageTk.PhotoImage(walpaper)
        imgLabel = tk.Label(self, image=photo)
        imgLabel.image = photo
        imgLabel.place(x=0, y=0)

        def select_image():
            global image_filename
            image_filename = filedialog.askopenfilename(initialdir="Y:/Minor Project/project/dc_test/generated image",title="Select audio file",filetypes=(("png files", "*.png*"),("all files","*.*")))
            file_label=tk.Label(self, text=image_filename,bg="light blue",font=("Terminal",10),fg="white")
            file_label.place(x=20,y=112)
            print(image_filename)
        # Select Audio

        Label = tk.Label(self, text="Audio Extraction From Image", font=("Arial Bold", 30),bg="sky blue",fg="dark Green")
        Label.place(x=100, y=30)
        select_btn = tk.Button(self, text="Select Image", font=("Terminal", 15), command=select_image,bg="deep sky blue",fg="white")
        select_btn.place(x=600, y=110)
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(login_page),bg="orange",fg="White",bd=5)
        Button.place(x=100, y=400)
        Button = tk.Button(self, text="Back", font=("Arial", 15), command=lambda: controller.show_frame(user_profile),bg="orange",fg="White",bd=5)
        Button.place(x=650, y=400)
        # Extracting Audi0
        def proceed_to_extract_audio():

            global password_list,value_list,pixel_count,status_checker,pixel3
            print(image_filename)
            image3 = Image.open(image_filename)
            width3, height3 = image3.size

            # checking if password is set
            append_count=0
            for x in range(0, height3):
                if status_checker == False:
                    for y in range(0, width3):
                        pixel3=()
                        if pixel_count == 14:
                            status_checker = True
                            break
                        pixel3 = image3.getpixel((x, y))
                        for i in range(0,3):
                            if append_count<40:
                                password_list.append(pixel3[i])
                                append_count = append_count + 1
                                # print("append count = ",append_count)
                        # print("count = ", pixel_count)
                        pixel_count = pixel_count + 1
                elif status_checker == True:
                    break

            count = 0
            check=''
            for p in range(1, 40):
                if password_list[p]==0:
                    check=True
                else:
                    check = False
                    break
            if check==True:
                # scanning Remaining pixels
                for x in range((height3)):
                    for y in range(width3):
                        pixel3 = image3.getpixel((x, y))
                        value_list.append(pixel3[0])
                        value_list.append(pixel3[1])
                        value_list.append(pixel3[2])
                # slicing Audio values
                for val in range(40, (len(value_list) - value_list[0])):
                    final_audio_value.append(value_list[val])
                final_audio_bytes = bytes(final_audio_value)
                if len(final_audio_value) != 0:
                    with open("audio files/generatedaudi.wav", "wb") as agf:
                        agf.write(final_audio_bytes)
                        agf.close()
                        messagebox.showinfo("Sucess","audio generated sucessfully")
                        print("Audio Generated Sucessfully")
                else:
                    messagebox.showerror("Error", "Error occurs while generating audio") # no pwd set
            else: #pwd set ask for Password
                window = tk.Tk()
                window.config(bg="deep sky blue")
                window.resizable(0, 0)
                window.title("Enter Password")
                # Password
                l1 = tk.Label(window, text="This image is password Encrypted.\n Enter Password to Scan ", font=("Terminal bold", 15), bg="deep sky blue", fg="Orange")
                l1.place(x=20, y=20)
                l2 = tk.Label(window, text="Password: ", font=("Arial Bold", 15), bg="deep sky blue", fg="#1d60af")
                l2.place(x=10, y=100)
                t2 = tk.Entry(window, width=30, bd=5)
                t2.place(x=140, y=100)
                # checking password with image password
                pwd_match_checked=''
                def submit_password():      # Start Working From Here
                    global pwd_match_checked
                    input_password=t2.get()
                    hash_pwd = hashlib.md5(input_password.encode())
                    hash_pwd = hash_pwd.hexdigest()
                    inp_pwd_in_int = int(hash_pwd, 16)
                    inp_pwd_in_str=str(inp_pwd_in_int)
                    if len(inp_pwd_in_str)==38:
                        inp_pwd_in_str="0"+inp_pwd_in_str
                    print(inp_pwd_in_str)
                    pwd_from_image=''
                    for i in range(0,39):
                        pwd_from_image=pwd_from_image+str(password_list[i+1])
                    if inp_pwd_in_str==pwd_from_image:
                        pwd_match_checked=True
                    else:
                        pwd_match_checked=False
                    if pwd_match_checked==True:
                        print('Password Matched Sucessfully')
                        messagebox.showinfo("Sucess","Password Matched Sucessfully! Audio generation is in process")
                        window.destroy()
                        # scanning Remaining pixels
                        for x in range((height3)):
                            for y in range(width3):
                                pixel3 = image3.getpixel((x, y))
                                value_list.append(pixel3[0])
                                value_list.append(pixel3[1])
                                value_list.append(pixel3[2])
                        # slicing Audio values
                        for val in range(40,(len(value_list)-value_list[0])):
                            final_audio_value.append(value_list[val])
                        final_audio_bytes=bytes(final_audio_value)
                        if len(final_audio_value)!=0:
                            with open("generated audio/generatedaudi.wav","wb") as agf:
                                agf.write(final_audio_bytes)
                                agf.close()
                                messagebox.showinfo("Sucess","Audio has been generated sucessfully")
                                print("Audio Generated Sucessfully")
                        else:
                            messagebox.showerror("Error","Error occurs while generating audio")

                    elif pwd_match_checked==False:
                        messagebox.showerror("Error","Enter Correct Password")
                        window.destroy()
                    else:
                        messagebox.showerror("Error ","Error occurs try again later")
                        window.destroy()
                # btn for password submission
                pwd_submit_btn=tk.Button(window,text="Submit",bd=5,bg="dark green",fg="white",command=submit_password)
                pwd_submit_btn.place(x=300,y=150)
                window.geometry("400x200")
                window.mainloop()
                count = count + 1
            print("check = ",check,"count = ",count)
            for x in range(height3):
                for y in range(width3):
                    pixel_count=pixel_count+1
                    pixel3 = image3.getpixel((x, y))
                    value_list.append(pixel3[0])
                    value_list.append(pixel3[1])
                    value_list.append(pixel3[2])
                    # print("Type = ",type(pixel3),"Val = ",pixel3)
                    # img_list.append(pixel3)

            with open("final_img.txt", "w") as fimg:
                fimg.write(str(value_list))
                fimg.close()


        proceed_btn = tk.Button(self, text="Proceed", font=("Terminal", 15), command=proceed_to_extract_audio,bg="deep sky blue",fg="white",bd=5)
        proceed_btn.place(x=300, y=180)
# Combining All Pages
class Application(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        # if we dont know the actual parameters to pe passed
        # Creating a Window
        window=tk.Frame(self)
        window.pack()

        window.grid_rowconfigure(0,minsize = 500)
        window.grid_columnconfigure(0,minsize = 800)

        # dct
        self.frames = {}
        for F in (main_window,login_page,user_profile,generate_page,extract_page):
            frame=F(window,self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(main_window)

            # self.show_frame(login_page)
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


app=Application()
app.maxsize(800,500)
app.mainloop()

# from tkinter import *
#
# new_window=''
# def open_window():
#     global new_window
#     new_window=Toplevel(root)
#     new_window.geometry("400x400")
#     new_window.title("New Window Title")
#     new_window.resizable(FALSE,FALSE)
#     lbl=Label(new_window,text="I am in New Window")
#     btn=Button(new_window,text="Close me!",command=lambda:new_window.destroy())
#     btn.pack()
#     lbl.pack()
# root=Tk()
#
# btn=Button(root,text="Open New Window",command=open_window)
# btn.pack(padx=10,pady=20)
#
# btn1=Button(root,text="Close New Window",command=lambda :new_window.destroy())
# btn1.pack()
#
# root.geometry("500x500")
# root.title("This is new Window")
# root.mainloop()



