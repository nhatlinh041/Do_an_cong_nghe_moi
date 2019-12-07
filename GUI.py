import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
import os
from tkinter import filedialog
from PIL import Image,ImageTk
import requests
import cv2
import shutil
from tkinter import messagebox
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.minsize(590,300)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")        
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        



class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.link_video='0'
        self.linkfile_id='.\\ids'
        self.link_file_img=self.linkfile_id

        self.controller = controller
        #tao listbox
        self.lbox_id=tk.Listbox(self,selectmode='single')
        self.lbox_id.place(x=10,y=10)
        #self.lbox_id.pack(side='left')
        
        #lay list file
        self.load_list_id()
        self.lbox_id.bind('<<ListboxSelect>>',lambda event: self.onclick_event())
        #add file
        

        #tao list image 
        self.lbox_list_img=tk.Listbox(self,selectmode='single')
        self.lbox_list_img.place(x=180,y=10)
        #self.lbox_list_img.pack(side='left')

        #double click len item trong list img 
        self.lbox_list_img.bind('<Double-1>',lambda event: self.onDoubleLeftClick())

        #default img
        self.image = Image.open('.\\Capture.jpg')
        self.image = self.image.resize((250, 250), Image.ANTIALIAS) ## The (250, 250) is (height, width)
        self.pic = ImageTk.PhotoImage(self.image)
        self.panel=tk.Label(self,image=self.pic)
        self.panel.place(x=190+130,y=10)
        #self.panel.pack()
        
        #add button Themid
        self.button_them_id=tk.Button(self,text='Thêm ID',command=lambda: controller.show_frame("PageOne"))
        self.button_them_id.place(x=10,y=180)
        #button_cmd.pack(side='bottom')


        #add button Xoa id
        self.button_cmd=tk.Button(self,text='Xóa ID',command=lambda: self.Xoa_id_click())
        self.button_cmd.place(x=89,y=180)

        #add button Them anh
        self.button_cmd=tk.Button(self,text='Thêm ảnh',command=lambda: self.fileDialog_them_anh())
        self.button_cmd.place(x=70+40+70,y=180)

        #add button Xoa anh
        self.btn_xoa_anh=tk.Button(self,text='Xóa ảnh',command=lambda: self.xoa_link_anh())
        self.btn_xoa_anh.place(x=70+40+40+100,y=180)


        #add button Refresh
        self.button_refresh=tk.Button(self,text='Refresh',command=lambda: self.load_list_id())
        self.button_refresh.place(x=10,y=220)


        #add button run cmd live cam
        self.button_run_cmd=tk.Button(self,text='Live cam',command=lambda: self.mycmd())
        self.button_run_cmd.place(x=10,y=255)

        ##add button run cmd video import
        self.button_run_cmd=tk.Button(self,text='Import video',command=lambda: self.mycmd_import())
        self.button_run_cmd.place(x=90,y=255)

        #Thêm textbox threshsold
        self.lbl_thresh_sold=tk.Label(self,text="Threshold:")
        self.lbl_thresh_sold.place(x= 89,y=225)
        self.txt_thresh_sold=tk.Entry(self)
        self.txt_thresh_sold.insert(tk.END ,'1.2')
        self.txt_thresh_sold.place(x= 159,y=225)

        #Thêm button xem ảnh của người lạ
        self.btn_nguoi_la=tk.Button(self,text='Danh sách người lạ',command=lambda: controller.show_frame("PageTwo"))
        self.btn_nguoi_la.place(x=190,y=255)

    def mycmd(self):
        os.system('start /wait cmd /k python main.py ./20180402-114759/saved_model.pb ./ids '+ self.link_video +' --threshold '+self.txt_thresh_sold.get())
    
    def mycmd_import(self):
        tmp=filedialog.askopenfilename(filetypes = (("mp4 file", "*.mp4"), ))
        if(len(str(tmp))>0):
            self.link_video =tmp
            os.system('start /wait cmd /k python main.py ./20180402-114759/saved_model.pb ./ids '+ self.link_video +' --threshold ' +self.txt_thresh_sold.get())
        else:
            messagebox.showinfo("Cảnh báo","Chưa chọn file video")
        self.link_video='0'
        
        
    def load_list_id(self):
        flist=os.listdir(self.linkfile_id)
        self.lbox_id.delete(0,tk.END)
        for item in flist:
            self.lbox_id.insert(tk.END,item)

    def onclick_event(self):
        # curselection() returns a tuple of indexes selected in listbox
        selection = self.lbox_id.curselection()
        if len(selection) > 0:
            self.link_file_img=self.linkfile_id
            self.lbox_list_img.delete(0,tk.END)
            self.link_file_img=self.link_file_img+'//'+self.lbox_id.get(selection[0])
            flist_img=os.listdir(self.link_file_img)
            for i in flist_img:
                self.lbox_list_img.insert(tk.END,i)
    
    def Xoa_id_click(self):
        # curselection() returns a tuple of indexes selected in listbox
        selection = self.lbox_id.curselection()
        if len(selection) > 0:
            self.link_file_img=self.linkfile_id+'//'+self.lbox_id.get(selection[0])
            flist_img=shutil.rmtree(self.link_file_img)
            self.load_list_id()

    def onDoubleLeftClick(self):
        selection = self.lbox_list_img.curselection()
        path = self.link_file_img+'//'+self.lbox_list_img.get(selection[0])
        self.image = Image.open(path)
        self.image = self.image.resize((250, 250), Image.ANTIALIAS) ## The (250, 250) is (height, width)
        self.pic = ImageTk.PhotoImage(self.image)
        self.panel.destroy()
        self.panel=tk.Label(self,image=self.pic)
        self.panel.place(x=180+130,y=0)
        #self.panel.pack()

    def xoa_link_anh(self):
        selection = self.lbox_list_img.curselection()
        if(len(selection)>0):
            i=self.lbox_list_img.index(selection[0])
            os.unlink(self.link_file_img+'//'+self.lbox_list_img.get(i))
            self.lbox_list_img.delete(i)
            
            
        else:
            messagebox.showinfo("Cảnh báo", "Chưa chọn hình để xóa")

    def fileDialog_them_anh(self):
        if(self.link_file_img=='.\\ids'):
            tk.messagebox.showinfo("Cảnh báo", 'Bạn chưa chọn id để thêm')
        else: 
            tmp=filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype =
            (("jpeg files","*.jpg"),("png file","*.png")) )
            if(len(str(tmp))>0):
                self.filename =tmp
                ##save img
                index1=str(self.lbox_list_img.get(tk.END,tk.END)).rfind('_')
                index2=str(self.lbox_list_img.get(tk.END,tk.END)).rfind('.')
                a=str(self.lbox_list_img.get(tk.END,tk.END))[index1+1:index2] 
                b=str(int(a)+1)
                c=str(self.lbox_list_img.get(tk.END,tk.END)).replace(a,b)
                c=c[0+2:len(c)-3]
                des = self.link_file_img+'\\'+c
                shutil.copy(self.filename, des)
                self.lbox_list_img.insert(tk.END,c)
            else:
                messagebox.showinfo("Cảnh báo","Chưa chọn file ảnh")
            

            




        


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #Thêm label 
        self.label = tk.Label(self, text="Nhập tên ID mới: ")
        self.label.place(x=10,y=10)

        #Thêm textbox id
        self.ten_id=tk.Entry(self)
        self.ten_id.place(x=10,y=30)

        #Thêm label 
        self.label = tk.Label(self, text="Danh sách ảnh: ")
        self.label.place(x=150,y=10)

        #thêm list ảnh
        self.lbox_list_img_id_moi=tk.Listbox(self,selectmode='single',)
        self.lbox_list_img_id_moi.place(x=150,y=30)

        #tao button browse anh
        self.btn_browse_anh=tk.Button(self, text='Browse',command=lambda: self.fileDialog())
        self.btn_browse_anh.place(x=150, y=200)

        #default img
        self.image = Image.open('.\\Capture.jpg')
        self.image = self.image.resize((250, 250), Image.ANTIALIAS) ## The (250, 250) is (height, width)
        self.pic = ImageTk.PhotoImage(self.image)
        self.panel=tk.Label(self,image=self.pic)
        self.panel.place(x=180+140,y=10)

        #double click vao link anh
        self.lbox_list_img_id_moi.bind('<Double-1>',lambda event: self.onDoubleLeftClick())

        #tao button xoa anh
        self.btn_xoa_anh=tk.Button(self,text='Xóa ảnh',command=lambda: self.xoa_link_anh())
        self.btn_xoa_anh.place(x=220,y=200)

        #toa button xac nhan luu id
        self.btn_luu_id=tk.Button(self,text='Xác nhận',command=lambda:[self.luu_id_moi()])
        self.btn_luu_id.place(x=200,y=269)

        self.button = tk.Button(self, text="Trở về",
                           command=lambda: [controller.show_frame("StartPage"),self.reload_page()])
        self.button.place(x=290,y=269)


    def fileDialog(self):
        self.filename =filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype =
        (("jpeg files","*.jpg"),("png file","*.png")) )
        if(len(str(self.filename))>0):
            self.lbox_list_img_id_moi.insert(tk.END,self.filename)
            img = Image.open(self.filename)
            photo = ImageTk.PhotoImage(img)
        else:
            messagebox.showinfo('Thông báo',"Chưa chọn ảnh")

    def onDoubleLeftClick(self):
        selection = self.lbox_list_img_id_moi.curselection()
        path = self.lbox_list_img_id_moi.get(selection[0])
        image = Image.open(path)
        image = image.resize((250, 250), Image.ANTIALIAS) ## The (250, 250) is (height, width)
        self.pic = ImageTk.PhotoImage(image)
        self.panel.destroy()
        self.panel=tk.Label(self,image=self.pic)
        self.panel.place(x=180+150,y=0)

    def reload_page(self):
        self.ten_id.delete(0,tk.END)
        self.lbox_list_img_id_moi.delete(0,tk.END)
        self.image = Image.open('.\\Capture.jpg')
        self.image = self.image.resize((250, 250), Image.ANTIALIAS) ## The (250, 250) is (height, width)
        self.pic = ImageTk.PhotoImage(self.image)
        self.panel=tk.Label(self,image=self.pic)
        self.panel.place(x=180+150,y=0)

    def xoa_link_anh(self):
        selection = self.lbox_list_img_id_moi.curselection()
        if(len(selection)>0):
            i=self.lbox_list_img_id_moi.index(selection[0])
            self.lbox_list_img_id_moi.delete(i)
        else:
            messagebox.showinfo("Cảnh báo", "Chưa chọn hình để xóa")
    def luu_id_moi(self):
        ten_id=str(self.ten_id.get())
        ten_id=ten_id.strip()
        ten_id=ten_id.replace(' ','_')
        path = ".\\ids\\"+ten_id
        os.mkdir(path)
        index=1
        for i in self.lbox_list_img_id_moi.get(0,tk.END):
            des = path+'\\'+ten_id+'_'+str(index)+'.jpg'
            shutil.copy(i, des)
            index=index+1
        



