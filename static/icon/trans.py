import os

for path in os.listdir("./"):
	if ".svg" in path:
		# path = "home_bc.svg"
		target = path.split(".")[0]+".png"
		command = "sudo inkscape -z -e %s -w 100 -h 100 %s" %(target, path)
		os.system(command)

