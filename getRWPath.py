import os
import configparser as inpar
import logging

progress = 0

def get_path(disk: str) -> list:
    if disk[0].upper() not in [chr(i) for i in range(65, 91)]:   
        print('驱动器错误')
        return []
    p = disk[0].upper() + ':'
    
    try:
        dir_lst = os.listdir(p)
        l = len(dir_lst)
    except FileNotFoundError as e:
        print(e)
        return []
    all = os.walk(p + '\\')
    pathLst = []
    progress_new = 0
    global progress
    for tup in all:
        path, dir, file = tup
        # r"E:\game\rw\1.15\Rusted Warfare\Rusted Warfare.exe"
        dirname = path[3:(path+'\\').index('\\', 3)]
        if dirname and dirname in dir_lst:
            progress = dir_lst.index(dirname)
            if progress != progress_new:
                print(f"{progress}/{l}")
                progress_new = progress
        if 'Rusted Warfare.exe' in file:
            pathLst.append(path)
    return pathLst


def is_1_15(path: str) -> bool:
    if path[-1] != '/' or path[-1] != '\\':
        path += '/'
    outpostpath = path + "assets/units/outpost/outpost.ini"
    try:
        conf = inpar.ConfigParser()
        conf.read(outpostpath)
        price = conf["core"]["price"]
        if price == "1500":
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def log_found_paths(pathLst: list, disks: list):
    logging.basicConfig(filename='info.log', filemode='w', format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%M-%Y %H:%M:%S", level=logging.INFO)
    for path in pathLst:
        ver = '1.15' if is_1_15(path) else '1.14'
        logging.info(f'   version:{ver} {path}') 
    if disks:
        s = " disk: "
        for d in disks:
            s += d[0] + " "
        logging.info(s + ' read')
    return pathLst

def read_log(filePath):
    lst = []
    lastline_2 = ""
    lastChoice = ""
    with open(filePath, 'r') as f:
        for line in f.readlines():
            
            if 'read' in line and 'disk' in line:
                lastline_2 = line
                continue
            if 'lastuse:' in line and 'Rusted Warfare' in line:
                path = line[line.index('lastuse:')+13:-1]                
                lastChoice = path
                continue
            ver = line[line.index('version:')+8: line.index('version:')+12]
            path = line[line.index('version:')+13:-1]
            lst.append((ver, path))
    return (lst, lastline_2, lastChoice)

def last_use(path):
    logging.basicConfig(filename='info.log', filemode='a', format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%M-%Y %H:%M:%S", level=logging.INFO)
    logging.info('   lastuse:     ' + path)