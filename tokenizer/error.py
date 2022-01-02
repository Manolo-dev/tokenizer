"""
    Gère les erreurs et dysfonctionnements
    @functions:
        ERROR(n, val):
    @imports:
        sys
"""

import sys

def ERROR(n:int, val:str = "", code:str = None, pos:int = None, traceback:list = None) -> None :
    """
        Gestionnaire d'erreur
        @params:
            n {int}
            val {str}[""]
            code {str}[None]
            pos {int}[None]
            traceback {list}[None]
        @returns:
            {None}
    """

    errors = [
        f"Le code donné n'est pas une string",
        f"Erreur d'ouverture du fichier de {val}",
        f"{val}",
        f"La boucle ne finit pas",
        f"Il manque le module `{val}`",
        f"On ne peut pas crop plus que la chaîne",
        f"Il faut une fin à l'appel de variable",
        f"La variable {val} n'existe pas",
        f"La condition doit être une liste",
        f"L'opérateur {val} n'existe pas",
    ]

    # commence l'erreur par une coloration rouge
    error_str = "\033[91m"

    # si il y a un traçage de l'erreur
    if traceback != None :
        # réduit la liste des appels pour ne pas inonder le terminal
        if len(traceback) > 10 :
            traceback = traceback[-10:]
        # ajoute à l'erreur tous les appels de modules
        error_str += "TRACEBACK GRAMMAR:\n" + "\n".join(map(lambda x : "    MODULE LINE: " + str(x), traceback)) + "\n"

    # si l'erreur est dans le code, donne la position de l'erreur
    if code != None and pos != None :
        # compte le nombre de lignes et de caractères avant l'erreur
        line   = 1 # pour que la première ligne s'appelle 1 et non 0
        column = pos

        # parcourt le code à la recherche de '\n'
        for i in range(len(code[:pos])) :
            char = code[i]
            if char == "\n" :
                line  += 1
                column = pos - i

        # ajoute la position de l'erreur
        error_str += f"ERROR CODE:\n    LINE: {line}, COLUMN: {column}\n"

    # ajoute le label de l'erreur à l'erreur
    error_str += "ERROR LABEL:\n    " + errors[n] + "\033[0m"

    # termine l'erreur par une neutre (blanche)
    error_str += "\033[0m"

    # affiche l'erreur
    print("\033[91m" + error_str + "\033[0m")

    # arrête le système
    sys.exit()