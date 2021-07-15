# SigmaF

The SigmaF project seeks to create a new programming language open source in the functional paradigm inspired by languages like Haskell, Python, JavaScript, and Rust.

It is an interpreted language fully built using Python 3.8.

---

## Install via binary archive on Linux

1. Download the version that you prefreir in `release`.
2. Unzip the binary archive.

```console
VERSION=v1.0
sudo mkdir -p /usr/local/lib/sigmaf
sudo tar -xJvf sigmaf-$VERSION.tar.xz -C /usr/local/lib/sigmaf
```

3. Set the environment variable ~/.profile, add below to the end.

```console
VERSION=v1.0
export PATH=/usr/local/lib/sigmaf/sigmaf-$VERSION:$PATH
```

4. Refresh profile

```console
. ~/.profile
```

5. Test installation using.

```
➜ sigmaf
Welcome to SigmaF, the Program Language of the future for the Programming Functional and a lot more


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
> If you have problems with this installation you can modify the file `home/.bashrc` and insert the below to the end of it.
>
> ```
> ## SigmaF
> VERSION=v1.0
> export PATH=/usr/local/lib/sigmaf/sigmaf-$VERSION:$PATH
> ```

## Install via Interpreter of Python

It has been implemented only in REPL for the moment , but you can execute a file with the ' _.sf_ ' extension inside of it.

### For install the REPL you must:

1. Clone the repository in your machine.

2. Create a virtual enviroment.

```shell
python3 -m venv venv
```

3. Run the virtual enviroment

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

4. Install requirements

```shell
pip install -r requirements.txt
```

---

## How use the REPL?

You can execute code lines inside of the REPL using:

```shell
python3.8 main.py
```

Or

```shell
sigmaf
```

This depends on how you installed SigmaF.

Also, you can create a script with your code and use it inside of any statement. For this you can use:

```shell
python3.8 main.py <file.sf>

sigmaf <file.sf>
```

It should show something like this:

![Imgur](https://i.imgur.com/bZRpaEx.png)

### Options of command line (SigmaF v1.1)

1. `-ncover`: This allows that the cover page to be not displayed.
2. `-cover`: This allows the cover page to be displayed.
3. `-version`: This display the version of SigmaF installed.

### Commands to REPL

1. `exit()`: This it allow you exit of the REPL.
2. `load()`: Whith this commands you can load a `file.sf`. For this, you must add like parameter a valid path. (version 1.1)
3. `update()`: This command reloads the path previously loaded. (version 1.1)

---

## Tutorial SigmaF

Before to start, it's necessary to know this.

```Haskell
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

This language doesn't use variables. Instead of variables, you can only declare static values.

For daclaring a value, you must use `let` and give it a value. For example:

```Haskell
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

The List allows to all the data types before, lists and functions.

Also, it allows to get an item through the next notation:

```Haskell
let value_list = [1,2,3,4,5,6,7,8,9]
value_list[0]       -- Output: 1
value_list[0, 4]    -- Output: [1,2,3,4]
value_list[0, 8, 2] -- Output: [1, 3, 5, 7]
```

> The struct of **List CAll** is `example_list[<Start>, <End>, <Jump>]`

### Tuples

The tuples are data structs of length greater than 1 that allow others operation different to lists like:

```Haskell
(1,2) + (3,4)      -- Output: (4,6)
(4,6,8) - (3,4,5)  -- Output: (1,2,3)
(0,1) == (0,1)     -- Output: true
(0,1) != (1,3)     -- Output: true
```

To obtain the values of a tuple must use the same notation of the list, but this data structure not allow ranges as the lists (only you can get one position of a tuple).

E.g.

```Haskell
let t = (1,2,3,4,5,6)
t[1] -- Output: 2
t[5] -- Output: 6
```

And so on.

### Operators

> **Warning**: SigmaF have **Static Typing**, so does not allow the operation between different data types.

These are operators:
| Operator | Symbol |
|----------------------|--------|
| Plus | + |
| Minus | - |
| Multiplication | \* |
| Division | / |
| Modulus | % |
| Exponential | \*\* |
| Equal | == |
| Not Equal | != |
| Less than | < |
| Greater than | > |
| Less or equal than | <= |
| Greater or equal than | >= |
| And | && |
| Or | \|\| |
<br/>

> The operator of negation for Boolean was not included. For this, you can use the `not()` function

### Functions

For declaring a function, you need to use the next syntax:

```Haskell
let example_function = fn <Name Argument>::<Argument Type> -> <Output Type> {
    => <Return Value>
}
```

> (For return, you must use the => symbol)

For example:

```Haskell
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

```Haskell
if <Condition> then {
    <Consequence>
}
else{
    <Other Consequence>
}
```

For example:

```Haskell
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

```Haskell
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

For know other examples of the implementations you can go to [e.g.](egs)

---

# Feedback

Feedback is very appreciated, reach out to me on [Twitter](https://twitter.com/fabianmativeal) or submit a new issue.

# Contribute

This is an **opensource** project, so everybody can contribute and be part of the community of **SigmaF**.

## Why be part of the SigmaF community?

### 1. A simple and understanble code

The source code of the interpreter is made with Python 3.8, a language easy to learn, also good practices are a priority from start this project.

### 2. A great potencial

This project has a great potential to be the next programming languages of the functional paradigm, to development the AI, and to development new metaheuristics.

### 3. Scalable development

One of the mains approaches of this project is the implementation of TDD from start and in the development of new features, what allows scalable development.

### 4. Simple and potency

One of the main worth to this programming language is build a functional language easy to learn, that at the same time, be a powerful language, capable to process great data quantities of way secure, that also allow concurrency and parallelism.

### 5. Respect for diversity

Everybody is welcome, without matter your genre, experience or nationality, anybody with enthusiasm can participate in this project, anybody from the most expert to the that is beginning to learn about programming, marketing, design, or any career.

## How start to contribute?

There is a multiply ways to contribute, since sharing this project, improving the brand of SigmaF, helping to solve the bugs or developing new features and make improves to the source code.

- **Share this project**: You can put your start in the repository, or talk about this project, or use the hashtag #SigmaF in Twitter, LinkedIn or any social network.
  
- **Improve the brand of SigmaF**: If you are a marketer, designer, or you would like help with writing, you can help to improve the brand of the project, also can contact me on Twitter like @fabianmativeal if you are interested in it.
  
- **Help to solve the bugs**: if you find one bug notify me, in issue, of this way all can improve this language.
  
- **Developing new features**: If you want development new features or make improves to the project, you can do a folk the branch `dev` (here are the ultimate develops) and work there, and later do a [`pull request`](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) to `dev` branch, of this way will be part of next update the **SigmaF**.
