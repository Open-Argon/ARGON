import re
from typing import Any, Tuple
import sys
import time
import math
import random
import json
import pathlib

version = "ARGON Beta 2.2.1"

# make a function that takes in 2 params, colour and text and outputs a coloured text
def colourify(colour, text):
    if colour == None:
        return text
    elif colour == "red":
        return "\033[31m" + text + "\033[0m"
    elif colour == "green":
        return "\033[32m" + text + "\033[0m"
    elif colour == "yellow":
        return "\033[33m" + text + "\033[0m"
    elif colour == "blue":
        return "\033[34m" + text + "\033[0m"
    elif colour == "purple":
        return "\033[35m" + text + "\033[0m"
    elif colour == "cyan":
        return "\033[36m" + text + "\033[0m"
    elif colour == "white":
        return "\033[37m" + text + "\033[0m"
    elif colour == "black":
        return "\033[30m" + text + "\033[0m"
    elif colour == "grey":
        return "\033[90m" + text + "\033[0m"
    elif colour == "orange":
        return "\033[33m" + text + "\033[0m"
    elif colour == "grey":
        return "\033[90m" + text + "\033[0m"
    elif colour == "lightred":
        return "\033[91m" + text + "\033[0m"
    elif colour == "lightgreen":
        return "\033[92m" + text + "\033[0m"
    elif colour == "lightyellow":
        return "\033[93m" + text + "\033[0m"
    elif colour == "lightblue":
        return "\033[94m" + text + "\033[0m"
    elif colour == "lightpurple":
        return "\033[95m" + text + "\033[0m"

# make a function that takes in a param of any type and returns it as a number
def number(value: Any):
    try:
        inted = int(value)
        floated = float(value)
        if inted == floated:
            return inted
        return floated
    except:
        return float(value)

def Atype(value):
    return {
        int: "number",
        float: "number",
        str: "string",
        bool: "logic",
        list: "items",
        tuple: "items",
        dict: "book",
    }[type(value)]

def code_Aexec(string):
    Aexec(string, False)


def code_Aeval(string):
    return Aexec(string, True)[1]

def logSF(*args):
    newargs = []
    for i in range(len(args)):
        newargs.append(valToArgonString(args[i], speach=True, colour=False))
    print(*newargs, end='')
def logSCF(*args):
    newargs = []
    for i in range(len(args)):
        newargs.append(valToArgonString(args[i], speach=True))
    print(*newargs, end='')
def logS(*args):
    newargs = []
    for i in range(len(args)):
        newargs.append(valToArgonString(args[i], speach=True, colour=False))
    print(*newargs)
def logSC(*args):
    newargs = []
    for i in range(len(args)):
        newargs.append(valToArgonString(args[i], speach=True))
    print(*newargs)

def logF(*args):
    newargs = []
    for i in range(len(args)):
        newargs.append(valToArgonString(args[i]))
    print(*newargs, end='')

def log(*args):
    newargs = []
    for i in range(len(args)):
        newargs.append(valToArgonString(args[i]))
    print(*newargs)


def boxify(text, length=0, align="left"):
    if align not in ['left', 'right', 'center']:
        raise SyntaxError(f"invalid alignment")
    textsplit = text.split("\n")
    for i in range(len(textsplit)):
        if len(textsplit[i]) > length:
            length = len(textsplit[i])
    processed = []
    for i in range(len(textsplit)):
        processed.append('║ ' + (" "*(length-len(textsplit[i]) if align == 'right' else math.ceil((length-len(textsplit[i]))/2) if align == 'center' else 0)) +
                         textsplit[i] + (" "*(length-len(textsplit[i]) if align == 'left' else math.floor((length-len(textsplit[i]))/2) if align == 'center' else 0)) + ' ║')
    return ('╔'+((length+2)*'═')+'╗\n'+("\n".join(processed))+'\n╚'+((length+2)*'═')+'╝')


def valToArgonString(value, speach = False, colour = True):
    if type(value) == int or type(value) == float:
        return colourify('cyan' if colour else None, str(value))
    elif value == None:
        return colourify('grey' if colour else None, "unknown")
    elif value == True:
        return colourify('green' if colour else None, "yes")
    elif value == False:
        return colourify('red' if colour else None, "no")
    elif type(value) == dict:
        return "{" + ", ".join(f"{valToArgonString(key, speach=True, colour=colour)}: {valToArgonString(value[key], speach=True, colour=colour)}" for key in value) + "}"
    elif type(value) in [list, tuple]:
        return "[" + ", ".join(valToArgonString(i, speach=True, colour=colour) for i in value) + "]"
    elif speach == True and type(value) == str:
      return colourify('yellow' if colour else None, f'\'{value}\'')
    return str(value)

