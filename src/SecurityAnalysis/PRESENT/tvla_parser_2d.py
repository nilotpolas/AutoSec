import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
# import re
import math
import sys
from tabulate import tabulate
plt.rcParams.update({'font.size': 14})
#based on the sampling rate.

#update the latency of the design. x ns ==> x * 1000
latency = 20 * 1000
percent = 0
font_size=20
# relative path to read .csv files and save generated plots.
path = "1cyclecomar:Vivado/"
output_file = "TVLA_Test_Results"
txt_format = ".txt"
html_format = ".html"
prefix = "traces_"
suffix = "ps.csv"


#title for t-value plot
t_value_plot_title = "PRESENT_COMAR T-Test Values"
#title for final T-Test plot
final_t_test_plot_title = "PRESENT_COMAR T-Test TVLA"
#title of the table
table_title = "PRESENT_COMAR TVLA Result"


#this variable used to save intermediate figure of sample point
figure_num = 0


def generate_table(data):
    # Start building the HTML table
    html = "<table border='1' cellspacing='0' cellpadding='5'>\n"
    
    # Add title row
    html += "<tr>"
    html += f"<th colspan='{len(data[0])}'>{table_title}</th>"
    html += "</tr>\n"
    
    # Add header row
    html += "<tr>"
    for header in data[0]:
        html += f"<th>{header}</th>"
    html += "</tr>\n"
    
    # Add data rows
    for row in data[1:]:
        html += "<tr>"
        for cell in row:
            if isinstance(cell, float):
                html += f"<td>{cell:.2f}</td>"  # Format float numbers to 2 decimal places
            else:
                html += f"<td>{cell}</td>"
        html += "</tr>\n"
    
    # Close the table
    html += "</table>"
    
    return html

    
def write_output_in_html_format(data):
	html_table = generate_table(data)
	with open(path+output_file+html_format, "w") as file:
		file.write(html_table)


# def show2dgraph(trace,T):
# 	plt.figure()
# 	#plt.plot(trace,T)
# 	plt.plot(trace, T, marker='o', color='blue', linestyle='-')  # Line with markers at data points

# 	# Plot the data points on the line
# 	plt.scatter(trace, T, color='blue')

# 	def thousands_formatter(x, pos):
# 		if(x>=1000000):
# 			return f'{x / 1000000:.1f}M'
# 		elif (x>=1000):
# 			return f'{x / 1000:.1f}k'
# 		else:
# 			return x
# 	# Set x-axis tick formatter
# 	plt.gca().xaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# 	plt.title(final_t_test_plot_title)
# 	plt.xlabel('No of Traces')
# 	plt.ylabel('T-Value')
# 	T_value_pos = 4.5
# 	T_value_neg = -4.5

# 	# Plotting
# 	plt.axhline(y=T_value_pos, color='red', linewidth=1)  # Draw a horizontal line at T_value_pos
# 	plt.axhline(y=T_value_neg, color='red', linewidth=1)  # Draw a horizontal line at T_value_neg
# 	plt.grid(True)
# 	plt.savefig(path+"final_T_value.png")
# 	#plt.show()



# def showgraph(T):
# 	plt.figure()
# 	plt.plot(T)
# 	plt.title(t_value_plot_title)
# 	plt.xlabel('Sample Count')
# 	plt.ylabel('T-Value')
# 	T_value_pos = 4.5
# 	T_value_neg = -4.5

# 	# Plotting
# 	plt.axhline(y=T_value_pos, color='red', linewidth=1)  # Draw a horizontal line at T_value_pos
# 	plt.axhline(y=T_value_neg, color='red', linewidth=1)  # Draw a horizontal line at T_value_neg
# 	plt.grid(True)
# 	plt.savefig(path+"traces_"+str(figure_num)+"ps.png")
# 	#plt.show()

