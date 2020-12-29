# Local Value Numbering

Maintain a map of values to canonical vars, and substitute identical values with canonical vars.

Can be used to

1. Dead code elimination
2. Copy propagation
3. Common Subexpression Elimination
4. Constant folding

Example

a := int const 4;
b := int const 5;
sum1 := int add a, b;
sum2 := int add a, b;
res := mul sum1, sum2;
print res;

LVN Table
|Id | Value       | Canonical Var |
| 1 |   4         |     a         |
| 2 |   5         |     b         |
| 3 | add #1, #2  |    sum1       |
| 4 | mul #3, #3  |    res        |

Transformed program

a := int const 4;
b := int const 5;
sum1 := int add a, b;
sum2 := id sum1; // This will be eliminated by DCE
res := mul sum1, sum1;
print res;
