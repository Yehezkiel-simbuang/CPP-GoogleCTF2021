#!usr/bin/env/python3
with open("cpp.c","r") as in_file,\
	open('cpp_indent.c', 'w') as out_file :
	indent = ""
	for line in in_file:
		if line.startswith("#if") :
			print(indent + line, end='',file=out_file)
			indent+= '  '
		elif line.startswith("#else") :
			print(indent[:-2] + line, end='',file = out_file)
		else :
			if line.startswith("#endif") :
				indent = indent[:-2]
			print(indent + line, end="", file = out_file)