def Arange(start, stop=None, step=1):
    if stop == None:
        stop = start
        start = 0
    if step == 0:
        raise ValueError("step cannot be 0")
    if step > 0:
        return list(range(start, stop + 1, step))
    else:
        return list(range(start, stop - 1, step))

vars = {
    'log': {'type': 'init', 'py': log},
    'logF': {'type': 'init', 'py': logF},
    'logS': {'type': 'init', 'py': logS},
    'logSC': {'type': 'init', 'py': logSC},
    'logSF': {'type': 'init', 'py': logSF},
    'logSCF': {'type': 'init', 'py': logSCF},
    'input': {'type': 'init', 'py': input},
    'PYeval': {'type': 'init', 'py': eval},
    'PYexec': {'type': 'init', 'py': exec},
    'abs': {'type': 'init', 'py': abs},
    'round': {'type': 'init', 'py': round},
    'length': {'type': 'init', 'py': len},
    'upper': {'type': 'init', 'py': lambda x: x.upper()},
    'lower': {'type': 'init', 'py': lambda x: x.lower()},
    'append': {'type': 'init', 'py': lambda list, value: list.append(value)},
    'insert': {'type': 'init', 'py': lambda list, to, value: list.insert(to,value)},
    'number': {'type': 'init', 'py': number},
    'char': {'type': 'init', 'py': chr},
    'ord': {'type': 'init', 'py': ord},
    'numberToBinary': {'type': 'init', 'py': lambda x: bin(x)[2:]},
    'numberToHex': {'type': 'init', 'py': lambda x: hex(x)[2:]},
    'numberToOctal': {'type': 'init', 'py': lambda x: oct(x)[2:]},
    'binaryToNumber': {'type': 'init', 'py': lambda x: int(x, 2)},
    'hexToNumber': {'type': 'init', 'py': lambda x: int(x, 16)},
    'octalToNumber': {'type': 'init', 'py': lambda x: int(x, 8)},
    'string': {'type': 'init', 'py': lambda x: valToArgonString(x, colour=False)}, 
    'logic': {'type': 'init', 'py': bool},
    'yes': {'type': 'init', 'value': True},
    'no': {'type': 'init', 'value': False},
    'unknown': {'type': 'init', 'value': None},
    'snooze': {'type': 'init', 'py': time.sleep},
    'time': {'type': 'init', 'py': time.time},
    'exit': {'type': 'init', 'py': sys.exit},
    'boxify': {'type': 'init', 'py': boxify},
    'whole': {'type':'init', 'py': int},
    'book': {'type':'init', 'py': dict},
    'exec': {"type": "init", "py": code_Aexec},
    'eval': {"type": "init", "py": code_Aeval},
    'range': {'type': 'init', 'py': Arange},
    'type': {'type': 'init', 'py': Atype},
    'random': {'type': 'init', 'py': random.random},
    'setRandomSeed': {'type': 'init', 'py': random.seed},
    'join': {'type': 'init', 'py': lambda by, list: by.join(list)},
    'split': {'type': 'init', 'py': lambda by, string: string.split(by)},
    'replace': {'type': 'init', 'py': lambda from_, to, string: string.replace(from_, to)},
    'readFile':{'type': 'init', 'py': lambda filename: open(filename, 'r').read()},
    'writeFile':{'type': 'init', 'py': lambda filename, text: open(filename, 'w').write(text)},
    'appendFile':{'type': 'init', 'py': lambda filename, text: open(filename, 'a').write(text)},
    'readLines':{'type': 'init', 'py': lambda filename: open(filename, 'r').readlines()},
    'writeLines':{'type': 'init', 'py': lambda filename, lines: open(filename, 'w').writelines(lines)},
    'appendLines':{'type': 'init', 'py': lambda filename, lines: open(filename, 'a').writelines(lines)},
    'JSONparse':{'type': 'init', 'py': json.loads},
    'JSONstringify':{'type': 'init', 'py': json.dumps},
    'pi': {'type': 'init', 'value': math.pi},
    'e': {'type': 'init', 'value': math.e},
    'sin': {'type': 'init', 'py': lambda x: math.sin(math.radians(x))},
    'cos': {'type': 'init', 'py': lambda x: math.cos(math.radians(x))},
    'tan': {'type': 'init', 'py': lambda x: math.tan(math.radians(x))},
    'rsin':{'type': 'init', 'py': math.sin},
    'rcos': {'type': 'init', 'py': math.cos},
    'rtan': {'type': 'init', 'py': math.tan},
    'asin': {'type': 'init', 'py': math.asin},
    'acos': {'type': 'init', 'py': math.acos},
    'atan': {'type': 'init', 'py': math.atan},
    'atan2': {'type': 'init', 'py': math.atan2},
    'sinh': {'type': 'init', 'py': math.sinh},
    'cosh': {'type': 'init', 'py': math.cosh},
    'tanh': {'type': 'init', 'py': math.tanh},
    'asinh': {'type': 'init', 'py': math.asinh},
    'acosh': {'type': 'init', 'py': math.acosh},
    'atanh': {'type': 'init', 'py': math.atanh},
    'exp': {'type': 'init', 'py': math.exp},
    'logarithm': {'type': 'init', 'py': math.log},
    'logarithm10': {'type': 'init', 'py': math.log10},
    'logarithm2': {'type': 'init', 'py': math.log2},
    'sqrt': {'type': 'init', 'py': math.sqrt},
    'ceil': {'type': 'init', 'py': math.ceil},
    'floor': {'type': 'init', 'py': math.floor},
    'round':  {'type': 'init', 'py': round},
    'pow': {'type': 'init', 'py': math.pow},
    'hypot': {'type': 'init', 'py': math.hypot},
    'degrees': {'type': 'init', 'py': math.degrees},
    'radians': {'type': 'init', 'py': math.radians},
}

