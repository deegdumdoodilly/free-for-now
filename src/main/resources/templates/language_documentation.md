# Storyteller Script Writing

## Basics

The following describes the language for scripts in the storyteller engine.
It's a formal language that is parsed and executed on a per-line basis with lookahead 1. Newlines are grammatically significant. Whitespaces are not significant, except for delimiting tokens.
Everything is case sensitive except where otherwise specified.

## Expressions and tokens

Expressions are delimited by newlines and executed as they are read.
Tokens are delimited by parentheses/quotes and whitespaces. The expression:

``` This (is a) "series of" $tokens```

Will evaluate to four tokens: `This`, `(is a)`, `series of` and `$tokens`, and the second token is an expression contains two tokens: `is` and `a`. After tokenization, tokens are evaluated left to right.


Anything in parentheses is evaluated as its own expression and evaluated before the expression it appears in.
Anything in quotes is treated as a string data type and its contents are taken literally. Single quotes are not considered special characters in the grammar.

## Expression syntax

Every new line must either be empty or contain an expression of the following form:

```[command] [argument] <[more arguments] [more arguments] ...>```

The `[command]` must be one of the commands listed later the documentation. Each command specifies how many arguments must follow it.
The only exception is a line that contains only a string literal, which will default to the 'say' command.


Each argument must be a valid data type, or an expression in parentheses that evaluates to a valid data type. Expressions used as arguments must be enclosed with ()
When an expression is used as an argument, everything inside will be evaluated and run as though it were an actual argument. Therefore, caution is advised when using commands in an argument.


Several types of expressions in this language will short circuit when possible, which may result in unexpected behavior when using commands within arguments


This language provides a series of operators that can evaluate higher-level values when used in arguments. Examples include equality operators (=, !=, < and >) and arithmetical operators.

## Data Types

The language's data types are
- boolean (a 0 or 1)
- integers (expressed as a series of digits with or without a negative sign)
- decimals (expressed as a series of digits with a single decimal point, with or without a negative sign. The decimal need not be eded or followed by any digits)
- strings (denoted by quotes. Quotes within the string must be immediately preceded by a \ to avoid terminating the string early)
- PENDING: lists (denoted by square brackets and delimited by commas. Can contain mixed data types)

This language will always attempt to coerce a given argument to a valid data type if possible. Use explicit casting operations when this behavior is undesirable.
Possible coercions include (in order of priority):
- integers and decimals to boolean (positive values = 1, zero/negative values = 0)
- boolean to integer or decimal
- boolean to string (0 = "false", 1 = "true")
- integer or decimal to string
- integer to decimal
- decimal to integer (truncated)
- string to decimal or integer (if string's contents are entirely numeric)

## Variables

Variables are set using the 'set' command and accessed using the '$' operator, which uniquely does not require a whitespace between it and its argument.
Variables can be cleared using 'delete', otherwise they persist. Variables, like everything else, are case sensitive.
The $answer variable is written to by the user, and manually assigning values to it may result in unexpected behavior.

## Logic
Some critical logic commands are explained below:

#### `if [boolean] <[expression]>`
This command takes one argument by default, and can take an optional additional argument.
When one argument is provided and it evaluates to true, execution continues as normal. 
  If it evaluates to false, execution skips until it encounters a matching 'endif', 'elif' or 'else' command.
If two arguments are provided and the first evaluates to true, the second argument is treated as an expression. It does not need to return anything and its returned value is ignored
  If it evaluates to false, execution continues to the next line without evaluating the second argument.

#### `endif`
Terminates an 'if', 'else', or 'elif' clause

#### `else`
Terminates an 'if' clause. If the associated 'if' statement was true, skips execution until it encounters its matching 'endif'. Otherwise, executes as normal.

#### `elif`
Terminates an 'if' clause, and functions as 'if', but automatically skips to the next 'elif', 'else' or 'endif' if any previous 'if' or 'elif' in the chain evaluated to true.

## Commands 
### `say [string]`
Prints the given string from the perspective of the narrator, and pauses execution to wait for user input to continue unless the next command is 'tack'

**Returns**: the given string 

### `tack [string]`
Appends the given string to the most recently printed text, and pauses execution to wait for user input to continue unless the next command is 'tack'

Consider using this as a form of concatenation to print strings one part at a time in situations where the presence or absence of components is dependent on game logic

**Returns**: the given string 

### `log [string]`
Prints the given value to the console

**Returns**: the given value

### `button [string]`
Offers a button prompt to the player with the given option. If the next command is not also 'button' or 'customButton', pauses execution to wait for user input.
User input is assigned to the $answer variable.

**Returns**: the given string

### `customButton`
Offers a button with a text field. If the next command is not 'button', pauses execution to wait for user input.
User input is assigned to the $answer variable.
Returns an empty string

### `set [string] [value]`
Sets a given variable to a given value. The variable's name is given by the first argument, and its value is given by the second.

**Returns**: the original value of the variable

## OPERATORS
### `[value] = [value], [value] != [value], [value] > [value], [value] < [value], [value] >= [value], [value] <= [value]`
Compares for equal value, unequal value, greater value, less value, greater or equal value, and less or equal value respectively

Behaves in the following way for the given data types, and will attempt to cast to fit one of these types:
- `[decimal/integer] = [decimal/integer]`: Mathematic comparison of the given values, casting to decimal as needed.
- `[string] = [string]`: Compares exact match for = and !=, otherwise compares dictionary order. (As per the corresponding javascript operator)

**Returns**:  a boolean 1 if the comparison holds, and 0 if it doesn't.

### `len [string]`
**Returns**: the length of the string

### `search [string] [string]`
Searches the first argument for occurrences of the second argument.

**Returns**: the position of the first instance found, or -1 if none is found

### `string [integer/decimal]`
**Returns**: a string representation of the integer or decimal

### `integer [string/decimal]`
**Returns**: an integer representation of the string or decimal (truncated if necessary)

### `decimal [string/integer]`
**Returns**: a decimal representation of the string or integer

### `[integer/decimal] + [integer/decimal], [integer/decimal] - [integer/decimal], [integer/decimal] * [integer/decimal], [integer/decimal] / [integer/decimal], [integer/decimal] ^ [integer/decimal], [integer/decimal] % [integer/decimal]`

**Returns**: the sum, difference, product, quotient, power or modulus of the two terms, respectively

### `$[value]`
Looks up a variable by the given name and returns its value. Does not use a whitespace between the '$' and the variable name. The value need not be enclosed in quotation marks, but it can be if a variable name with whitespaces or other reserved characters is desired.

Additionally, the value can be an expression in parentheses which will be evaluated at runtime.

**Returns**: The value of the variable with the specified name.

### `random <[value]> <[value]>`
Generates a random number within the provided range, whose data type corresponds to the arguments' type. If one argument is specified, generates between 0 (or 0.0) and that argument. If no arguments are specified, generates a decimal between 0.0 and 1.0.

**Returns**: A randomly generated number between the first and second arguments.


## SAVED STATE
All text printed to the game's output feed is stored in a log file. The current state of all variables, the current script path, and the current script execution pointer are stored in a state file. This is what the engine uses to resume execution when a session is resumed.

If you edit the script for an ongoing session, it is highly recommended that you test the session yourself locally before publishing the changes, as you may need to adjust the execution pointer if your edits altered the number of lines in the script.