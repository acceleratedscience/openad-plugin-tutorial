"""
Centralized Pyparsing grammar definitions

You can also define these in the command file, but if you will repeat
grammar definitions across multiple commands, it's better to centralize them.
"""

import pyparsing as py


calculate = py.CaselessKeyword("calc") | py.CaselessKeyword("calculate")
f_or = py.CaselessKeyword("for")
fp_type = py.MatchFirst(
    [
        py.CaselessKeyword("mfp"),
        py.CaselessKeyword("rdk"),
        py.CaselessKeyword("ap"),
        py.CaselessKeyword("tt"),
        py.CaselessKeyword("fm"),
    ]
)("fp_type")
clause_update = py.Optional(py.CaselessKeyword("update"))("update")