class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.linkfile_id='.\\stranger\\'
        #add Label
        self.lbl_danh_sach_nguoi_la=tk.Label(self,text='Danh sách:')
        self.lbl_danh_sach_nguoi_la.place(x=20,y=20)

        #tao listbox
        self.lbox_id=tk.Listbox(self,selectmode='single')
        self.lbox_id.place(x=20,y=40)

        #lay list file
        self.load_list_id()
        self.lbox_id.bind('<Double-1>',lambda event: self.onDoubleLeftClick_listbox())

        #default img
        self.image = Image.open('.\\Capture.jpg')
        self.image = self.image.resize((250, 250), Image.ANTIALIAS) ## The (250, 250) is (height, width)
        self.pic = ImageTk.PhotoImage(self.image)
        self.panel=tk.Label(self,image=self.pic)
        self.panel.place(x=180+130,y=10)

        #tao button trở về
        self.btn_tro_ve=tk.Button(self,text='Trở về',command=lambda: controller.show_frame("StartPage"))
        self.btn_tro_ve.place(x=100,y=300)

    def onDoubleLeftClick_listbox(self):
        selection = self.lbox_id.curselection()
        path = self.linkfile_id+'//'+self.lbox_id.get(selection[0])
        self.image = Image.open(path)
        self.image = self.image.resize((300, 300), Image.ANTIALIAS) ## The (250, 250) is (height, width)
        self.pic = ImageTk.PhotoImage(self.image)
        self.panel.destroy()
        self.panel=tk.Label(self,image=self.pic)
        self.panel.place(x=180+130,y=0)
        #self.panel.pack()

    def load_list_id(self):
        flist=os.listdir(self.linkfile_id)
        self.lbox_id.delete(0,tk.END)
        for item in flist:
            self.lbox_id.insert(tk.END,item)
            
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()