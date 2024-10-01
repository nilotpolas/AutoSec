def write_file(output_filename,N):
	# Open the output file in write mode

	folder  = output_filename.split(".")[0]
	# 2 share of random + 1share of fixed
	files = [ (folder +"/"+folder+"_random.txt",2), (folder +"/"+folder+"_fixed.txt",1)]

	lines = []
	random2 = []
	with open(output_filename, 'w') as output_file:
		# Write the lines to the output file
		for (file_name,M) in files:
			tmp = read_file_to_list(file_name)
			lines.extend(tmp[:N])
			if M==2:
				random2.extend(tmp[N:M*N])
		lines.extend(random2)
		output_file.writelines(lines)

def read_file_to_list(filename):
	try:
	# Open the file in read mode
		with open(filename, 'r') as file:
			# Read all lines from the file and store them in a list
			lines = file.readlines()
			# Strip newline characters from each line
			lines = [line for line in lines]
			return lines
	except FileNotFoundError:
		print(f"Error: File '{filename}' not found.")
		return []


if __name__ == "__main__":
	out_files = ["out0Comb.txt","out1Comb.txt"]
	N = int(input("Enter Size of N: "))
	total_record = 50000
	
	if(N>total_record):
		print("Can't generate more than {0} testcases",total_record)
		exit
	for f in out_files:
		write_file(f,N)
