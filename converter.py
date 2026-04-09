# start : 06/04/26 18:53:31
# end   : 06/04/26 21:26:58

from customtkinter import *
from subprocess import run
from os import path, mkdir, listdir as ls
from psutil import disk_partitions as drives

class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("converter!!")
        self.geometry("400x300")
        self.minsize(width=400, height=300)
        self.font = CTkFont(family="Consolas", size=18)

        self.frame_entry = CTkFrame(self, fg_color=self.cget("bg"))
        self.entry_path = CTkEntry(self.frame_entry, placeholder_text="C:/", font=self.font, width=250)
        self.entry_input = CTkEntry(self.frame_entry, placeholder_text="ogg", font=self.font, width=55)
        self.label_text = CTkLabel(self.frame_entry, text="->", font=self.font)
        self.entry_output= CTkEntry(self.frame_entry, placeholder_text="mp3", font=self.font, width=55)

        self.frame_gridDebug = CTkFrame(self, fg_color=self.cget("bg"))
        self.label_error = CTkLabel(self.frame_gridDebug, text="error are displayed here", font=self.font)


        self.frame_entry.pack(pady=25, fill=Y, expand=True)
        self.entry_path.pack(pady=2, anchor=N)
        self.entry_input.pack(side=LEFT, anchor=N)
        self.label_text.pack(side=LEFT, anchor=N, expand=True)
        self.entry_output.pack(side=RIGHT, anchor=N)

        self.frame_gridDebug.pack(side=BOTTOM, fill=X)
        self.label_error.pack(side=BOTTOM)

        self.entry_path.bind(sequence="<Return>", command=(lambda x : self.verify_path()))
        self.entry_input.bind(sequence="<Return>", command=(lambda x : self.verify_path()))
        self.entry_output.bind(sequence="<Return>", command=(lambda x : self.verify_path()))

    def getPath_link(self)->str:
        path = self.entry_path.get().replace("/", "\\").strip()
        return path if path.endswith("\\") else path+"\\"

    def getInput(self)->str:
        input = self.entry_input.get().replace(".", "").strip().lower()
        return input if len(input) != 0 else "ogg"

    def getOutput(self)->str:
        output = self.entry_output.get().replace(".", "").strip().lower()
        return output if len(output) != 0 else "mp3"

    def getDrives(self)-> list:
        return [drive._asdict()["device"] for drive in drives()]

    def DEBUG(self):
        print(f"path : {self.getPath_link()}")
        print(f"input : {self.getInput()}")
        print(f"output : {self.getOutput()}")

    def ERROR(self, message : str):
        self.label_error.configure(text=message)

    def GREEN(self):
        self.label_error.configure(text_color="black")

    def RED(self):
        self.label_error.configure(text_color="red")

    def verify_path(self):
        value = self.getPath_link()
        self.GREEN()
        if len(value) > 3:
            if value[:3].upper() in self.getDrives():
                if path.exists(value):

                    self.ERROR("no error")
                    self.title("converter!! running")
                    self.convert(value)

                else:
                    self.RED()
                    self.ERROR(f"{value} doesn't exist")
            else:
                self.RED()
                self.ERROR(f"'{value[:3]}' is not a drive")
        else:
            self.RED()
            self.ERROR(f"path entry is not valid")
        self.DEBUG()

    def createDir(self, dirPath):
        try:
            mkdir(dirPath)
        except FileExistsError as e:
            pass

    def writeLogs(self, filename="", e=""):
        try:
            with open(f"{dirpath}converterLOGS.txt", "x") as xf:
                xf.write(f"error with {filename} : {e}")
        except FileExistsError:
            with open(f"{dirpath}converterLOGS.txt", "w") as wf:
                wf.write(f"error with {filename} : {e}")

    def makeCmd(self, pathI, fileI, pathO, fileO)->str:
        return f"ffmpeg -i \"{pathI}{"".join(fileI)}\" \"{pathO}{"".join([fileO[0], "."+self.getOutput()])}\""

    def convert(self, dirPath: str):
        c_dirPath = f"{dirPath}CONVERTED\\"
        self.createDir(c_dirPath)
        for file in ls(dirPath):
            file_s = path.splitext(file) #file splitext
            if file_s[-1][1:] == self.getInput():
                command = self.makeCmd(dirPath, file_s, c_dirPath, file_s)
                try:
                    run(["powershell", "-NoProfile", "-Command", command], encoding="UTF-8", stderr=1)
                except Exception as e:
                    self.writeLogs(dirPath+file, e)
        else:
            self.title("converter!! done")




Main = App()

Main.mainloop()
