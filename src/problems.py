import tkinter as tk
import subprocess

class Problem:
	
	def __init__(self, view):
		self.view = view
		if(self.view.tab_files[0]["path"] != ""):
			self.view.tab_files.append({"path": "PROBLEM", "button": tk.Button(self.view.top_frame, text="problem-list", fg="white", bg="blue", width=10)})
		else:
			self.view.tab_files[0]["path"] = "PROBLEM"
			self.view.tab_files[0]["button"].config(text="problem-list")

		self.indice_prob = len(self.view.tab_files)-1
		self.view.tab_files[self.indice_prob]["button"].config(command=lambda: self.click_on_prob_tab())
		self.view.tab_files[self.indice_prob]["button"].pack(side="left")
		self.problem_list = self.database()
		self.size_list = len(self.problem_list)
		for i in range(self.size_list):
			self.problem_list[i]["button"] = tk.Button(self.view.window, text=self.problem_list[i]["title"]+", difficulty: " + self.problem_list[i]["difficult"], height=3, command=lambda indice=i: self.start_prob(indice))
		self.click_on_prob_tab()
	
	def click_on_prob_tab(self):
		self.view.tab_files[self.view.current_tab]["button"].config(bg="gray")
		self.view.tab_files[self.indice_prob]["button"].config(bg="blue")
		self.view.current_tab = self.indice_prob
		self.view.main_entry.pack_forget()
		self.view.terminal.pack_forget()
		for i in range(self.size_list):
			self.problem_list[i]["button"].pack(side="top", fill="x")
		self.view.terminal.pack(side="bottom")
			

	def start_prob(self, i):
		self.view.tab_files[self.indice_prob]["path"] = "prob: "+str(i)
		size = len(self.problem_list)
		for i in range(size):
			self.problem_list[i]["button"].pack_forget()
		self.view.main_entry.pack(side="top")
		self.view.main_entry.insert("end", "#"+self.problem_list[i]["title"]+"\n#"+self.problem_list[i]["description"])
		
	def run_prob(self, i):
		result = tk.Tk()
		result.config(bg="black")
		result.geometry("200x200")
		result.title("Result")
		error = -1
		k = 0
		nb_tests = len(self.problem_list[i]["test"])
		stdout = ""
		stderr = ""
		file_txt = self.view.main_entry.get("1.0", "end")
		file_txt += "\n#martinzivojinovic1808200422210770\nprint("
		while(error == -1 and k<nb_tests):
			output = subprocess.run('print("hello")',shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			print(output.stderr.decode(), output.stdout.decode())
			k += 1
		error = 0
		k=0
		txt="All tests passed, wp sir"
		if(error != -1):
			txt = ""
			nb_param = len(self.problem_list[i]["test"][k])-1
			txt = str(k)+" tests passed on "+str(nb_tests)+", input: "
			for j in range(nb_param):
				txt+=str(self.problem_list[i]["test"][k][j])
			txt+=" output: "+""+" when "+str(self.problem_list[i]["test"][k][nb_param])+" was expected"
		win_label = tk.Label(result, text=txt, bg="black", fg="white")
		win_label.pack(side="top")
		result.mainloop()


	def database(self):
		return [{"title": "maxi", "difficult": "easy", 
		"description": "Given an array of n integers, return the indice of the bigger of them, -1 for an empty tab. The name of your function is maxi and take one parameter",
		"test":[[[1, 2, 3, 4], 3], [[2, 2, 3], 2], [[], -1]]}]