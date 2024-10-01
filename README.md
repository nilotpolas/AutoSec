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
   /home/nilotpola/Desktop/ESSC/AutoSec-master/src/FunctionalCorrectness/PRESENT/present_tb
   ```
   ```
   /home/nilotpola/Desktop/ESSC/AutoSec-master/src/FunctionalCorrectness/AES/aes_tb.v
   ```
    **Step3: Simulate the verilog file using**
   ```
   iverilog -o simulation design.v design_tb.v
   ```
   ```
   vvp simulation
   ```

   Example: 

3. **Checking the AST-graphs**

4. **TVLA - analysis**: Automated scripts to be used after the design compiler is used to generate netlist.
   Example: ...
