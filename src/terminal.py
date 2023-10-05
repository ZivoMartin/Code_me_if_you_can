import tkinter as tk
import subprocess

class Terminal:

    def __init__(self, view):
        self.view = view
        self.home = "/home/martin"
        self.current_repo = "[martin@martin ~]$ "
        self.config_terminal()
        self.view.run_button.config(command=self.run)
        self.histo = []
        self.pwd = "/home/martin"
        self.indice_histo = 0


    def config_terminal(self):
        self.view.terminal.insert("end", self.current_repo)
        self.view.terminal.bind("<Key>", lambda event : self.modif_terminal(event))
        self.view.terminal.bind("<Return>", lambda event : self.return_pressed(event))
        self.view.terminal.bind("<KeyRelease>", lambda event : self.key_release(event))
    
    def modif_terminal(self, event):
        ligne, colonne = map(lambda x: int(x), (self.view.terminal.index("insert").split('.')))
        last_line = int(self.view.terminal.index("end").split('.')[0])-1
        size_repo = len(self.current_repo)
        str_event = str(event)
        if(ligne != last_line or colonne < size_repo or ("BackSpace" in str_event and colonne == size_repo)):
            self.view.terminal.config(state="disabled")
        if("keysym=Up" in str_event):
            self.indice_histo -= 1
            if(self.indice_histo>=0 and len(self.histo) != 0):
                self.view.terminal.delete(str(last_line)+".0", "end")
                self.view.terminal.insert("end", "\n"+self.current_repo+self.histo[self.indice_histo])
            self.view.terminal.config(state="disabled")
        if("keysym=Down" in str_event):
            self.indice_histo += 1
            if(self.indice_histo<len(self.histo) and len(self.histo) != 0):
                self.view.terminal.delete(str(last_line)+".0", "end")
                self.view.terminal.insert("end", "\n"+self.current_repo+self.histo[self.indice_histo])
            self.view.terminal.config(state="disabled")
        elif("keysym=Tab" in str_event):
            last_line_txt = self.view.terminal.get(f"{last_line}.0", "end").split("]$ ")[1]
            split_space = last_line_txt.split(" ")
            last_chain_char = split_space[len(split_space)-1].split('\n')[0]
            slash_split = last_chain_char.split('/')
            last_word = slash_split[len(slash_split)-1]
            ls = subprocess.run(f"cd {self.pwd} && ls", shell=True, capture_output=True, text=True).stdout.split('\n')
            size = len(ls)
            for i in range(size):
                if(ls[i].startswith(last_word)):
                    start = len(last_word)
                    end = len(ls[i])
                    insert = ""
                    for j in range(start, end):
                        insert += ls[i][j]
                    self.view.terminal.insert("end", insert)
            self.view.terminal.config(state="disabled")

    def return_pressed(self, event):
        last_line = int((self.view.terminal.index('end-1c').split('.'))[0])
        self.term_command(self.view.terminal.get(f"{last_line}.0", "end").split("]$ ")[1], True)


    def term_command(self, command, change_path):
        self.histo.append(command.split('\n')[0])
        self.indice_histo += 1
        split_command = command.split(" ")
        if(split_command[0] == "clear\n"):
            self.view.terminal.delete("1.0", "end")
            self.view.terminal.insert("1.0", self.current_repo)
        elif(split_command[0] == "cd"):
            result = subprocess.run("cd "+self.pwd+" && cd "+split_command[1].split('\n')[0]+" && pwd", shell=True, capture_output=True, text=True)
            if(result.stderr != ""):
                self.view.terminal.insert("end","\n"+result.stderr)
            else: 
                self.pwd = result.stdout.split('\n')[0]
                pwd_splited = self.pwd.split('/')
                if(self.pwd == self.home):
                    self.current_repo = f"[martin@martin ~]$ "
                else:
                    self.current_repo = f"[martin@martin {pwd_splited[len(pwd_splited)-1]}]$ "
                self.view.terminal.insert("end", "\n")  
        else:   
            if(change_path):  
                command = "cd "+self.pwd + " && " + command
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            txt = self.view.terminal.get("1.0", "end-1c")
            if(result.stdout != ""):
                self.view.terminal.insert("end","\n"+result.stdout)
            elif(result.stderr != ""):
                self.view.terminal.insert("end","\n"+result.stderr)
            else:
                self.view.terminal.insert("end", "\n")
        self.view.terminal.insert("end", self.current_repo)
        self.view.terminal.config(state="disabled")

    def run(self):
        path = self.view.tab_files[self.view.current_tab]["path"]
        if(path.startswith("prob:")):
            self.view.problem_tab.run_prob(int(path.split(": ")[1]))
        elif(path == "PROBLEM"):
            return
        final_file = self.view.get_final_file(self.view.tab_files[self.view.current_tab]["path"])
        ext = final_file.split(".")[1]
        file = final_file.split(".")[0]
        if(ext == 'c'):
            self.term_command(f"gcc {self.view.tab_files[self.view.current_tab]['path']} -o {file} && ./{file}", False)
        elif(ext == 'py'):
            self.term_command(f"python {self.view.tab_files[self.view.current_tab]['path']}", False)
        elif(ext == 'cpp'):
            self.term_command(f"g++ {self.view.tab_files[self.view.current_tab]['path']} -o {file} && ./{file}", False)
        self.key_release(None)


    def key_release(self, event):
        self.view.terminal.config(state="normal")

