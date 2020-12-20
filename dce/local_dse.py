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

def local_dse():
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        for bb in getblocks(func):
            while True:
                last_def = {}
                delinsts = []
                for inst in bb:

                    # Remove uses from last_def
                    for arg in inst.get('args', []):
                        if arg in last_def:
                            last_def.pop(arg)

                    if 'dest' in inst:
                        var = inst['dest']

                        # If var is in last_def, then this inst is overwriting
                        # previous inst that last defined it, so mark previous inst
                        # for deletion
                        if var in last_def:
                            delinsts.append(last_def[var])

                        # Record definition
                        last_def[var] = inst
                    
                for dinst in delinsts:
                    func['instrs'].remove(dinst)
                    bb.remove(dinst)

                if not delinsts:
                    break

    json.dump(prog, sys.stdout)
    print("\n")

local_dse()
