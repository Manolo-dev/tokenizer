"""
    Module d'analyse syntaxique et de grammaire tokenization
    @name: tokenizer
    @version: 1.3
    @date: 01/01/2022
    @authors: Manolo Sardo
    @datas:
        name {str}["tokenizer"]
        version {float}[1.3]
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
version = 1.3
author  = "Manolo Sardo"

import yaml
import re
import sys
from   tokenizer.classes import *
from   tokenizer.error   import *
from   tokenizer.string  import *
from   tokenizer.main    import *
