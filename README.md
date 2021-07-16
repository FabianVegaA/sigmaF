# SigmaF

The SigmaF project seeks to create a new programming language open source in the functional paradigm inspired by languages like Haskell, Python, JavaScript, and Rust.

SigmaF is an interpreted language fully built using Python 3.8.

---
## Install via binary archive on Linux

1. Download the version that you prefer  in `release`.
2. Unzip the binary archive:
``` console
VERSION=v1.1
sudo mkdir -p /usr/local/lib/sigmaf
sudo tar -xJvf sigmaf-$VERSION.tar.xz -C /usr/local/lib/sigmaf
```
3. Set the environment variable ~/.profile:
``` console
VERSION=v1.1
export PATH=/usr/local/lib/sigmaf/sigmaf-$VERSION:$PATH
```
4. Refresh profile:
``` console
. ~/.profile
```
5. Test installation using the command showed below:
``` 
➜ sigmaf
Welcome to SigmaF, the Program Language of the future for the Functional Programming and a lot more

 
                                                .         .                                                
   d888888o.    8 8888     ,o888888o.          ,8.       ,8.                   .8.          8 8888888888   
 .`8888:' `88.  8 8888    8888     `88.       ,888.     ,888.                 .888.         8 8888         
 8.`8888.   Y8  8 8888 ,8 8888       `8.     .`8888.   .`8888.               :88888.        8 8888         
 `8.`8888.      8 8888 88 8888              ,8.`8888. ,8.`8888.             . `88888.       8 8888         
  `8.`8888.     8 8888 88 8888             ,8'8.`8888,8^8.`8888.           .8. `88888.      8 888888888888 
   `8.`8888.    8 8888 88 8888            ,8' `8.`8888' `8.`8888.         .8`8. `88888.     8 8888         
    `8.`8888.   8 8888 88 8888   8888888 ,8'   `8.`88'   `8.`8888.       .8' `8. `88888.    8 8888         
8b   `8.`8888.  8 8888 `8 8888       .8',8'     `8.`'     `8.`8888.     .8'   `8. `88888.   8 8888         
`8b.  ;8.`8888  8 8888    8888     ,88',8'       `8        `8.`8888.   .888888888. `88888.  8 8888         
 `Y8888P ,88P'  8 8888     `8888888P' ,8'         `         `8.`8888. .8'       `8. `88888. 8 8888         

----------------------------------------------------------------------------------------------------------
>> 

```
> WARNING:
> If you have problems with this installation you can modify the file `home/.bashrc` by going to the end and inserting the following:
> ```
> ## SigmaF
> VERSION=v1.1
> export PATH=/usr/local/lib/sigmaf/sigmaf-$VERSION:$PATH
> ```
## Install via Interpreter of Python

It has been implemented only in REPL for the moment, but you can execute a file with the ' *.sf* ' extension on it.

### To install the REPL you have to do the following steps: 

1. Clone the repository in your machine.

2. Create a virtual enviroment:

``` shell
python3 -m venv venv
```

3. Run the virtual enviroment:

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

4. Install requirements:

``` shell
pip install -r requirements.txt
```
---

## How to use the REPL?

You can execute the code lines inside of the REPL using:

``` shell
python3.8 main.py
```
Or
``` shell
sigmaf
```
This depends on how you have installed SigmaF.

Also, you can create a script with your code and use it inside of any statement, doing the following:

``` shell
python3.8 main.py <file.sf>

sigmaf <file.sf>
```

It should show something like this:

![Imgur](https://i.imgur.com/bZRpaEx.png)

### Options of command line (SigmaF v1.1)

1. `-ncover`: This does not allow the cover page to be displayed.
2. `-cover`: This allows the cover page to be displayed.
3. `-version`: This displays the version of SigmaF installed.

### Commands to REPL
1. `exit()`: This it allow you exit of the REPL.
2. `load()`: With this you can load a `file.sf`. For proper use of this command, you must add parameter as a valid path. (version 1.1)
3. `update()`: This command reloads the path previously loaded. (version 1.1)

---
## Tutorial SigmaF

Before starting, it is necessary to know this.

``` SigmaF
printLn("Hello, World!")
```
### Comments

If you want to comment your code, you can use:
```sql

-- This is a single line comment
/*
    And this a multiline comment
*/

```

### Let Statements

This language does not use variables. Instead of variables, you can only declare static values.

For declaring a value, you must use `let` and give it a value. For example:

``` sql
let a = 1        -- Interger
let b = 1.0      -- Float
let c = "string" -- String
let d = true     -- Boolean
let e = [1,2,3]  -- List
let f = (1,2)    -- Tuple
...             
```

SigmaF allows data type as Integer, Float, Boolean, and String.

### Lists 

The Lists allow to use all the data types before mentioned, as well as lists and functions.

Also, they allow to get an item through the next notation:

``` sql
let value_list = [1,2,3,4,5,6,7,8,9]
value_list[0]       -- Output: 1
value_list[0, 4]    -- Output: [1,2,3,4]
value_list[0, 8, 2] -- Output: [1, 3, 5, 7]
```

> The struct of **List CAll** is `example_list[<Start>, <End>, <Jump>]`

### Tuples 

The tuples are data structs of length greater than 1. Unlike lists, they allow the following operations:
``` sql
(1,2) + (3,4)      -- Output: (4,6)
(4,6,8) - (3,4,5)  -- Output: (1,2,3)
(0,1) == (0,1)     -- Output: true
(0,1) != (1,3)     -- Output: true
```
To obtain the values of a tuple, you must use the same notation of the list. But this data structure does not allow ranges like the lists (only you can get one position of a tuple).

E.g. 
``` sql
let t = (1,2,3,4,5,6)
t[1] -- Output: 2
t[5] -- Output: 6
```
And so on.

### Operators

> **Warning**: SigmaF have **Static Typing**, so it does not allow the operation between different data types.

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
| Greater or equal than |   >=   |
| And                  |   &&   |
| Or                   |  \|\|  |
<br/>

> The operator of negation for Boolean was not included. You can use the `not()` function in order to do this.

### Functions

For declaring a function, you have to use the next syntax:

``` Python
let example_function = fn <Name Argument>::<Argument Type> -> <Output Type> {
    => <Return Value>
}  
```

> (For return, you have to use the => symbol)

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

Regarding the conditionals, the syntax structure is:

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

## Some Examples
``` sql
-- Quick Sort
let qsort = fn l::list -> list {

	if (l == []) then {=> [];}
	else {
		let p = l[0];
		let xs = tail(l);
		
		let c_lesser = fn q::int -> bool {=> (q < p)}
		let c_greater = fn q::int -> bool {=> (q >= p)}

		=> qsort(filter(c_lesser, xs)) + [p] + qsort(filter(c_greater, xs));
	}
}

-- Filter
let filter = fn c::function, l::list -> list {
	if (l == []) then {=> [];} 

    => if (c(l[0])) then {[l[0]]} else {[]} +  filter(c, tail(l));
}

-- Map
let map = fn f::function, l::list -> list {
	if (l==[]) then {=> [];}
	
	=> [f(l[0])] + map(f, tail(l));
}


```

To know other examples of the implementations, you can go to [e.g.](egs)

---
## Feedback
I would really appreciatte your feedback. You can submit a new issue, or reach out me on [Twitter](https://twitter.com/fabianmativeal).
## Contribute
This is an **opensource** project, so everybody can contribute and be part of the community of [**SigmaF**](https://twitter.com/fabianmativeal/status/1385762245246922752).