stringTextREGEX = r"( *)((((\')((\\([a-z\\\"\']))|[^\\\'])*(\'))|((\")((\\([a-z\\\"\']))|[^\\\"])*(\"))))( *)"
numberTextREGEX = r"( *)(\-)?([0-9]*(\.[0-9]*)?(e[0-9]+)?)( *)"
varNoSpace = r'([a-z]|[A-Z])([a-zA-Z0-9]*)((\[.*\])*)'
varTextREGEX = fr"( *){varNoSpace}( *)"
bookTextREGEX = r"( *)\{((( *).+( *):( *).+( *))(( *)\,( *).+( *):( *).+( *))*|)?\}( *)"
bracketsTextREGEX = r"( *)\(.*\)( *)"
commentTextREGEX = r'( *)\#(.*)( *)'
functionTextREGEX = r"( *)(([a-z]|[A-Z])([a-zA-Z0-9]*))\(.*\)( *)"
varAdd1 = fr"( *){varNoSpace}\+\+( *)"
switchTextREGEX = r"( *).+\?.+\:.+( *)"
itemsTextREGEX = r"( *)\[.*\]( *)"
remTextREGEX = fr"( *)del( +)({varTextREGEX})( *)"
appendTextREGEX = fr"( *)append( +)({varTextREGEX})( +).+( *)"
cobined = fr"{stringTextREGEX}|{numberTextREGEX}|{varTextREGEX}|{functionTextREGEX}|{switchTextREGEX}|{itemsTextREGEX}|{commentTextREGEX}|{bookTextREGEX}|{varAdd1}"
commentTest = re.compile(commentTextREGEX)
cobinedcompiled = re.compile(cobined)
bookcompiled = re.compile(bookTextREGEX)
bracketsTest = re.compile(bracketsTextREGEX)
varAdd1compiled = re.compile(varAdd1)
stringTest = re.compile(stringTextREGEX)
itemscompiled = re.compile(itemsTextREGEX)
remcompiled = re.compile(remTextREGEX)
functionTest = re.compile(functionTextREGEX)
switchcompiled = re.compile(switchTextREGEX)
numberTest = re.compile(numberTextREGEX)
setVarREGEX = fr"( *)(((const|var) ({varTextREGEX})(( +)=( +).+)?)|({varTextREGEX})(( +)=( +).+))( *)"
setVar = re.compile(
    setVarREGEX
)
cobinedevalcompiled = re.compile(fr"{cobined}|{setVarREGEX}|{remTextREGEX}")
evalcompiled = re.compile(r"( *)( *)")
varTest = re.compile(varTextREGEX)

