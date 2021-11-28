import re
from typing import Tuple
import sys
import time
import math

# make a function that takes in a param of any type and returns it as a number

version = "ARGON B1.0"


def number(value):
    try:
        inted = int(value)
        floated = float(value)
        if inted == floated:
            return inted
        return floated
    except:
        return float(value)


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
        processed.append('║ ' + (" "*(length-len(textsplit[i]) if align == 'right' else math.floor((length-len(textsplit[i]))/2) if align == 'center' else 0)) +
                         textsplit[i] + (" "*(length-len(textsplit[i]) if align == 'left' else math.ceil((length-len(textsplit[i]))/2) if align == 'center' else 0)) + ' ║')
    return ('╔'+((length+2)*'═')+'╗\n'+("\n".join(processed))+'\n╚'+((length+2)*'═')+'╝')


def valToArgonString(value):
    if type(value) == int or type(value) == float:
        return str(value)
    elif value == None:
        return "unknown"
    elif value == True:
        return "yes"
    elif value == False:
        return "no"
    return value


vars = {'log': {'type': 'init', 'py': log}, 'input': {'type': 'init', 'py': input}, 'PYeval': {'type': 'init', 'py': eval}, 'PYexec': {'type': 'init', 'py': exec}, 'abs': {'type': 'init', 'py': abs}, 'round': {'type': 'init', 'py': round}, 'length': {'type': 'init', 'py': len}, 'number': {'type': 'init',
                                                                                                                                                                                                                                                                                                  'py': number}, 'string': {'type': 'init', 'py': str}, 'bool': {'type': 'init', 'py': bool}, 'yes': {'type': 'init', 'value': True}, 'no': {'type': 'init', 'value': False}, 'unknown': {'type': 'init', 'value': None}, 'snooze': {'type': 'init', 'py': time.sleep}, 'time': {'type': 'init', 'py': time.time}, 'exit': {'type': 'init', 'py': sys.exit}, 'boxify': {'type': 'init', 'py': boxify}}

stringTextREGEX = r"( *)((((\')((\\([a-z]|\\|\"))|[^\\])*(\'))|((\")((\\([a-z]|\\|\"))|[^\\])*(\"))))( *)"
numberTextREGEX = r"( *)([0-9]*(\.[0-9]*)?(e[0-9]+)?)( *)"
varTextREGEX = r"( *)([a-z]|[A-Z])([a-zA-Z0-9]*)( *)"
bracketsTextREGEX = r"\(.*\)"
functionTextREGEX = r"( *)(([a-z]|[A-Z])([a-zA-Z0-9]*))\(.*\)( *)"
cobined = fr"{stringTextREGEX}|{numberTextREGEX}|{varTextREGEX}|{functionTextREGEX}|bracketsTextREGEX"
cobinedcompiled = re.compile(cobined)
bracketsTest = re.compile(bracketsTextREGEX)
stringTest = re.compile(stringTextREGEX)
functionTest = re.compile(functionTextREGEX)
numberTest = re.compile(numberTextREGEX)
setVarREGEX = fr"( *)(((const|var) ({varTextREGEX})(( *)=( *).+)?)|(([a-z]|[A-Z])+)(( *)(\+|\-|\*|\/)?=( *).+))( *)"
setVar = re.compile(
    setVarREGEX
)
cobinedevalcompiled = re.compile(fr"{cobined}|{setVar}")
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
    elif operator == "**":
        return value1 ** value2
    elif operator == "//":
        return value1 // value2
    elif operator == "==":
        return value1 == value2
    elif operator == "!=":
        return value1 != value2
    elif operator == ">":
        return value1 > value2
    elif operator == "<":
        return value1 < value2
    elif operator == ">=":
        return value1 >= value2
    elif operator == "<=":
        return value1 <= value2
    elif operator == "in":
        return value1 in value2
    elif operator == "not in":
        return value1 not in value2
    elif operator == "or":
        return value1 or value2
    elif operator == "and":
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


def code_Aexec(string):
    Aexec(string, False)


def code_Aeval(string):
    return Aexec(string, True)[1]


vars['exec'] = {"type": "init", "py": code_Aexec}
vars['eval'] = {"type": "init", "py": code_Aeval}

# value Argon executer


def val_Aexec(string, eval=False, vars=vars) -> Tuple[bool, any]:
    didprocess = False
    output = None
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
        if varname in vars and vars[varname]["type"] == "const":
            raise Exception(f"Variable {varname} is already a constant")
        vars[varname] = {"type": type, "value": value}
    elif not eval and re.fullmatch(fr"rem( +)({varTextREGEX})", string):
        varname = re.split(r"( +)", string)[2]
        if varname in vars:
            if vars[varname]["type"] == "init":
                raise Exception(f'Cannot delete initialized variable')
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
        try:
            output = int(string)
        except:
            output = float(string)
    elif varTest.fullmatch(string):
        didprocess = True
        var = string.strip()
        if var in vars:
            if 'f' in vars[var] or 'py' in vars[var]:
                output = f'function({var})'
            else:
                output = vars[var]["value"]
        else:
            raise Exception(f"Variable {var} does not exist")
    elif functionTest.fullmatch(string):
        function = string.strip().split("(")
        funcname = function[0]
        funcpramsTEXT = "(".join(function[1:])[:-1]
        funcprams = []
        process = []
        for i in range(len(funcpramsTEXT)):
            process.append(funcpramsTEXT[i])
            if cobinedcompiled.fullmatch("".join(process)[:-1]) and funcpramsTEXT[i] == ",":
                funcprams.append(
                    Aexec("".join(process)[:-1], True, vars=vars)[1])
                process = []
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
    else:
        raise SyntaxError(f"invalid syntax")
    return didprocess, output


# bodmas stands for brackets, order of operations, division, multiplication, addition, subtraction
def Aexec(string, eval=False, vars=vars) -> Tuple[bool, str]:
    string = string.strip()
    brackets = 0
    if not (string.startswith("(") and string.endswith(")")):
        return val_Aexec(string, eval, vars=vars)
    else:
        loopoutput = []
        process = []
        for i in range(len(string)):
            if string[i] == "(":
                brackets += 1
                if brackets > 1:
                    process.append(string[i])
                elif len(process) > 0:
                    loopoutput.append("".join(process).strip())
                    process = []
            elif string[i] == ")":
                brackets -= 1
                if brackets > 0:
                    process.append(string[i])
                elif brackets == 0:
                    didprocess, val = Aexec("".join(process), True, vars=vars)
                    if didprocess:
                        loopoutput.append(val)
                    else:
                        raise Exception(f"Error in brackets: {val}")
                    process = []
                elif brackets < 0:
                    raise SyntaxError(f"invalid syntax")
            elif brackets == 0:
                process.append(string[i])
            else:
                process.append(string[i])
        if brackets != 0:
            raise SyntaxError(f"invalid syntax")
        if len(process) > 0:
            loopoutput.append("".join(process).strip())
            process = []
        finaloutput = loopoutput[0]
        for i in range(0, int(len(loopoutput) / 2)):
            i = i * 2 + 2
            finaloutput = math_exec(
                loopoutput[i - 1], finaloutput, loopoutput[i])
        return True, finaloutput


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
            version+'\nMIT LICENCE (https://github.com/Ugric/Argon)',  align='center'))
        while True:
            try:
                code = input(">>> ")
                output = (Aexec(code))
                if output[0]:
                    log(output[1])
            except Exception as e:
                print(e)
