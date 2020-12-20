import json
import sys
from collections import OrderedDict

def terminator(inst):
    if not 'op' in inst:
        return False

    op = inst['op']
    return op == 'jmp' or op == 'br' or op == 'ret'

def block_map (blocks):
    out = OrderedDict()

    for block in blocks:
        if 'label' in block[0]:
            label = block[0]['label']
            block = block[1:]
        else:
            label = "b" + str(len(out))

        out[label] = block
    return out

def get_cfg (blockmap):
    out = {}
    for i, (name, block) in enumerate(blockmap.items()):
        last = block[-1]
        if terminator(last):
            out[name] = last.get('labels', [])
        else:
            if i < len(blockmap.keys()) - 1:
                out[name] = [list(blockmap.keys())[i + 1]];
            else:
                out[name] = []
    return out

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


def mycfg():
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        preds = {}
        succs = {}
        labelBlocks = {}
        blocks = list(getblocks(func))
        blockmap = block_map (blocks)
        cfg = get_cfg (blockmap)
        print (cfg)
mycfg()