# make a function that takes an input of a string that represents a string and convert all the \ commands to their actual character
# make is decode unicode encoding (eg '\u0041' to A)


def convert_backslash(string):
    string = string.strip()
    if string[0] == "'":
        string = string[1:-1]
    elif string[0] == '"':
        string = string[1:-1]
    string = re.sub(r"\\([a-z\"\'])",
                    lambda x: eval(f"'\\{x.group(1)}'"), string)
    string = re.sub(r"\\u([a-fA-F0-9]{4})",
                    lambda x: chr(int(x.group(1), 16)), string)
    return string

# make a function that takes in variable and outputs 2 things, the variable name and the itterable indexes
# e.g. variable: 'my2DList[1][4]' will output name: "my2DList" and indexes: [1, 4]
# to get the true value of the indexes the Aexec function
def get_var_name_and_indexes(variable):
    bracketSplit = variable.strip().split("[")
    varName = bracketSplit[0]
    indexes = []
    if len(bracketSplit) > 1:
        brackets = "["+('['.join(bracketSplit[1:]))
        process = []
        inbracket = 0
        for i in range(len(brackets)):
            char = brackets[i]
            if inbracket == 0 and char == "[":
                inbracket += 1
            elif inbracket >= 1 and char == "]":
                inbracket -= 1
                if inbracket == 0:
                    indexes.append(Aexec("".join(process), True, vars=vars)[1])
                    process = []
                else:
                    process.append(char)
            else:
                process.append(char)
    return varName, indexes
    



# make a function takes takes in 2 values, a mathermatical operator and 2 values and returns the result
# the mathermatical operators are +, -, *, /, %, **, //, and access boolian operators and their nots such as ==, !=, >, <, >=, <=, and in, not in
def math_exec(operator, value1, value2):
    if operator == "+":
        if type(value1) == str or type(value2) == str:
            return str(value1)+str(value2)
        return value1+value2
    elif operator == "-":
        output = value1-value2
        if type(output) == float:
            output = number(output)
        return output
    elif operator == "*":
        output = value1*value2
        if type(output) == float:
            output = number(output)
        return output
    elif operator == "/":
        output = value1 / value2
        if type(output) == float:
            return number(output)
        return output
    elif operator == "%":
        return value1 % value2
    elif operator == "^":
        output = value1 ** value2
        if type(output) == float:
            return number(output)
        return output
    elif operator == "$":
        return value1 // value2
    elif operator == "==":
        return value1 == value2
    elif operator == "!=":
        return value1 != value2
    elif operator == "===":
        if isinstance(value2, type(value1)):
            return value1 == value2
        return False
    elif operator == "!==":
        if isinstance(value2, type(value1)):
            return value1 != value2
        return False
    elif operator == ">-":
        return value1 > value2
    elif operator == "<-":
        return value1 < value2
    elif operator == ">=":
        return value1 >= value2
    elif operator == "<=":
        return value1 <= value2
    elif operator == "@":
        return value1 in value2
    elif operator == "!@":
        return value1 not in value2
    elif operator == "||":
        return value1 or value2
    elif operator == "&&":
        return value1 and value2
    else:
        raise SyntaxError(f"invalid syntax")


def runSub(subname, args):
    if len(vars[subname]['f']['prams']) != len(args):
        raise SyntaxError(
            f"{subname} requires {len(vars[subname]['f']['prams'])} arguments, but {len(args)} were given")
    kwargs = vars
    for i in range(len(args)):
        if vars[subname]['f']['prams'][i] in kwargs and kwargs[vars[subname]['f']['prams'][i]]['type'] == 'init':
            raise RuntimeError(
                f"{vars[subname]['f']['prams'][i]} is an initialized variable / function")
        kwargs[vars[subname]['f']['prams'][i]] = {
            'type': 'var', 'value': args[i]}
    return run(vars[subname]['f']['code'], kwargs, True)[1]

