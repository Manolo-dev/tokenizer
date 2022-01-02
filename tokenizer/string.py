"""
    Gère les chaîne de caractères, les crée, les formate
    @functions:
        format(string, variables):
        adjust(string, variables):
        to_str(tokens, char, typp):
    @imports:
        re
        Tokenizer.error
"""

import re
from   Tokenizer.error import *

def format(string:str, variables:dict) -> str :
    """
        Formate une chaine de caractère selon la syntax {{variable}}
        @params:
            string {str} la chaine à formater
            variables {dict} les variables à insérer
        @returns:
            string {str} la chaine formatée
    """

    # vérifie si une variable de type `{{var}}` est appelée
    begin = re.search(r"\{\{", string)
    if begin != None :
        # vérifie si la syntax d'appel de variable est correcte
        end = re.search(r"\}\}", string)
        if end == None :
            ERROR(6)
        # trouve le nom de la variable
        var = string[begin.span()[0] + 2:end.span()[0]]
        # si l'élément est une variable on la remplace par sa valeur
        # ou si la variable n'existe pas on renvoie une erreur
        if var in variables :
            strlist = list(string)
            strlist[begin.span()[0]:end.span()[0] + 2] = variables[var]
            string = ''.join(strlist)
        else :
            ERROR(7, var)

    # vérifie si une autre variable est présente, si oui, on formate la chaine obtenue
    begin = re.search(r"\{\{", string)
    if begin != None :
        return format(string, variables)

    return string

def adjust(string:str, variables:dict) -> str :
    """
        Remplace les variables par leurs valeurs dans une chaine de caractère
        Crop la chaine si demandé
        @params:
            string {str} la chaine de caractère à modifier
            variables {dict} les variables à insérer
        @returns:
            string {str} la chaine de caractère après remplacement des variables par leurs valeurs
    """

    # si l'élément est une variable on la remplace par sa valeur
    # ou si la variable n'existe pas on renvoie une erreur
    if string[0] == ';' if len(string) > 0 else False :
        # regarde si la chaîne est cropé, fait attention à ne pas l'inclure dans le nom de variable
        crop_pos = string.find(':')
        if crop_pos != -1 :
            # vérifie si le crop est échappé ou non
            if string[crop_pos - 1] == "\\" if crop_pos > 0 else False :
                crop_pos = -1
        if crop_pos != -1 :
            var = string[1:crop_pos]
        else :
            var = string[1:]
        if not var in variables :
            ERROR(7, var)
        if crop_pos != -1 :
            string = variables[var] + string[crop_pos:]
        else :
            string = variables[var]

    # si l'élément contient une variable on la remplace par sa valeur
    string = format(string, variables)

    # crop la chaîne
    crop_pos = string.find(':')
    if crop_pos != -1 :
        # vérifie si le crop est échappé ou non
        if string[crop_pos - 1] == "\\" if crop_pos > 0 else False :
            crop_pos = -1
    if crop_pos != -1 :
        crop = string[crop_pos + 1:]
        crop = int(crop)
        if crop > len(string) :
            ERROR(5)
        string = string[:crop_pos][:-crop]
    return string

def to_str(tokens:list, char:bool = True, typp:bool = False) -> str :
    """
        Transforme une liste de tokens en chaîne de caractères
        Cela peut servir à trans-tokenizer un code
        @params:
            tokens {list} liste des tokens à décompiler
            char {bool}[True] si l'on veut la valeur du token
            type {bool}[False] si l'on veut le type du token
        @returns:
            tokens_string {str} code trans-tokenizé
    """

    all_tokens = []
    for i in range(len(tokens)) :
        if type(tokens[i]) == list :
            all_tokens.append(to_str(tokens[i], char, typp))
        else :
            token = ""
            if char :
                token = tokens[i][0]
            if typp :
                token += tokens[i][1]
            all_tokens.append(str(token))
    tokens_string = ''.join(all_tokens)
    return tokens_string