def show2dgraph(trace,T):
	plt.figure()
	#plt.plot(trace,T)
	plt.plot(trace, T, marker='o', color='blue', linestyle='-')  # Line with markers at data points

	# Plot the data points on the line
	plt.scatter(trace, T, color='blue')

	def thousands_formatter(x, pos):
		if(x>=1000000):
			return f'{x / 1000000:.1f}M'
		elif (x>=1000):
			return f'{x / 1000:.0f}k'
		else:
			return x
	# Set x-axis tick formatter
	plt.gca().xaxis.set_major_formatter(FuncFormatter(thousands_formatter))

	plt.title(final_t_test_plot_title,fontsize=font_size)
	plt.xlabel('No of Traces',fontsize=font_size)
	plt.ylabel('T-Value',fontsize=font_size)
	T_value_pos = 4.5
	T_value_neg = -4.5

	# Plotting
	plt.axhline(y=T_value_pos, color='red', linewidth=1)  # Draw a horizontal line at T_value_pos
	plt.axhline(y=T_value_neg, color='red', linewidth=1)  # Draw a horizontal line at T_value_neg
	plt.grid(True)
	plt.xticks(fontsize=font_size-3)  # Adjust the fontsize as needed
	plt.yticks(fontsize=font_size-2)  # Adjust the fontsize as needed
	plt.savefig(path+"final_T_value.png",dpi=600, bbox_inches='tight')
	#plt.show()



def showgraph(T):
	plt.figure()
	plt.plot(T)
	plt.title(t_value_plot_title,fontsize=font_size)
	plt.xlabel('Sample Count',fontsize=font_size)
	plt.ylabel('T-Value',fontsize=font_size)
	T_value_pos = 4.5
	T_value_neg = -4.5

	# Plotting
	plt.axhline(y=T_value_pos, color='red', linewidth=1)  # Draw a horizontal line at T_value_pos
	plt.axhline(y=T_value_neg, color='red', linewidth=1)  # Draw a horizontal line at T_value_neg
	plt.grid(True)
	plt.xticks(fontsize=font_size)  # Adjust the fontsize as needed
	plt.yticks(fontsize=font_size)  # Adjust the fontsize as needed
	plt.savefig(path+"traces_"+str(figure_num)+"ps.png",dpi=600, bbox_inches='tight')
	#plt.show()


def tvla(set1TracesList,set2TracesList,NO_OF_SAMPLE_PER_TRACE):
	T = np.zeros(NO_OF_SAMPLE_PER_TRACE+1)

	set1TracesCardinality = set1TracesList.shape[0]
	set2TracesCardinality = set2TracesList.shape[0]
	
	data = []
	
	out_of_range = 0
	
	for i in range(NO_OF_SAMPLE_PER_TRACE):

		set1TracesMean = np.mean(set1TracesList[:,i])
		set2TracesMean = np.mean(set2TracesList[:,i])

		set1TracesVar = np.var(set1TracesList[:,i])
		set2TracesVar = np.var(set2TracesList[:,i])	

		meanDiff = (set1TracesMean - set2TracesMean)
		denomSum = (set1TracesVar/set1TracesCardinality) + (set2TracesVar/set2TracesCardinality)
		denom = math.sqrt(denomSum)
		if denom!=0:	
			t_value = meanDiff/denom
		else:
			t_value = 0

		T[i+1] = t_value
		
		data.append((abs(t_value),t_value))
		if (t_value)> 4.5:
			out_of_range+=1
		#print("sample",i+1,"T-Value",T[i])	
	
	
	final_t_value = np.mean(T)
	per_out_of_threshold = (out_of_range/NO_OF_SAMPLE_PER_TRACE)*100
	#print("Sample: ",per_out_of_threshold,"% T-Value: ",final_result)
	
	#print("Original Mean: ",np.mean(T))
	showgraph(T)
	return (final_t_value,per_out_of_threshold)
	
	
	
	'''
	record_discard_cnt = int(NO_OF_SAMPLE_PER_TRACE * percent)
	tmp_var = NO_OF_SAMPLE_PER_TRACE-1
	
	
	Sort the list based on the first value of each tuple
	sorted_data = sorted(data, key=lambda x: x[0])
	
	#modified_len = NO_OF_SAMPLE_PER_TRACE - record_discard_cnt
	
	while(tmp_var>modified_len):
		if(sorted_data[tmp_var][0]<4.5):
			break
		tmp_var-=1
	
	Tm = np.zeros(tmp_var)
	
	#for i in range(tmp_var):
	#	Tm[i] = sorted_data[i][1]

	final_result = np.mean(Tm)
	print("Modified Mean: ",final_result)
	#showgraph(Tm)
	return final_result
	'''

