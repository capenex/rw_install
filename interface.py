import tkinter as tk
import threading
from tkinter import filedialog
import getRWPath
import os
from extractor import extract

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

disk = ['D']

class UI(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.root.title('rw_installer')

        self._v = tk.IntVar()   # 摇了我把这两个玩意实在不知道放哪
        self._v3_s = ""
        self.install_without_check = False
        # 属性
        self.gamePaths = []
        
        # 控件
        # 占位
        tk.Label(self.root, text="", width=PADDING_LEFT, height=PADDING_TOP).grid(row=0, column=0)
        tk.Label(self.root, text="", width=PADDING_RIGHT, height=PADDING_TOP).grid(row=0, column=4)
        
        self.txtV1 = tk.StringVar()
        self.txtV1.set('请选择模组')
        self.l1 = tk.Label(self.root, textvariable=self.txtV1, font=(FONT_FAMILY, FONT_SIZE_LABEL))
        self.l1.grid(row=1, column=1, columnspan=3)
        
        self.inpTxtV1 = tk.StringVar(value='')
        self.inp1 = tk.Entry(self.root, textvariable=self.inpTxtV1, font=(FONT_FAMILY, FONT_SIZE_LABEL))
        self.inp1.grid(row=2, column=0, columnspan=3)

        self.btn1 = tk.Button(self.root, text="浏览文件", font=(FONT_FAMILY, FONT_SIZE_BUTTON), command=self.browseFiles)
        self.btn1.grid(row=2, column=3, columnspan=2)

        self.txtV2 = tk.StringVar(value='请选择安装到的路径')
        self.l2 = tk.Label(self.root, textvariable=self.txtV2, font=(FONT_FAMILY, FONT_SIZE_LABEL))
        self.l2.grid(row=3, column=1, columnspan=3)

        self.inpTxtV2 = tk.StringVar(value='')
        self.inp2 = tk.Entry(self.root, textvariable=self.inpTxtV2, font=(FONT_FAMILY, FONT_SIZE_LABEL))
        self.inp2.grid(row=4, column=0, columnspan=3)

        self.btn2 = tk.Button(self.root, text="浏览路径", font=(FONT_FAMILY, FONT_SIZE_BUTTON), command=self.browsePaths)
        self.btn2.grid(row=4, column=3, columnspan=2)
        
        self.insBtn = tk.Button(self.root, text='安装', font=(FONT_FAMILY, FONT_SIZE_BUTTON), command=self.start_install)
        self.insBtn.place(x=30, y=BODY_HEIGHT-25-2*FONT_SIZE_BUTTON)
        self.cancelBtn = tk.Button(self.root, text='取消', font=(FONT_FAMILY, FONT_SIZE_BUTTON), command=self.stop)
        self.cancelBtn.place(x=BODY_WIDTH-30 - 20 - 2*FONT_SIZE_BUTTON, y=BODY_HEIGHT-25-2*FONT_SIZE_BUTTON)

        self.log_read()
        if self.gamePaths:    
            self.selectPath = self.gamePaths[0]
        else:
            self.selectPath = ""
        if self.inpTxtV2.get() != '':
            if getRWPath.is_1_15(self.inpTxtV2.get()):
                self.txtV2.set('(1.15)')
            else:
                self.txtV2.set('(1.14)')

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
        
        self.txtV3 = tk.StringVar(value="当前已扫描了D盘")
        if self._v3_s:
            self.txtV3.set(self._v3_s)
        self.l3 = tk.Label(self.toplevel, textvariable=self.txtV3, font=(FONT_FAMILY, FONT_SIZE_LABEL))
        self.l3.pack()

        self.l4 = tk.Label(self.toplevel, text='扫描其他盘', font=(FONT_FAMILY, FONT_SIZE_LABEL))
        self.l4.pack()
        self.inpTxtV3 = tk.StringVar(value='E')
        self.inp3 = tk.Entry(self.toplevel, textvariable=self.inpTxtV3, font=(FONT_FAMILY, FONT_SIZE_LABEL))
        self.inp3.pack()
        tk.Button(self.toplevel, text='扫描', font=(FONT_FAMILY, FONT_SIZE_BUTTON), command=self.scan_disk).pack()

        self.rdbLst = []
        for i, path in enumerate(self.gamePaths):
            if getRWPath.is_1_15(path):
                ver = '(1.15)'
            else:
                ver = '(1.14)'
            name = ver + ' ' + path
            self.rdbLst.append(tk.Radiobutton(self.toplevel, text=name, variable=self._v, value=i, font=(FONT_FAMILY, FONT_SIZE_PATH)))
            self.rdbLst[i].pack(anchor="w")

        tk.Button(self.toplevel, text="选好了", command=self.set_path, font=(FONT_FAMILY, FONT_SIZE_BUTTON)).pack()

    def start_install(self):
        threading.Thread(target=self._start_install).start()

    def _start_install(self):
        source = self.inpTxtV1.get()
        destin = self.inpTxtV2.get()
        if destin[-1] != '/' and destin[-1] != '\\':
            destin += '\\'
        getRWPath.last_use(destin)
        destin += "mods\\units\\"
        
        if not os.path.isabs(source):
            self.inpTxtV1.set('请输入绝对路径')
            return
        if not os.path.isfile(source):
            self.inpTxtV1.set('不受支持的文件类型')
            return
        source_suffix = os.path.splitext(source)[1]
        source = source.replace('/', '\\')
        source_name = (os.path.splitext(source)[0])[source.rindex('\\')+1:]
        
        if source_suffix == ".rwmod":
            if destin[-1] != '/' and destin[-1] != '\\':
                destin += '\\'
            os.system(f"move {source} {destin}{source_name}.rwmod")
        elif source_suffix in ['.rar', '.7z', '.zip']:
            source = source.replace('/', '\\')
            if not self.install_without_check:
                if os.path.exists(destin + source[source.rindex('\\')+1:]):
                    self.txtV1.set('文件已存在, 是否替换该文件')
                    self.install_without_check = True
                    return
                else:
                    extract(source, destin)
            else:
                extract(source, destin)
        else:
            self.inpTxtV1.set('安装失败')
            return
        self.inpTxtV1.set('安装成功')
        return

    def set_path(self):
        self.inpTxtV2.set(self.gamePaths[self._v.get()])
        if getRWPath.is_1_15(self.inpTxtV2.get()):
            ver = '(1.15)'
        else:
            ver = '(1.14)'
        txtV2Set = ver
        self.txtV2.set(txtV2Set)
        self.toplevel.destroy()
        
    def log_read(self):
        if not os.path.exists('info.log'):
            self.txtV2.set('首次使用，请点击浏览路径')
            return
        lst, Lastline, lastUse = getRWPath.read_log('info.log')
        lastLineList = Lastline.split()
        diskList = lastLineList[lastLineList.index('disk:')+1: -1]
        diskStr = ",".join(diskList)
        self._v3_s = '当前已扫描' + diskStr + '盘'
        self.inpTxtV2.set(lastUse)
        self.gamePaths.extend([tup[1] for tup in lst])

    def scan_disk(self):
        lst = getRWPath.get_path(self.inpTxtV3.get()[0])
        lst = getRWPath.log_found_paths(lst, [self.inpTxtV3.get()[0]])
        self.inpTxtV3.set(self.inpTxtV3.get()[0])
        self.txtV3.set('当前扫描了' + self.inpTxtV3.get()[0] + '盘')
        self.gamePaths = lst
        self.toplevel.destroy()
        self.browsePaths()


