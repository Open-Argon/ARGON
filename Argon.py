import re
from typing import Tuple
import sys
import time
import math
import random

# make a function that takes in a param of any type and returns it as a number

version = "ARGON Beta 2.1.0"


def number(value):
    try:
        inted = int(value)
        floated = float(value)
        if inted == floated:
            return inted
        return floated
    except:
        return float(value)


def code_Aexec(string):
    Aexec(string, False)


def code_Aeval(string):
    return Aexec(string, True)[1]

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


def valToArgonString(value, speach = False):
    if type(value) == int or type(value) == float:
        return str(value)
    elif value == None:
        return "unknown"
    elif value == True:
        return "yes"
    elif value == False:
        return "no"
    elif type(value) == dict:
        return "{" + ", ".join(f"{valToArgonString(key, speach=True)}: {valToArgonString(value[key], speach=True)}" for key in value) + "}"
    elif type(value) in [list, tuple]:
        return "[" + ", ".join(valToArgonString(i, speach=True) for i in value) + "]"
    elif speach == True and type(value) == str:
      return f'"{value}"'
    return value

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

vars = {'log': {'type': 'init', 'py': log}, 'input': {'type': 'init', 'py': input}, 'PYeval': {'type': 'init', 'py': eval}, 'PYexec': {'type': 'init', 'py': exec}, 'abs': {'type': 'init', 'py': abs}, 'round': {'type': 'init', 'py': round}, 'length': {'type': 'init', 'py': len}, 'number': {'type': 'init', 'py': number}, 'string': {'type': 'init', 'py': str}, 'bool': {'type': 'init', 'py': bool}, 'yes': {'type': 'init', 'value': True}, 'no': {'type': 'init', 'value': False}, 'unknown': {'type': 'init', 'value': None}, 'snooze': {'type': 'init', 'py': time.sleep}, 'time': {'type': 'init', 'py': time.time}, 'exit': {'type': 'init', 'py': sys.exit}, 'boxify': {'type': 'init', 'py': boxify}, 'whole': {'type':'init', 'py': int}, 'exec': {"type": "init", "py": code_Aexec}, 'eval': {"type": "init", "py": code_Aeval}, 'range': {'type': 'init', 'py': Arange}, 'random': {'type': 'init', 'py': random.random}, 'setRandomSeed': {'type': 'init', 'py': random.seed}}

stringTextREGEX = r"( *)((((\')((\\([a-z\\\"\']))|[^\\\'])*(\'))|((\")((\\([a-z\\\"\']))|[^\\\"])*(\"))))( *)"
numberTextREGEX = r"( *)([0-9]*(\.[0-9]*)?(e[0-9]+)?)( *)"
varTextREGEX = r"( *)([a-z]|[A-Z])([a-zA-Z0-9]*)((\[.*\])*)( *)"
bracketsTextREGEX = r"( *)\(.*\)( *)"
functionTextREGEX = r"( *)(([a-z]|[A-Z])([a-zA-Z0-9]*))\(.*\)( *)"
switchTextREGEX = r"( *).+\?.+\:.+( *)"
itemsTextREGEX = r"( *)\[.*\]( *)"
remTextREGEX = fr"( *)del( +)({varTextREGEX})( *)"
cobined = fr"{stringTextREGEX}|{numberTextREGEX}|{varTextREGEX}|{functionTextREGEX}|{switchTextREGEX}|{itemsTextREGEX}"
cobinedcompiled = re.compile(cobined)
bracketsTest = re.compile(bracketsTextREGEX)
stringTest = re.compile(stringTextREGEX)
itemscompiled = re.compile(itemsTextREGEX)
remcompiled = re.compile(remTextREGEX)
functionTest = re.compile(functionTextREGEX)
switchcompiled = re.compile(switchTextREGEX)
numberTest = re.compile(numberTextREGEX)
setVarREGEX = fr"( *)(((const|var) ({varTextREGEX})(( +)=( +).+)?)|(([a-z]|[A-Z])+)(( +)=( +).+))( *)"
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


