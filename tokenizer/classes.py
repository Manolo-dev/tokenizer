"""
    Classes de token et de liste de tokens
    @classes:
        Token:
            Object Token, hérité de list pout plus de simplicité
            @bases: list
            @attributes:
            @method :
                {**list}
                __init__(self, valu, typp):
                set_value(self, valu):
                set_type(self, typp):
                __repr__(self):
                __str__(self):
        Logs:
            Object Logs, liste de tokens, hérité de list pout plus de simplicité
            @bases: list
            @attributes:
            @method :
                {**list}
                str(self, tab):
                __repr__(self):
                __str__(self):
"""

class Token(list) :
    """
        Classe Token, hérité de list pout plus de simplicité
        @bases: list
        @attributes:
        @method :
            {**list}
            __init__(self, valu, typp):
                Crée le token
                @params:
                    self {object}
                    valu {str}[None] la valeur du token
                    typp {str}[None] le type du token
                @returns:
                    self {object}
            set_value(self, valu):
                Définit la valeur du token
                @params:
                    self {object}
                    valu {str}[None] la valeur du token
                @returns:
                    self {object}
            set_type(self, typp):
                Définit le type du token
                @params:
                    self {object}
                    typp {str}[None] le type du token
                @returns:
                    self {object}
            __repr__(self): __str__
            __str__(self):
                Renvoie la chaîne de caractère associé au token
                @params:
                    self {object}
                @returns:
                    {str}
    """

    def __init__(self:object, valu:str = None, typp:str = None) -> object :
        """
            Crée le token
            @params:
                self {object}
                valu {str}[None] la valeur du token
                typp {str}[None] le type du token
            @returns:
                self {object}
        """

        self.append(valu)
        self.append(typp)

    def set_value(self:object, valu:str) -> None :
        """
            Définit la valeur du token
            @params:
                self {object}
                valu {str}[None] la valeur du token
            @returns:
                self {object}
        """

        self[0] = valu

    def set_type(self:object, typp:str) -> None :
        """
            Définit le type du token
            @params:
                self {object}
                typp {str}[None] le type du token
            @returns:
                self {object}
        """

        self[1] = typp

    def __repr__(self:object) -> str :
        """
            Renvoie la chaîne de caractère associé au token
            @params:
                self {object}
            @returns:
                {str}
        """

        return f"{{value: '{self[0]}', type: '{self[1]}'}}"

    def __str__(self:object) -> str :
        """
            Renvoie la chaîne de caractère associé au token
            @params:
                self {object}
            @returns:
                {str}
        """

        return f"{{value: '{self[0]}', type: '{self[1]}'}}"

class Logs(list) :
    """
        Classe Logs, liste de tokens, hérité de list pout plus de simplicité
        @bases: list
        @attributes:
        @method :
            {**list}
            str(self, tab):
                Renvoie la chaîne de caractère associé à la liste de tokens
                et fait de la récursivité pour les sous liste de tokens
                @params:
                    self {object}
                    tab {str}[""] tabulation courante, augmente pour chaque sous ^liste
                @returns:
                    result {str}
            __repr__(self): __str__
            __str__(self):
                Renvoie la chaîne de caractère associé à la liste de tokens
                @params:
                    self {object}
                @returns:
                    {str}
    """

    def str(self:object, tab:str = "") -> str :
        """
            Renvoie la chaîne de caractère associé à la liste de tokens
            et fait de la récursivité pour les sous liste de tokens
            @params:
                self {object}
                tab {str}[""] tabulation courante, augmente pour chaque sous ^liste
            @returns:
                result {str}
        """

        result = "- " + str(self[0]) + "\n"
        for i in self[1:] :
            if type(i) == Token :
                result += tab + "- " + str(i) + "\n"
            if type(i) == Logs :
                result += tab + "- " + i.str(tab + "  ")
        return result

    def __repr__(self:object) -> str :
        """
            Renvoie la chaîne de caractère associé à la liste de tokens
            @params:
                self {object}
            @returns:
                {str}
        """

        return "---\n" + self.str()

    def __str__(self:object) -> str :
        """
            Renvoie la chaîne de caractère associé à la liste de tokens
            @params:
                self {object}
            @returns:
                {str}
        """

        return "---\n" + self.str()