# value Argon executer takes in a string and runs it through the parser
def val_Aexec(string, eval=False, vars=vars) -> Tuple[bool, Any]: # returns a tuple of a bool and a value
    didprocess = False # did the string get processed
    output = None # the output of the string
    if commentTest.fullmatch(string) or string.strip() == "":
        pass
    elif not eval and setVar.fullmatch(string):
        string = string.strip()
        typeAndVar = re.split(r"( +)", string)
        varname = []
        varnamearray = []
        aftertype = string[5:] if string[0:5] == "const" else string[3:] if string[0:3] == "var" else string
        value = None
        type = typeAndVar[0]
        if type not in ["const", "var"]:
            varname = type
            type = "var"
        for i in range(len(aftertype)):
          char = aftertype[i]
          joined = "".join(varnamearray)
          if i == len(aftertype)-1 and varTest.fullmatch(joined):
            varnamearray.append(char)
            joined = "".join(varnamearray)
            varname = joined.strip()
            break
          elif char == "=" and varTest.fullmatch(joined):
            value = Aexec(aftertype[len(joined)+1:], eval=True,vars=vars)[1]
            varname = joined.strip()
            break
          else:
            varnamearray.append(char)
        varname, brackets = get_var_name_and_indexes(varname)
        if varname in vars:
            if vars[varname]["type"] == "init":
                raise Exception(f'Variable {varname} is an initialized variable')
            elif vars[varname]["type"] == "const" and len(brackets) == 0:
                raise Exception(f"Variable {varname} is already a constant")
        if len(brackets) == 0:
            vars[varname] = {"type": type, "value": value}
        else:
            val = vars[varname]["value"]
            for i in range(len(brackets)-1):
                val = val[brackets[i]]
            val[brackets[-1]] = value
    
    elif not eval and remcompiled.fullmatch(string):
        var = re.split(r"( +)", string)[2]
        bracketSplit = var.strip().split("[")
        varname = bracketSplit[0]
        if varname in vars:
            if vars[varname]["type"] == "init":
                raise Exception(f'Cannot delete initialized variable')
            if len(bracketSplit) > 1:
                brackets = "["+('['.join(bracketSplit[1:]))
                bracketslist = []
                process = []
                inbracket = 0
                for i in range(len(brackets)):
                    char = brackets[i]
                    if inbracket == 0 and char == "[":
                        inbracket += 1
                    elif inbracket >= 1 and char == "]":
                        inbracket -= 1
                        if inbracket == 0:
                            bracketslist.append(Aexec("".join(process), True, vars=vars)[1])
                            process = []
                        else:
                            process.append(char)
                    else:
                        process.append(char)
                
                val = vars[varname]['value']
                for i in range(len(bracketslist)-1):
                    val = val[bracketslist[i]]
                val.pop(bracketslist[-1])
            else:
                del vars[varname]
        else:
            raise Exception(f"Variable {varname} does not exist")
    elif bracketsTest.fullmatch(string):
        output = Aexec(string.strip()[1:-1], True, vars=vars)
        didprocess = True
    elif stringTest.match(string):
        didprocess = True
        output = convert_backslash(string)
    elif numberTest.fullmatch(string):
        didprocess = True
        output = number(string)
    elif varTest.fullmatch(string):
        didprocess = True
        bracketSplit = string.strip().split("[")
        var = bracketSplit[0]
        if var in vars:
            if 'f' in vars[var] or 'py' in vars[var]:
                output = f'function({var})'
            else:
                if len(bracketSplit) > 1:
                    brackets = "["+('['.join(bracketSplit[1:]))
                    bracketslist = []
                    process = []
                    inbracket = 0
                    for i in range(len(brackets)):
                        char = brackets[i]
                        if inbracket == 0 and char == "[":
                            inbracket += 1
                        elif inbracket >= 1 and char == "]":
                            inbracket -= 1
                            if inbracket == 0:
                                bracketslist.append(Aexec("".join(process), True, vars=vars)[1])
                                process = []
                            else:
                                process.append(char)
                        else:
                            process.append(char)
                    
                    output = vars[var]['value']
                    for i in range(len(bracketslist)):
                        output = output[bracketslist[i]]
                else:
                    output = vars[var]["value"]
        else:
            raise Exception(f"Variable {var} does not exist")
    elif switchcompiled.fullmatch(string):
        process = []
        switchlen = 0
        switchval = None
        breaks = False
        for i in range(len(string)):
            switchlen += 1
            if string[i] == "?":
                try:
                    switchval = Aexec("".join(process), True, vars=vars)[1]
                    breaks = True
                    break
                except SyntaxError:
                    pass
            process.append(string[i])
        if not breaks:
            raise Exception(f"invalid 'checker' value within switch statement")
        if switchval:
            process = []
            for i in range(len(string[switchlen+1:])):
                char = string[switchlen+1+i]
                if char == ":":
                    try:
                        didprocess,output = Aexec("".join(process), True, vars=vars)
                        breaks = True
                        break
                    except SyntaxError:
                        pass
                process.append(char)
            if not breaks:
                raise Exception(f"invalid 'yes' value within switch statement")
        else:
            process = []
            for i in range(len(string)):
                char = string[len(string)-i-1]
                if char == ":":
                    try:
                        didprocess,output = Aexec("".join(process), True, vars=vars)
                        break
                    except SyntaxError:
                        pass
                process.insert(0, char)
            if not breaks:
                raise Exception(f"invalid 'no' value within switch statement")
    elif functionTest.fullmatch(string):
        function = string.strip().split("(")
        funcname = function[0]
        funcpramsTEXT = "(".join(function[1:])[:-1]
        funcprams = []
        process = []
        for i in range(len(funcpramsTEXT)):
            process.append(funcpramsTEXT[i])
            if funcpramsTEXT[i] == ",":
                    try:
                      funcprams.append(Aexec("".join(process)[:-1], True, vars=vars)[1])
                      process = []
                    except SyntaxError:
                      pass
        if len(process) > 0:
            funcprams.append(Aexec("".join(process), True, vars=vars)[1])

        if funcname in vars:
            if 'f' in vars[funcname] or 'py' in vars[funcname]:
                if 'py' in vars[funcname]:
                    didprocess = True
                    output = vars[funcname]["py"](*funcprams)
                else:
                    didprocess = False
                    output = runSub(funcname, funcprams)
            else:
                raise Exception(f"Variable {funcname} is not a function")
        else:
            raise Exception(f"Function {funcname} does not exist")
    elif varAdd1compiled.fullmatch(string):
        didprocess = True
        string = string.strip()
        var = string[:-2]
        varname, brackets = get_var_name_and_indexes(var)
        if varname in vars:
            if vars[varname]["type"] == "init":
                raise Exception(f'Cannot add to initialized variable')
            if brackets:
                val = vars[varname]['value']
                for i in range(len(brackets)):
                    val = val[brackets[i]]
                val += 1
                output = val
            else:
                vars[varname]["value"] += 1
                output = vars[varname]["value"]
        else:
            raise Exception(f"Variable {varname} does not exist")
    elif bookcompiled.fullmatch(string):
        didprocess = True
        string = string.strip()[1:-1]
        output = {}
        process = []
        key = None
        iskey = False
        for i in range(len(string)):
            char = string[i]
            if iskey:
                if char == ",":
                    try:
                        output[key] = Aexec("".join(process), True, vars=vars)[1]
                        process = []
                        iskey = False
                        key = None
                    except SyntaxError:
                        pass
                else:
                    process.append(char)
            else:
                if char == ":":
                    try:
                        key = Aexec("".join(process), True, vars=vars)[1]
                        if key in output:
                            raise Exception(f'Key \'{key}\' already exists')
                        iskey = True
                        process = []
                    except SyntaxError:
                        pass
                else:
                    process.append(char)
        if iskey:
            output[key] = Aexec("".join(process), True, vars=vars)[1]
    elif itemscompiled.fullmatch(string):
        itemsText = string.strip()[1:-1]
        items = []
        process = []
        for i in range(len(itemsText)):
            process.append(itemsText[i])
            if itemsText[i] == ",":
                    try:
                      items.append(Aexec("".join(process)[:-1], True, vars=vars)[1])
                      process = []
                    except SyntaxError:
                      pass
        if len(process) > 0:
            items.append(Aexec("".join(process), True, vars=vars)[1])
        didprocess = True
        output = items
    else:
        raise SyntaxError(f"invalid syntax")
    return didprocess, output


