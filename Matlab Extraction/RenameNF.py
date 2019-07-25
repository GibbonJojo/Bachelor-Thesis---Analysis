import os
import shutil

os.chdir(r"C:\Users\jojou\OneDrive\Dokumente\Uni\BACHELORARBEIT\Analysis\NF")


for file in os.listdir():
    if file[11] == "_":
        prob = file[:3]
        num = file[10]
        fill = "0"

        os.rename(file, f"{prob}_NF_Run{fill}{num}_data.mat")


for file in os.listdir():
	if file [-7:-4] == "new":
		os.rename(file, file[:-3]+".mat")
