from tkinter import ttk,filedialog
import tkinter as tk
import models
import os
from ttkbootstrap import Style
class window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        Style('superhero')
        self.title("search")
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "home.ico")
        self.iconbitmap(icon_path)
        self.frame_header()
        self.bar_1()
        self.bar_2()
        self.columnconfigure(0, weight=1)
        self.style = ttk.Style(self)
        self.style.configure("TRadiobutton", font=('arial', 12))
        self.style.configure('TButton', font=('Arial', 12, 'bold'))
        self.output_bar3()
        self.config()
        
    def frame_header(self):
        title = ttk.Label(self, text='Write text here', font=('arial', 22))
        title.grid(row=0, column=0)
        header = ttk.Frame(self)
        self.search_text = ttk.Entry(header, font=('arial', 25), justify='center')
        self.search_text.grid(row=0, column=0, rowspan=2, sticky='ew')
        header.grid(row=1, column=0, sticky='ew', padx=30)
        header.columnconfigure(0, weight=100)

    def bar_1(self):
        title = ttk.Label(self, text='file path', font=('arial', 20))
        title.grid(row=2, column=0, padx=30, pady=(15, 0))
        bar_1 = ttk.Frame(self)
        bar_1.grid(row=3, column=0, sticky='ew', padx=30)
        self.path_field = ttk.Entry(bar_1, font=('Arial', 16))
        self.path_field.grid(row=0, column=0, rowspan=2, sticky='ew')
        self.button_path = ttk.Button(bar_1, text='file/directory', padding=(5, 10))
        self.button_path.grid(row=0, column=1, rowspan=2,padx=(0,8))
        self.file_or_folder = tk.StringVar()
        self.file = ttk.Radiobutton(bar_1, text='file', value='file', variable=self.file_or_folder)
        self.directory = ttk.Radiobutton(bar_1, text='folder', value='folder', variable=self.file_or_folder)
        self.file.grid(row=0, column=2, sticky='ew')
        self.directory.grid(row=1, column=2, sticky='ew')
        bar_1.columnconfigure(0, weight=20)
        bar_1.columnconfigure(1, weight=0)
        bar_1.columnconfigure(2, weight=0)

    def bar_2(self):
        self.slider = ttk.Scale(self, from_=0, to=100, length=300)
        self.slider.grid(row=4, column=0, padx=30, pady=(15, 0))
        self.slider.set(80)
        self.slider_label = ttk.Label(self, text=f'sensitivity {80}')
        self.slider_label.grid(row=5, column=0)

    def output_bar3(self):
        self.check = ttk.Button(self, text='check text', padding=(10, 10))
        self.check.grid(row=6, column=0, padx=30, pady=(15, 0))
        self.status = ttk.Label(self, text='Welcome', font=('arial', 15))
        self.status.grid(row=7, column=0, padx=30, pady=(15, 0))

        # Create a canvas with a scrollbar
        self.output_canvas = tk.Canvas(self)
        self.output_canvas.grid(row=8, column=0, padx=30, pady=(15, 0), sticky="nsew")

        self.output_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.output_canvas.yview)
        self.output_scrollbar.grid(row=8, column=1, sticky="ns")
        self.output_canvas.configure(yscrollcommand=self.output_scrollbar.set)

        self.output_frame = ttk.Frame(self.output_canvas)
        self.output_canvas.create_window((0, 0), window=self.output_frame, anchor="nw")

        self.output = ttk.Label(self.output_frame, font=('arial', 15))
        self.output.pack(fill="both", expand=True)

        self.output_frame.bind("<Configure>", self.update_scrollregion)

        self.output_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def update_scrollregion(self, event=None):
        self.output_canvas.configure(scrollregion=self.output_canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.output_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    def print_error(func):
        def wrapper(self,*args, **kwargs):
            try:
                return func(self,*args, **kwargs)
            except Exception as e:
                self.msg(f"Error occurred in function '{func.__name__}': {str(e)}",1)
        return wrapper
    @print_error
    def get_file_path(self):
        self.path_field.delete(0, 'end')
        if self.file_or_folder.get() == 'file':
            file_path = filedialog.askopenfilename(filetypes = [('PDF files', '*.pdf'), ('Word files', '*.docx')])
            self.path_field.insert('end',file_path)
            self.msg('file is selected',0)
        elif self.file_or_folder.get() == 'folder':
            folder_path = filedialog.askdirectory()  
            self.path_field.insert('end',folder_path)
            self.msg('directory is selected',0)

    @print_error
    def config(self):
        self.button_path.configure(command=self.get_file_path)
        self.check.configure(command=self.check_process)
        self.slider.bind("<ButtonRelease-1>", self.check_process)
    @print_error
    def check_process(self,*args,**kwargs):
        self.slider_label.configure(text=f'sensitivity {int(self.slider.get())}')
        result = models.pdf_Check((self.path_field.get()))
        out = result.check_it((self.search_text.get()),int(self.slider.get()))
        text_output=''
        for i,v in out.items():
            for l in v:
                text_output+=(f"{i[-30:]:<40} | {'page        ' if i.endswith('.pdf') else 'paragraph' }   number   {l :<20}")+'\n'
        self.output.configure(text=text_output)
        self.msg('files is checked',0)
    def msg(self,text,type):
        if type==0:
            self.status.configure(text=text,background='green',foreground='white',font=('arial',12,'bold'))
        elif type==1:
            self.status.configure(text=text,background='red',foreground='white',font=('arial',12,'bold'))
        else:
            self.status.configure(text=text,background='black',foreground='white',font=('arial',12,'bold'))

if __name__=="__main__":
    project = window()
    project.mainloop()
    


