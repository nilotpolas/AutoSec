# Instructions to Install and Execute the Tool
## Installing the dependencies

```bash
  pip install -r requirements.txt
```
    
## Run the tool

cd to the folder where the script.py file is present.
Run the following command:
```
 $ python script.py <options>
```
The following operations are supported.


| Option  | Use |
| ------------- | ------------- |
| --topModule  | Name of the top topModule (mandatory)  |
| --inputFile  |  Name of the input file (it is mandatory too and shouldbe in the same directory as script.py |
| --rtlFile|the final verilog code file(default is output.v) |
| --bitWidth|specify the bitWidth for the rtl code |
| --checkBalancing|Set to 1 to verify the balancing (default is 0) |



## Note

- Temporary files will be generated in the tempFiles folder.
- The output Verilog file will be in the same folder as the input file.
  
## Getting Started: 

### Example 1: AES DOM Masked S-box
**Input:**
```bash
$ python3 script.py --topModule=sbox --inputFile=../test/AES/DOM/input.c --rtlFile=../test/AES/DOM/output.v --bitWidth=8
```
**Output:**
```
----------Nodes and edges------------
1308
2402
-------------------------------------
Max path weight 4
No of registers if added levelwise: 4752
Execution Time
--- 1.644021987915039 seconds ---
```

**Output Meaning:** 
- **Nodes and edges:**  
  - 1308 // number of nodes in the HLS-model  
  - 2402 // number of edges in the HLS-model  
- **Max path weight:** 4 // desired minimum latency  
- **No of registers if added levelwise:** 4752 // manual number of registers adding level-wise  
- **Execution Time:** 1.644021987915039 seconds  

### Example 2: PRESENT DOM Masked S-box
**Input:**
```bash
$ python3 script.py --topModule=sbox --inputFile=../test/PRESENT/DOM/input.c --rtlFile=../test/PRESENT/DOM/output.v --bitWidth=1
```
**Output:**
```
----------Nodes and edges------------
105
180
-------------------------------------
Max path weight 3
No of registers if added levelwise: 168
Execution Time
--- 0.04634523391723633 seconds ---
```

### Example 3: Checking balancing PRESENT DOM Masked S-box
**Input:**
```bash
$ python3 script.py --topModule=sbox --inputFile=../test/PRESENT/DOM/input.c --rtlFile=../test/PRESENT/DOM/output.v --bitWidth=1 --checkBalancing=1
```
**Output:**
```
----------Nodes and edges------------
105
180
-------------------------------------
Max path weight 3
No of registers if added levelwise: 168
Execution Time
--- 0.05016446113586426 seconds ---
Design is balanced.
```

**Output Meaning:**
- **Check balancing** verifies if the balancing is correct. Runs another pass.
- **Nodes and edges:** 105 and 180, respectively.
- **Max path weight:** 3 // checks the latency
- **No of registers if added levelwise:** 168 // checks the number of registers added levelwise
- **Execution Time:** 0.05016446113586426 seconds // takes a little more time than the actual balancing process
- **Design is balanced.**

## Bonus Features:
1. **Checking functional correctness via Simulation-Based Verification:**  
   **Step1: Install IARCUS-verilog**
   ```
   sudo apt-get install iverilog
   ```
   **Step2: Write a testbench file**
    We have testbenches for the AES and PRESENT S-boxes:
   ```
   AutoSec-master/src/FunctionalCorrectness/PRESENT/present_tb.v
   ```
   ```
   AutoSec-master/src/FunctionalCorrectness/AES/aes_tb.v
   ```
    **Step3: Generate the simulation input files**
   The input generator code generates the input simulation files: 
   ```
   AutoSec-master/src/FunctionalCorrectness/input_generator.py
   ```
   Run it using:
   ```
   python input_generator.py
   ```
   You can edit the *total_record = 50000* on line *37* in the file to specify the total number of records
   It asks for the following input
   ```
   Enter Size of N: 
   ```
   Here N means the number of samples you want to test the design for:
   Say we put 498, it gives us the test for that many number of samples into files "out0Comb.txt","out1Comb.txt"  with the 0-shares and 1-shares respectively.

    **Step4: Simulate the verilog file using**
   ```
   iverilog -o simulation design.v design_tb.v
   ```
   ```
   vvp simulation
   ```

   **Step5:Sort and compare the generated simulation file with the original S-box output**
   ```
   diff simulation_out_cfile_sorted.csv simulation_out_iverilog_sorted.csv
   ``` 

  2. **Checking the AST-graphs**
      We can print the AST after dummy node insertion (or at any step in the algorithm by re-using the same function) by uncommenting line 62 in:
     
    ```
    AutoSec-master/src/RegBalancer/src/main.py
    ```
  
    the line is: 
    
    ```
    save_graph(dfg_gen.dfg, "graph.png")
    ```
  
    The graph will be generated at:
    
    ```
    AutoSec-master/src/graph.png
    ```
    Note: Doing this for bigger designs (AES) is not scalable due to the screen being unable to render such a huge graph.
  3. **TVLA - analysis**: Automated scripts to be used after the design compiler is used to generate netlist.
     Example: ...