# make a function takes takes in 2 values, a mathermatical operator and 2 values and returns the result
# the mathermatical operators are +, -, *, /, %, **, //, and access boolian operators and their nots such as ==, !=, >, <, >=, <=, and in, not in
def math_exec(operator, value1, value2):
    if operator == "+":
        return value1 + value2
    elif operator == "-":
        return value1 - value2
    elif operator == "*":
        return value1 * value2
    elif operator == "/":
        return value1 / value2
    elif operator == "%":
        return value1 % value2
    elif operator == "^":
        return value1 ** value2
    elif operator == "$":
        return value1 // value2
    elif operator == "==":
        return value1 == value2
    elif operator == "!=":
        return value1 != value2
    elif operator == ">-":
        return value1 > value2
    elif operator == "<-":
        return value1 < value2
    elif operator == ">=":
        return value1 >= value2
    elif operator == "<=":
        return value1 <= value2
    elif operator == " in ":
        return value1 in value2
    elif operator == " not in ":
        return value1 not in value2
    elif operator == " or ":
        return value1 or value2
    elif operator == " and ":
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
    run(vars[subname]['f']['code'], kwargs)

# value Argon executer takes in a string and runs it through the parser
def val_Aexec(string, eval=False, vars=vars) -> Tuple[bool, any]: # returns a tuple of a bool and a value
    didprocess = False # did the string get processed
    output = None # the output of the string
    if not eval and setVar.fullmatch(string):
        stringsplit = string.split("=")
        if len(stringsplit) > 1:
            val = Aexec("=".join(stringsplit[1:]).strip(), True, vars=vars)
            if val[0]:
                value = val[1]
            else:
                raise Exception(f"Error in assignment: {val[1]}")
        else:
            value = None
        typeAndVar = re.split(r"( +)", stringsplit[0])
        varname = typeAndVar[2]
        type = typeAndVar[0]
        if varname == "" and type not in ["const", "var"]:
            varname = type
            type = "var"
        if varname in vars:
            if vars[varname]["type"] == "init":
                raise Exception(f'Variable {varname} is an initialized variable')
            elif vars[varname]["type"] == "const":
                raise Exception(f"Variable {varname} is already a constant")
        vars[varname] = {"type": type, "value": value}
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
    if (eval and cobinedcompiled.fullmatch(string)) or (not eval and cobinedevalcompiled.fullmatch(string)):
        return val_Aexec(string, eval, vars=vars)
    elif bracketsTest.fullmatch(string) and string.startswith("(") and string.endswith(")"):
        try:
          return Aexec(string[1:-1], eval, vars=vars)
        except SyntaxError:
          pass
    processes = [" and ", " or ", " not in ", " in ", "<=", ">=", "<-", ">-", "!=", "==", "-", "+", "^","*","$", '%',"/"]
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
          output = (math_exec(loopoutput[i], Aexec(''.join(loopoutput[:i]))[1],  Aexec(''.join(loopoutput[i+1:]))[1]))
          didprocess = True
          breaks = True
          break
      if breaks:
        break
    if not didprocess:
        raise SyntaxError(f"invalid syntax")
    return didprocess, output


runnerREGEX = re.compile(
    r"( *)(while( +)\(.*\)|if( +)\(.*\)|(sub)( +)([a-zA-Z]+)\((.*)\)( +))( *)\[( *)")


def run(code: list, vars=vars):
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
            Aexec(line, vars=vars)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        code = open(sys.argv[1], "r").read().split("\n")
        run(code)
    else:
        print(boxify(
            version+'\nMIT LICENCE AGREEMENT\n(https://github.com/Ugric/Argon)',  align='center'))
        while True:
                code = input(">>> ")
                if code != "":
                    output = (Aexec(code))
                    if output[0]:
                        log(output[1])
