"""
    Gère les erreurs et dysfonctionnements
    @functions:
        ERROR(n, val):
    @imports:
        sys
"""

import sys

def ERROR(n:int, val:str = "") -> None :
    """
        Gestionnaire d'erreur
        @params:
            n {int}
            val {str}[""]
        @returns:
            {None}
    """
    error = [
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

    print("\033[91m" + error[n] + "\033[0m")
    sys.exit()