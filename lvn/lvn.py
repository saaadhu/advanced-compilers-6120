import json
import sys

def terminator(inst):
    if not 'op' in inst:
        return False

    op = inst['op']
    return op == 'jmp' or op == 'br' or op == 'ret'

def getblocks(func):
    currbb = []
    for inst in func['instrs']:
        if 'op' in inst:
            currbb.append(inst)
            if  terminator(inst):
                yield currbb
                currbb = []
        else:
            if len(currbb) > 0:
                yield currbb
            currbb = [inst]
    if len(currbb) > 0:
        yield currbb

def lvn():
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        for bb in getblocks(func):

            # Rename multiple defs
            multdefs = {}
            for inst in bb:
                newargs = []
                for arg in inst.get('args', []):
                    version = multdefs.get(arg, 0)
                    if version:
                        newargs.append(arg + "_" + str(version))
                    else:
                        newargs.append(arg)
                inst['args'] = newargs
                if 'dest' in inst:
                    origdest = inst['dest']
                    version = multdefs.get(origdest, -1)
                    if version != -1:
                        inst['dest'] = origdest + "_" + str(version + 1)
                    multdefs[origdest] = version + 1


            table = {}
            var2num = {}
            canonicaldefs = {}
            count = -1
            for inst in bb:

                replaced_args = []
                for arg in inst.get('args', []):
                    if not arg in var2num:
                        # No def seen in current BB, so manufacture unique value
                        canonicaldefs[len(canonicaldefs)] = arg
                        varnum = len(canonicaldefs)-1
                        var2num[arg] = varnum
                    replaced_args.append(canonicaldefs[var2num[arg]])

                if replaced_args:
                    inst['args'] = replaced_args

                if 'dest' in inst:
                    keylist = []
                    keylist.append(inst['op'])
                    if 'value' in inst:
                        keylist.append(inst['value'])
                    
                    for arg in inst.get('args', []):
                        keylist.append(var2num[arg])

                    if inst['op'] == 'id':
                        varnum = keylist[-1]
                    else:
                        key = tuple(keylist)

                        if key in table:
                            varnum = table[key]
                            inst['op'] = 'id';
                            inst['args'] = [canonicaldefs[varnum]]
                        else:
                            canonicaldefs[len(canonicaldefs)] = inst['dest']
                            varnum = len(canonicaldefs)-1
                            table[key] = varnum

                    var2num[inst['dest']] = varnum


    json.dump(prog, sys.stdout)
    print("\n")

lvn()
