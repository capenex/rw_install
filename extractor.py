import os

def extract(source, destin):
    current_dir = os.getcwd()
    command = f"{current_dir}\\7z\\7z.exe x {source} -o\"{destin}\" -y"
    print(os.system(command))

