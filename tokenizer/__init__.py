"""
    Module d'analyse syntaxique et de grammaire tokenization
    @name: tokenizer
    @version: 1.2
    @date: 01/01/2022
    @authors: Manolo Sardo
    @datas:
        name {str}["tokenizer"]
        version {float}[1.0]
        author {str}["Manolo Sardo"]
    @imports:
        yaml
        re
        sys
        Tokenizer.classes
        Tokenizer.error
        Tokenizer.string
        Tokenizer.main
"""

name    = "tokenizer"
version = 1.2
author  = "Manolo Sardo"

import yaml
import re
import sys
from   Tokenizer.classes import *
from   Tokenizer.error   import *
from   Tokenizer.string  import *
from   Tokenizer.main    import *