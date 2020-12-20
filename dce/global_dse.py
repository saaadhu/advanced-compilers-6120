import json
import sys

def global_dse():
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        while True:
            # Compute uses
            uses = set()
            for inst in func['instrs']:
                if 'args' in inst:
                    for arg in inst['args']:
                        uses.add(arg)

            # Mark inst having dest without use
            delinsts = []
            for inst in func['instrs']:
                if 'dest' in inst and not inst['dest'] in uses:
                    delinsts.append(inst)

            # Delete marked insts
            for dinst in delinsts:
                func['instrs'].remove(dinst)

            if not delinsts:
                break

    json.dump(prog, sys.stdout)
    print("\n")

global_dse()
