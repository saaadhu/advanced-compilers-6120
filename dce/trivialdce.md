# Trivial Dead Code Elimination

Remove instructions that do not have any effect on program execution

Two kinds;
Global - Works across basic blocks.
Local - Works within a basic block.

#Global

Collect a set of variables that are used by walking through all insns. Then walk through all insns a second time, marking those whose destination is not in said set. Remove marked insns.

#Local

For each insn in a basic block, clear var from set on use. Add var to set if it is dest - if var is in set, then insn of last def is dead, mark and remove.

To chain both, do

bril2json < {filename} | python ~/code/personal/advanced-compilers/dce/global_dse.py {args} | python ~/code/personal/advanced-compilers/dce/local_dse.py {args}  | bril2txt