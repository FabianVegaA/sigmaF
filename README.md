# SigmaF

The project sigmaF search to create a new program language in the paradigm functional.

SigmaF is a programming language of the Functional paradigm, inspired by languages like Haskell, Python, JavaScript, and Rust.

The interpreter is build with Python 3.8 with strategie Tree Walking Interpreter.

## Install
Until now has implemented just the REPL, but you can execute a file with extension ' *.sf* ' inside of this.

For install the REPL you must clone the repositorie in your machine.

Create a virtual enviroment.
``` shell
python3 -m venv venv
```
Run the virtual enviroment

- Linux or Mac
```shell
cd sigmaF
source venv/bin/activate
```

- Windows
```shell
cd sigmaF
source /venv/Scripts/activate
```
Install requirements
```shell
pip install -r requirements.txt
```
## How use the REPL?
Inside the it you can execute code lines using:
```shell
python3.8 main.py
```
Also, you can create a script with your code and use any statement inside, for this you use:
```shell
python3.8 main.py < file.sf >
```

It should show some like it.
![Imgur](https://i.imgur.com/bZRpaEx.png)

## Tutorial SigmaF
Before averything first is it.
```SigmaF
printLn("Hello, World!")
```
This language have not variables, in its place use values for daclare must utilize `let` and give it a value, for example:
```Python
let a = 1        # Interger
let b = 1.0      # Float
let c = "string" # String
let d = true     # Boolean
let d = [1,2,3]  # List
...              # And Others
```
Sigma allows data type as Integer, Float, Boolean, and String. Also, it allows all the data types before, lists and functions.

For declare function you use the next sintaxis:
```Python
let example_function = fn <name argument>::<argument type> -> <output type> {
    => <Return Value>
}  
```
For example:
```Python
let is_prime_number = fn x::int, i::int -> bool {
    if x <= 1 then {=> false;}
    if x == i then {=> true;}
    if (x % i) == 0 then {=> false;}
    => is_prime_number(x, i+1);
}

printLn(is_prime_number(11, 2)) # Output: true
```