# bodmas stands for brackets, order of operations, division, multiplication, addition, subtraction
def Aexec(string, eval=False, vars=vars) -> Tuple[bool, str]: # Aexec stands for Argon Execution
    string = string.strip()
    print(string)
    if (eval and cobinedcompiled.fullmatch(string)) or (not eval and cobinedevalcompiled.fullmatch(string)):
        return val_Aexec(string, eval, vars=vars)
    elif bracketsTest.fullmatch(string):
        print(string)
        try:
            return Aexec(string[1:-1], eval, vars=vars)
        except SyntaxError:
          pass
    processes = ["&&", "||", "!@", "@", "<=", ">=", "<-", ">-", "!=", "==", "-", "+", "^","*","$", '%',"/"]
    loopoutput = []
    process = []
    didprocess = False
    for i in range(len(string)):
      process.append(string[i])
      for x in range(len(processes)):
        joined = ''.join(process)
        if joined.endswith(processes[x]):
          removed = joined[:-len(processes[x])].strip()
          if cobinedevalcompiled.fullmatch(removed):
              loopoutput.append(removed)
              loopoutput.append(processes[x])
              process = []
          elif removed.startswith("(") and removed.endswith(")"):
              loopoutput.append(removed)
              loopoutput.append(processes[x])
              process = []
    if len(process)> 0:
      loopoutput.append("".join(process))
      process = []
    didprocess = False
    output = None
    for x in range(len(processes)):
      breaks = False
      for i in range(1,len(loopoutput),2):
        if processes[x] == loopoutput[i]:
            didprocess = True
            output = (math_exec(loopoutput[i], Aexec(''.join(loopoutput[:i]))[1],  Aexec(''.join(loopoutput[i+1:]))[1]))
            breaks = True
            break
      if breaks:
        break
    if not didprocess:
        raise SyntaxError(f"invalid syntax")
    return didprocess, output


