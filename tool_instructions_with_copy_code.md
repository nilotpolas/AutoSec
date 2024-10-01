
# Instructions to Install and Execute the Tool

## Steps:
1. Install dependencies:
   ```bash
   $ pip install -r requirements.txt
   ```

2. Run the tool:
   ```bash
   $ python script.py <options>
   ```

   Following are the options:
   - `--topModule` : Name of the top module (**mandatory**)
   - `--inputFile` : Name of the input file (**mandatory**, should be in the same directory as `script.py`)
   - `--rtlFile` : Name of the final Verilog code file (default is `output.v`)
   - `--bitWidth` : Specify the bit width for the RTL code
   - `--checkBalancing` : Set to 1 to verify the balancing (default is 0)

### Notes:
- Temporary files will be generated in the `tempFiles` folder.
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
   Example: ...

2. **Checking the AST-graphs**

3. **TVLA - analysis**: Automated scripts to be used after the design compiler is used to generate netlist.
   Example: ...
