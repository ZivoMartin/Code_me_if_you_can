import tkinter as tk
import subprocess
import psycopg2
from psycopg2 import OperationalError




# cursor = conn.cursor()
# cursor.execute("SELECT * FROM villes;")
# rows = cursor.fetchall()


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
		for j in range(size):
			self.problem_list[j]["button"].pack_forget()
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
		new = subprocess.run("touch code_me_if_u_can_file_test.py && pwd", shell=True, capture_output=True, text=True).stdout.split("\n")[0] + "/code_me_if_u_can_file_test.py"
		while(error == -1 and k<nb_tests):
			call_function = f"\nprint({self.problem_list[i]['title']}("
			nb_param = len(self.problem_list[i]["test"][k]) - 1
			for j in range(nb_param):
				call_function += str(self.problem_list[i]["test"][k][j])
				if(j != nb_param-1):
					call_function += ", "
			call_function += "))"
			with open(new, "w") as fichier:
				fichier.write(file_txt+call_function)
			output_test = subprocess.run(f"python {new}", shell=True, capture_output=True, text=True)
			if(output_test.stderr != "" or output_test.stdout.split("\n")[0] != str(self.problem_list[i]["test"][k][nb_param])):
				error = 1
				stdout = output_test.stdout
				stderr = output_test.stderr
			else:	
				k += 1
		txt="All tests passed, wp sir"
		if(error != -1):
			txt = ""
			nb_param = len(self.problem_list[i]["test"][k])-1
			txt = str(k)+" tests passed on "+str(nb_tests)+", input: "
			for j in range(nb_param):
				txt+=str(self.problem_list[i]["test"][k][j])
			if(stderr == ""):
				txt+=" output: "+stdout+" when "+str(self.problem_list[i]["test"][k][nb_param])+" was expected"
			else:
				txt += " stderr: " + stderr
		win_label = tk.Label(result, text=txt, bg="black", fg="white")
		win_label.pack(side="top")
		result.mainloop()


	def database(self):
		# conn = psycopg2.connect(
		# 	dbname="cmiyc",
		# 	user="postgres",
		# 	password="",
		# 	host="",
		# 	port=""
		# )
		# cursor = conn.cursor()
		# cursor.execute("SELECT * FROM problems_list;")
		# rows = cursor.fetchall()
		# cursor.close()
		# conn.close()
		# result_tab = []
		# nb_problems = len(rows)
		# for i in range(nb_problems):
		# 	result.append({"title": rows[i][0], "difficult": rows[i][1], "description": rows[i][2]})
		return [{"title": "maxi", "difficult": "easy", 
		"description": "Given an array of n integers, return the indice of the bigger of them, -1 for an empty tab. The name of your function is maxi and take one parameter",
		"test":[[[1, 2, 3, 4], 3], [[2, 2, 3], 2], [[], -1]]},
		{"title": "sort", "difficult": "easy", 
		"description": "Given an array of n integers, return the sorted array. The name of your function is array and take one parameter",
		"test":[[[2, 1, 3, 1], [1, 1, 2, 3]], [[54, 5, 8, 10, 11, 2, 3], [2, 3, 5, 8, 10, 11, 54]], [[], []]]}]


# def maxi(tab):
#    if(len(tab) == 0):
#       return -1
#    result = 0
#    the_max = tab[0]
#    for i in range(len(tab)):
#       if(tab[i]>the_max):
#          the_max = tab[i]
#          result = i
#    return i