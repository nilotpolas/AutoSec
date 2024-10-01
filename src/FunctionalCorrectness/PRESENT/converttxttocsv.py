# Open the input and output files
with open('simulation_out_cfile.txt', 'r') as input_file, open('simulation_out_cfile_sorted.csv', 'w') as output_file:
# Open the input and output files
# with open('simulation_out_iverilog.txt', 'r') as input_file, open('simulation_out_iverilog_sorted.csv', 'w') as output_file:
    # Read each line from the input file
    lines = input_file.readlines()

    # Sort the lines based on the second value
    sorted_lines = sorted(lines, key=lambda line: int(line.split()[1]))

    # Write sorted lines to the output file
    for line in sorted_lines:
        # Split the line into separate values
        values = line.split()

        # Join the values with commas and write them to the output file
        output_line = ','.join(values)
        output_file.write(output_line + '\n')