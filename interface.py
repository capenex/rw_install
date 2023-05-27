import tkinter as tk
import threading
from tkinter import filedialog

FONT_SIZE_LABEL = 15
FONT_SIZE_BUTTON = 12
FONT_SIZE_PATH = 12
FONT_FAMILY = '等线'

PADDING_TOP = 0
PADDING_LEFT = 0
PADDING_BOTTON = 0
PADDING_RIGHT = PADDING_LEFT
BODY_WIDTH = 320
BODY_HEIGHT = 260
WINDOW_WIDTH = BODY_WIDTH + FONT_SIZE_LABEL * PADDING_LEFT * 2
WINDOW_HEIGHT = BODY_HEIGHT + FONT_SIZE_LABEL * (PADDING_TOP + PADDING_BOTTON) * 2



class UI(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.title('rw_installer')
        self._v = tk.IntVar()
        # 属性
        self.gamePaths = ['C:/path/to/file']
        self.selectPath = self.gamePaths[0]
        # 控件
        # 占位
        tk.Label(self.root, text="", width=PADDING_LEFT, height=PADDING_TOP).grid(row=0, column=0)
        tk.Label(self.root, text="", width=PADDING_RIGHT, height=PADDING_TOP).grid(row=0, column=4)
        
        self.txtV1 = tk.StringVar()
        self.txtV1.set('请选择模组')
        self.l1 = tk.Label(self.root, textvariable=self.txtV1, font=(FONT_FAMILY, FONT_SIZE_LABEL))
        self.l1.grid(row=1, column=1, columnspan=3)
        
        self.inpTxtV1 = tk.StringVar(value='')
        self.inp1 = tk.Entry(self.root, textvariable=self.inpTxtV1, font=(FONT_FAMILY, FONT_SIZE_LABEL))   # width=round(BODY_WIDTH/FONT_SIZE_LABEL)
        self.inp1.grid(row=2, column=0, columnspan=3)

        self.btn1 = tk.Button(self.root, text="浏览文件", font=(FONT_FAMILY, FONT_SIZE_BUTTON), command=self.browseFiles)
        self.btn1.grid(row=2, column=3, columnspan=2)

        self.txtV2 = tk.StringVar(value='请选择安装到的路径')
        self.l2 = tk.Label(self.root, textvariable=self.txtV2, font=(FONT_FAMILY, FONT_SIZE_LABEL))
        self.l2.grid(row=3, column=1, columnspan=3)

        self.inpTxtV2 = tk.StringVar(value='')
        self.inp2 = tk.Entry(self.root, textvariable=self.inpTxtV2, font=(FONT_FAMILY, FONT_SIZE_LABEL))   # width=round(BODY_WIDTH/FONT_SIZE_LABEL)
        self.inp2.grid(row=4, column=0, columnspan=3)

        self.btn2 = tk.Button(self.root, text="浏览路径", font=(FONT_FAMILY, FONT_SIZE_BUTTON), command=self.browsePaths)
        self.btn2.grid(row=4, column=3, columnspan=2)

        self.insBtn = tk.Button(self.root, text='安装', font=(FONT_FAMILY, FONT_SIZE_BUTTON), command=self.start_install)
        self.insBtn.place(x=30, y=BODY_HEIGHT-25-2*FONT_SIZE_BUTTON)
        self.cancelBtn = tk.Button(self.root, text='取消', font=(FONT_FAMILY, FONT_SIZE_BUTTON), command=self.stop)
        self.cancelBtn.place(x=BODY_WIDTH-30 - 20 - 2*FONT_SIZE_BUTTON, y=BODY_HEIGHT-25-2*FONT_SIZE_BUTTON)

    def mainloop(self):
        self.root.mainloop()
    
    def stop(self):
        self.root.destroy()
    

    def browseFiles(self):
        
        filename = filedialog.askopenfilename(
            initialdir = "/",
            title = "Select a File",
            filetypes = (("all files", "*.*"), ("all files", ""))
        )

        self.inpTxtV1.set(filename)
    
    def browsePaths(self):
        
        self.toplevel = tk.Toplevel(self.root)
        self.toplevel.geometry('400x200')
        self._v.set(0)
        for i, path in enumerate(self.gamePaths):
            tk.Radiobutton(self.toplevel, text=path, variable=self._v, value=i, font=(FONT_FAMILY, FONT_SIZE_PATH)).pack(anchor="w")
        
        tk.Button(self.toplevel, text="选好了", command=self.set_path, font=(FONT_FAMILY, FONT_SIZE_BUTTON)).pack()

    def verSelect(self):
        pass

    def start_install(self):
        threading.Thread(self._start_install).start()

    def _start_install(self):
        pass

    def set_path(self):
        self.inpTxtV2.set(self.gamePaths[self._v.get()])
        self.toplevel.destroy()
        
ui = UI()

ui.mainloop()
