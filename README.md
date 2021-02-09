# SigmaF

The SigmaF project seeks to create a new programing language in the functional paradigm inspired by languages like Haskell, Python, JavaScript, and Rust.

It is an interpreted language with its interpreter fully built using Python 3.8.

## Install

It has been implemented for the moment only REPL, but you can execute a file with extension ' *.sf* ' inside of it.

### For install the REPL you must: 

1. Clone the repositorie in your machine.

2. Create a virtual enviroment.

``` shell
python3 -m venv venv
```

3. Run the virtual enviroment

* Linux or Mac

``` shell
cd sigmaF
source venv/bin/activate
```

* Windows

``` shell
cd sigmaF
source /venv/Scripts/activate
```

4. Install requirements

``` shell
pip install -r requirements.txt
```

## How use the REPL?

Inside the it you can execute code lines using:

``` shell
python3.8 main.py
```

Also, you can create a script with your code and use any statement inside, for this you use:

``` shell
python3.8 main.py < file.sf >
```

It should show some like it.

![Imgur](https://i.imgur.com/bZRpaEx.png)

## Tutorial SigmaF

Before of all it is necessary to know this.

``` SigmaF
printLn("Hello, World!")
```
### Comments

If you want to comment on your code, you can use:
```sql

-- This is a single line comment
/*
    And this a multiline comment
*/

```

### Let Statements

This language have not variables, in its place use values for daclare must utilize `let` and give it a value, for example:

``` sql
let a = 1        -- Interger
let b = 1.0      -- Float
let c = "string" -- String
let d = true     -- Boolean
let e = [1,2,3]  -- List
...              -- And Others
```

SigmaF allows data type as Integer, Float, Boolean, and String.

### Lists 

The List allows all the data types before, lists and functions.

Also, it allows get item through the next notation:

``` sql
let value_list = [1,2,3,4,5,6,7,8,9]
value_list[0]       -- Output: 1
value_list[0, 4]    -- Output: [1,2,3,4]
value_list[0, 8, 2] -- Output: [1, 3, 5, 7]
```

> The struct of *List CAll* is example_list[\<Start>, \<End>, \<Index Jump>]

### Operators

> **Warning**: SigmaF does not allow the operation between different data type.

These are operators:
| Operator             | Symbol |
|----------------------|--------|
| Plus                 |    +   |
| Minus                |    -   |
| Multiplication       |    *   |
| Division             |    /   |
| Modulus              |    %   |
| Exponential          |   **   |
| Equal                |   ==   |
| Not Equal            |   !=   |
| Less than            |    <   |
| Greater than         |    >   |
| Less or equal than   |   <=   |
| Grater or equal than |   >=   |
| And                  |   &&   |
| Or                   |  \|\|  |
<br/>

> The operator of negation for Boolean was not included, for this, you can use the function `not()`

### Functions

For declare function you use the next sintaxis:

``` Python
let example_function = fn <Name Argument>::<Argument Type> -> <Output Type> {
    => <Return Value>
}  
```

> (The symbol `=>` mean return inside of the language)

For example:

``` sql
let is_prime_number = fn x::int, i::int -> bool {
    if x <= 1 then {=> false;}
    if x == i then {=> true;}
    if (x % i) == 0 then {=> false;}
    => is_prime_number(x, i+1);
}

printLn(is_prime_number(11, 2)) -- Output: true
```

### Conditionals

Regarding the conditionals the syntax struct is:

``` Python
if <Condition> then {
    <Consequence>
}
else{
    <Other Consequence>
}
```

For example:

``` Python
if x <= 1 || x % i == 0 then {
    false;
}
if x == i then {
    true;
}
else {
    false;
}
```