def fsdb_parser(file_path,NO_OF_SAMPLE_PER_TRACE):

	# Define the path to your CSV file
	csv_file_path = file_path
	#print("fileName: ",file_path)
	# Initialize lists to store data from each column
	xval_data = []
	pc_sbox_data = []

	# Read the CSV file and extract data
	with open(csv_file_path, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		next(reader)  # Skip the header row if it exists
		next(reader)
		for row in reader:
			# Extract data from each row and append to respective lists
			xval_data.append(float(row[0].strip()))
			pc_sbox_data.append(float(row[1].strip()))


	total_length = len(pc_sbox_data)
	extra_element = total_length % NO_OF_SAMPLE_PER_TRACE

	#creating 2d array based on no_of_sample_per_trace
	truncated_pc_sbox_data = pc_sbox_data[:-extra_element] if extra_element!=0 else pc_sbox_data

	pc_sbox_data_2d = np.reshape(truncated_pc_sbox_data, (-1, NO_OF_SAMPLE_PER_TRACE))

	rows,cols = pc_sbox_data_2d.shape
	
	#print(pc_sbox_data_2d)

	range1 = rows//3
	range2 = (2*rows)//3

	random1 = pc_sbox_data_2d[:range1]
	fixed = pc_sbox_data_2d[range1:range2]
	random2 = pc_sbox_data_2d[range2:]
	
	#print("--------------------------------------------------------------------------")
	#print("Random1: ",random1.shape[0],"fixed: ",fixed.shape[0],"Random2: ",random2.shape[0])
	array1 = np.vstack((random1,random2))
	array2 = fixed
	
	#print(array1)
	#print(array2)
	
	#print("--------------------------------------------------------------------------")
	#print("array1: ",array1.shape[0],"array2: ",array2.shape[0])
	#print("--------------------------------------------------------------------------")

	return array1,array2

 
if __name__ == '__main__':
	
	hpc2 = [275,240,225,215,175,85,75]
	hpc1 = [300,275,240,225,215,175,85,75]
	mult = [55,60,90,120,150,180,210] 	
	mult_p = [110,120,180,240,300,360,420]
	mult_r = [360,384,416,440,480,720,960,1200,1440,1680]#[330,360,540,720,900,1080,1260]#[220,240,360,480,600,720,840]
	vivadohpc1 = [43,52,97,300,375,450]
	vivadohpc2 = [43, 52, 97, 138, 150, 187, 225, 300, 375]
	vivadocomar = [43,52,97,150,375,450,525]
	file_num = vivadocomar
	
	#file_num = [90,120,150,210,115]
	#file_num = [300,275,250,240,225,215,200,175,135,125,105,85,75]

	
	data = [["Time Interval(ps)","Samples > |4.5| %"," TVLA Value ","Samples/Traces(N)","Total PlainText(3*N)","Total Traces(3*N*N)"]]

	no_of_files = len(file_num)

	T_values = np.zeros(no_of_files)
	trace_point = np.zeros(no_of_files)

	for i in range(no_of_files):
		f = file_num[i]
		figure_num = f
		filePath = path+prefix+str(f)+suffix

		# formula 
		NO_OF_SAMPLE_PER_TRACE = latency // f
		total_plain_text = 3 * NO_OF_SAMPLE_PER_TRACE
		Total_Traces = 3 * (NO_OF_SAMPLE_PER_TRACE**2)

		#print("Time:",f," NO_OF_SAMPLE_PER_TRACE:",NO_OF_SAMPLE_PER_TRACE)

		array1,array2 = fsdb_parser(filePath,NO_OF_SAMPLE_PER_TRACE)

		final_t_value , per_out_of_threshold = tvla(array1,array2,NO_OF_SAMPLE_PER_TRACE)
		T_values[i] = final_t_value
		trace_point[i] = Total_Traces


		data.append([f,per_out_of_threshold,final_t_value,NO_OF_SAMPLE_PER_TRACE,total_plain_text,Total_Traces])


	#showing the final T-value (mean of each sample)
	show2dgraph(trace_point,T_values)

	#Print data in tabular form
	table = tabulate(data, headers="firstrow", tablefmt="grid") 
	#print(table)

	with open(path+output_file+txt_format, "w") as file:
		file.write(table)
	
	write_output_in_html_format(data)
	#showing the result for the file from given below path
	print("Plots and final output saved in : ",path)
	