runnerREGEX = re.compile(
    r"( *)(while( +)\(.*\)|if( +)\(.*\)|(sub)( +)([a-zA-Z]+)\((.*)\)( +))( *)\[( *)")


def run(code: list, vars=vars, isSub = False):
    Runnertype = ""
    Runnercheck = None
    inRunner = 0
    Runnercode = []
    prams = []
    subname = ""
    inElse = False
    Elsecode = []
    for line in code:
        if runnerREGEX.fullmatch(line):
            inRunner += 1
            if inRunner == 1:
                inElse = False
                Runnertype = line.strip().split(' ')[0]
                if Runnertype == 'sub':
                    subdata = "".join(line.strip().split(' ')[1:]).split('(')
                    subname = subdata[0]
                    prams = '('.join(subdata[1:]).split(')')[0].split(',')
                    for i in range(len(prams)):
                      if prams[i] == '':
                        prams.pop(i)
                else:
                    Runnercheck = ''.join(line.strip().split(' ')[1:])[
                        :-1].strip()[1:-1]
            else:
                if inElse:
                    Elsecode.append(line)
                else:
                    Runnercode.append(line)
        elif inRunner > 0:
            if re.fullmatch(r'( *)]( *)', line):
                inRunner -= 1
                if inRunner == 0:
                    if Runnertype == "while":
                        while Aexec(Runnercheck, True, vars=vars)[1]:
                            run(Runnercode, vars)
                    elif Runnertype == "if":
                        if Aexec(Runnercheck, True, vars=vars)[1]:
                            run(Runnercode, vars)
                        else:
                            run(Elsecode, vars)
                    elif Runnertype == "sub":
                        vars[subname] = {"type": "const", 'f': {
                            'prams': prams, 'code': Runnercode}}
                    Runnertype = ""
                    subname = ""
                    Runnercheck = None
                    Runnercode = []
                    prams = []
                    inElse = False
                    Elsecode = []
                else:
                    if inElse:
                        Elsecode.append(line)
                    else:
                        Runnercode.append(line)
            elif re.fullmatch(r'( *)(\] else \[)( *)', line) and Runnertype == "if" and inRunner == 1 and not inElse:
                inElse = True
            else:
                if inElse:
                    Elsecode.append(line)
                else:
                    Runnercode.append(line)
        elif line != "":
            if isSub and line.strip().startswith('return'):
              return Aexec(line.strip()[6:], vars=vars, eval=True)
            Aexec(line, vars=vars)
    return False, None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        split = pathlib.Path(filename)
        if len(split.suffix) == 0:
            filename += ".ar"
        code = open(filename, "r").read().split("\n")
        run(code)
    else:
        print(boxify(
            version+'\nMIT LICENCE AGREEMENT\n(https://github.com/Ugric/Argon)',  align='center'))
        while True:
            try:
                code = input(">>> ")
                if code != "":
                    output = (Aexec(code))
                    if output[0]:
                        log(output[1])
            except Exception as e:
              print(e)