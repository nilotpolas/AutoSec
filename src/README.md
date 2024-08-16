Run `pip install -r requirements.txt`.

Run `python script.py <options>`. Following are the options:

- `--topModule` : Name of the top module (mandatory).
- `--inputFile` : Name of the input file (it is mandatory too and should be in the same directory as `script.py`).
- `--rtlFile` : The final Verilog code file (default is `output.v`).
- `--bitWidth` : Specify the bit width for the RTL code.
- `--checkBalancing` : Set to `1` to verify the balancing (default is `0`).

The temporary files will be generated in the `tempFiles` folder.  
The output Verilog file will be in the same folder as the input file.
