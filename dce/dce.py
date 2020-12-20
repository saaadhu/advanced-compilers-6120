import json
import sys

def delete_if_unused(func, uses):
    deletedvars = {}
    while True:
        changed = False
        for inst in func['instrs']:
            if 'dest' in inst:
                var = inst['dest']
                if var in deletedvars:
                    continue

                varusage = uses.get(var, set())
                if not varusage:
                    deletedvars[var] = inst
                    for arg in inst.get('args', []):
                        uses[arg].discard(var)
                        if not uses[arg]:
                            changed = True
        if not changed:
            break
    print deletedvars.values()

def dse():
    prog = json.load(sys.stdin)
    uses = {}
    for func in prog['functions']:
        for inst in func['instrs']:
            var = inst.get('dest', "__sideeffect__")
            if 'args' in inst:
                for arg in inst['args']:
                    uses.setdefault(arg, set()).add(var)
    delete_if_unused (func, uses)

dse()
