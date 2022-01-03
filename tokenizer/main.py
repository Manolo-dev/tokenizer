"""
    Module python d'analyse syntaxique et de grammaire, tokenization
    @name: tokenizer
    @version: 1.2
    @date: 01/01/2022
    @authors: Manolo Sardo
    @functions:
        check_modules(grammar):
        if_condition(condition, value0, value1):
        do_tokenize(grammar, pos):
        tokenize(code_file, grammar_file, code_string, grammar):
    @datas:
        _code {str}[""]
        _variables {dict}[{}]
        _modules {dict}[{}]
        _trace {list}[[]]
        _LIMIT {int}[2048]
    @imports:
        yaml
        re
        sys
        tokenizer.classes
        tokenizer.error
        tokenizer.string
"""

import yaml
import re
import sys
from   tokenizer.classes import *
from   tokenizer.error   import *
from   tokenizer.string  import *

_code      = ""
_variables = {}
_modules   = {}
_trace     = []
_LIMIT     = 2048

def check_modules(grammar:dict) -> None :
    """
        Vérifie la présence d'erreur dans la grammaire donnée
        @params:
            grammar {dict} la grammaire à vérifier
        @returns:
            {None|raiseError} erreur possible
    """

    if not "variables" in grammar :
        ERROR(4, "variables")
    if not "main" in grammar :
        ERROR(4, "main")

def if_condition(condition:str, value0:str, value1:str) -> bool :
    """
        Vérifie la condition avec les valeurs données
        @params:
            condition {str} la condition (égalité, différence, longueur, etc...)
            value0 {str} première valeur
            value1 {str} seconde valeur
        @returns:
            result {bool} résultat de la vérification
    """

    if not condition in ["==", "!=", "<", ">", "<=", ">="] :
        ERROR(9, rule["if"][0], traceback = _trace)

    all_conditions = {
        "==": lambda v0, v1: v0 == v1,
        "!=": lambda v0, v1: v0 != v1,
        "<" : lambda v0, v1: len(v0) <  len(v1),
        ">" : lambda v0, v1: len(v0) >  len(v1),
        "<=": lambda v0, v1: len(v0) <= len(v1),
        ">=": lambda v0, v1: len(v0) >= len(v1),
    }

    result = all_conditions[condition](value0, value1)

    return result

