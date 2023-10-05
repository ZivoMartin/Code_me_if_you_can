import tkinter as tk
from tkinter import filedialog
import subprocess
from src.problems import Problem

class View:

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1500x800")
        self.window.title("Code me if you can")
        self.current_tab = 0
        self.window.config(bg="black")
        self.approved_ext = ["c", "py", "cpp"]
        self.top_frame = tk.Frame(self.window, bg="black")
        self.top_frame.pack(side="top", fill="x")
        self.tab_files = [{"path": "", "button": tk.Button(self.top_frame, text="Empty", fg="white", bg="blue", width=10)}]
        self.tab_files[0]["button"].config(command=lambda: self.click_on_tab(0))
        self.run_button = tk.Button(self.top_frame, bg="blue", text="▶")
        self.run_button.pack(side="right")
        self.tab_files[0]["button"].pack(side="left")
        self.main_entry = tk.Text(self.window, width=300, height=35, foreground="white", bg="#{:02X}{:02X}{:02X}".format(24, 55, 69))
        self.main_entry.pack(side="top")
        self.terminal = tk.Text(self.window, width=300, height=20, foreground="white", bg="#{:02X}{:02X}{:02X}".format(30, 50, 69))
        self.terminal.pack(side="bottom")
        self.config_menu()
        self.problems = []
        self.problem_tab = None
        self.window.bind("<Control-s>", lambda event : self.save(event))

    def open_file(self):
        file_path = filedialog.askopenfilename()
        slash_split = file_path.split("/")
        if(slash_split[len(slash_split)-1].split('.')[1] in self.approved_ext):
            if(self.tab_files[self.current_tab]["path"] != ""):
                self.tab_files.append({"path": file_path, "button": tk.Button(self.top_frame, text=self.get_final_file(file_path), fg="white", bg="blue", width=10)})
                i = len(self.tab_files)-1
                self.tab_files[i]["button"].pack(side="left")
                self.tab_files[i]["button"].config(command=lambda indice=i: self.click_on_tab(indice))
                self.click_on_tab(i)
            else:
                self.tab_files[self.current_tab]["path"] = file_path
                self.tab_files[self.current_tab]["button"].config(text=self.get_final_file(file_path))
            with open(file_path, "r") as fichier:
                contenu_fichier = fichier.read()
                self.main_entry.delete("1.0", "end")
                self.main_entry.insert("end", contenu_fichier)
                
    def save(self, event):
        txt = self.main_entry.get("1.0", "end-1c")
        if(self.tab_files[self.current_tab]["path"] == ""):
            if(txt != ""):
                new = filedialog.asksaveasfilename(defaultextension=".txt")
                subprocess.run(f"touch {new}", shell=True)
                with open(new, "w") as fichier:
                    fichier.write(txt)
                self.tab_files[self.current_tab]["path"] = new
        else:
            with open(self.tab_files[self.current_tab]["path"], "w") as fichier:
                    fichier.write(txt)



    def config_menu(self):
        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Do some funny problems ?", command=self.open_problem_tab)

    
    def get_file_extention(self, file):
        file, ext = map(lambda x: x, (file.split('.')))
        return file, ext


    def get_final_file(self, path):
        slash_split = path.split("/")
        return slash_split[len(slash_split)-1]

    def click_on_tab(self, i):
        if(self.tab_files[self.current_tab]["path"] == "PROBLEM"):
            size = len(self.problem_tab.problem_list)
            for i in range(size):
                self.problem_tab.problem_list[i]["button"].pack_forget()
        self.main_entry.pack(side="top")
        print(i, self.current_tab)
        if(i != self.current_tab):
            self.tab_files[self.current_tab]["button"].config(bg="gray")
            self.tab_files[i]["button"].config(bg = "blue")

            with open(self.tab_files[i]["path"], "r") as fichier:
                contenu_fichier = fichier.read()
                self.main_entry.delete("1.0", "end")
                self.main_entry.insert("end", contenu_fichier)
            self.current_tab = i
    
    def open_problem_tab(self):
        self.problem_tab = Problem(self)