def do_tokenize(grammar:dict, pos:int = 0) -> tuple :
    """
        Transforme le code en liste de token selon la grammaire.
        @params:
            grammar {dict} grammaire à utiliser pour tokenizer
            pos {int}[0] position à partir de laquelle tokenizer le code
        @returns:
            all_tokens {Logs} la liste des tokens
    """

    global _code, _variables, _modules, _trace, _LIMIT

    # liste des tokens
    all_tokens = Logs()

    # vérifie les inclusions et inclue les modules nommés
    idx = 0
    while idx < len(grammar) :
        if "include" in grammar[idx] :
            name = grammar[idx]["include"]
            # remplace la ligne "- include: x" par le modules x
            del grammar[idx]
            grammar[idx:idx] = _modules[name]
        idx += 1

    # parcourt le code
    i         = pos
    l_current = 0

    # vérifie que le curseur n'est pas au dela du code ou que la limite d'exécution n'est pas atteinte
    while i <= len(_code) and l_current < _LIMIT :
        l_current += 1
        token  = (None, None)
        for idx in range(len(grammar)) :
            # remplace les variables par leur valeurs dans la règle)
            rule = grammar[idx].copy()

            # ajoute au traçage des erreurs la ligne du module
            if "__line__" in rule :
                _trace.append(rule["__line__"])

            # définit les conditions d'exécution
            execute = False
            match   = False

            # vérifie si il y a un match dans la règle
            if "match" in rule :
                pattern = re.compile(adjust(string = rule["match"], variables = _variables), re.MULTILINE)
                match   = True

            # exécute s'il y a un match et que le match correspond
            if match and pattern.match(_code, i) :
                # crée le token
                t                = pattern.match(_code, i).group()
                token            = Token()
                # ajoute aux variables le token trouvé
                _variables = {**_variables, '_': t}

                # vérifie s'il y a une condition dans la règle
                checked = True
                if "if" in rule :
                    # vérifie si la forme de la condition est correcte
                    if type(rule["if"]) != list :
                        ERROR(8, code = _code, pos = i, traceback = _trace)
                    # vérifie si la condition est remplie
                    condition = rule["if"][0]
                    value0    = adjust(string = rule["if"][1], variables = _variables)
                    value1    = adjust(string = rule["if"][2], variables = _variables)
                    checked   = if_condition(condition, value0, value1)

                execute = match and pattern.match(_code, i) and checked

            # vérifie si la règle est exécutable
            if execute:
                i += len(t) - 1

                # imprime ce qui est demandé
                if "print" in rule :
                    printable = adjust(string = rule["print"], variables = _variables)
                    print(f"\033[92mPRINTING: '{printable}'\033[0m")
                # modifie les variables données
                if "var" in rule :
                    changed = {k:adjust(string = rule["var"][k], variables = _variables) for k in rule["var"] if k != "__line__"}
                    _variables = {**_variables, **changed}
                # *produit l'erreur demandée
                if "error" in rule :
                    ERROR(2, adjust(string = rule["error"], variables = _variables), code = _code, pos = i, traceback = _trace)
                # enregistre le token
                if "save" in rule :
                    # enregistre le token via un type
                    if type(rule["save"]) == str :
                        token.set_value(t)
                        token.set_type(adjust(string = rule["save"], variables = _variables))
                    # enregistre un token donné et un type donné
                    elif type(rule["save"]) == list :
                        token.set_value(adjust(string = rule["save"][0], variables = _variables))
                        token.set_type(adjust(string = rule["save"][1], variables = _variables))
                    all_tokens.append(token)
                # empèche l'avancement du curseur
                if "ignore" in rule :
                    i -= len(t)
                # commence un noeud
                if "begin" in rule :
                    node, j, err, ending = do_tokenize(
                        grammar = rule["begin"],
                        pos = i + 1
                    )
                    i = j - 1
                    # si la boucle ne finit pas
                    if err :
                        ERROR(3, code = _code, pos = i, traceback = _trace)
                    # ajoute la boucle à la liste de tokens
                    if len(node) > 0 :
                        all_tokens.append(node)
                    # ajoute le dernier token du noeud s'il est sauvegardé
                    if ending != None :
                        all_tokens.append(ending)
                # finit le noeud
                if "end" in rule :
                    if "save" in rule :
                        ending = all_tokens.pop()
                        return all_tokens, i + 1, False, ending
                    return all_tokens, i + 1, False, None
                break
        i += 1

    return all_tokens, len(_code) - 1, True, None

def tokenize(code_file:str = None, grammar_file:str = None, code_string:str = None, grammar:dict = None) -> list :
    """
        Script maître
        @params:
            code_file {str}[None] fichier de code à tokenizer
            grammar_file {str}[None] fichier de grammaire à utiliser pour tokenizer le code
            code {str}[None] code à tokenizer
            grammar {dict}[None] grammaire à utiliser pour tokenizer le code
        @returns:
            tokens {list} liste des tokens obtenus
    """

    global _code, _variables, _modules, _trace, _LIMIT

    # essaie d'ouvrir les fichier de code source et de grammaire
    if code_string == None :
        code_string = ""
        try :
            # ouvre le fichier de code source
            code_source = open(
                file     = code_file,
                mode     = "r",
                encoding = "utf-8"
            )

            code_string = code_source.read()
        except :
            ERROR(1, "code")

    if grammar == None :
        grammar = {}
        try :
            # ouvre le fichier de grammaire
            grammar_source = open(
                file     = grammar_file,
                mode     = "r",
                encoding = "utf-8"
            )

            # transforme le fichier de grammaire en dictionnaire exploitable par python
            grammar = yaml.load(grammar_source, Loader = SafeLineLoader)
        except :
            ERROR(1, "grammaire")

    _code = code_string

    # vérifie que le code est bien une chaîne de caractères
    if type(_code) != str :
        ERROR(0)

    # vérifie la grammaire
    check_modules(grammar = grammar)

    _variables   = grammar["variables"] # importe les variables du fichier de grammaire
    _variables   = {} if _variables == None else _variables # vérifie si il n'y a pas de variables
    _modules     = grammar # importe les modules
    _modules.pop("variables") # supprime des modules le module variables

    # appelle la fonction principale
    tokens = do_tokenize(
        grammar = grammar["main"]
    )[0]

    return tokens

if __name__ == "__main__" :
    print(tokenize(
        code_file    = "examples/parenthetization.txt",
        grammar_file = "examples/parenthetization.yaml"
    ))
