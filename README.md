# Tokenizer

Le Tokenizer est un analyseur lexicale, il permet, comme Flex and Yacc par exemple, de tokenizer du code, c'est à dire transformer du code en liste tokens. En l'occurence, contrairement à Flex and Yacc, la liste de token sera hiérarchisée et les tokens peuvent .

### Qu'est-ce que c'est quoi dis donc un token ?

Un token, litteralement, c'est un jeton... Bof bof comme définition... Repprenons. Un token c'est une chaîne de caractères qui, ensemble, ont une signification. La chaîne de caractères qui forme un jeton est appelée Lexeme.

### Et à quoi ça sert ?

La tokenization, c'est la prmière étape de la compilation ou de l'interprétation de la plupart des langages informatiques. Prenons Python par exemple, l'ordinateur ne sait absolument pas quoi faire avec le ficher qu'on lui donne, il le découpe donc pour avoir chacun des mots du code et pouvoir comprendre ce qu'on lui demande.

---

## Exemple :

Du code python comme celui ci :

```python
def hello(name) :
    print("Hello", name, "!")
```

sera convertit en YAML (ou n'importe quel autre langage de stockage de données comme JSON par exemple)

```yaml
---
- {value: 'def', type: function.declaration}
- {value: 'hello', type: name.funciton.declaration}
- {value: '(', type: punctuation.begin}
- {value: 'name', type: parameter}
- {value: ')', type: punctuation.end}
- {value: ':', type: start.node}
- - {value: 'print', type: function}
  - {value: '(', type: punctuation.begin}
  - {value: '"Hello"', type: string}
  - {value: ',', type: separator}
  - {value: 'name', type: variable}
  - {value: ',', type: separator}
  - {value: '"!"', type: string}
  - {value: ')', type: punctuation.end}
```

Ici les tokens sont hiérarchisés et typés, c'est à dire que pour chaque nœud, une nouvelle liste est créée et pour chaque token, un attribut de type lui est appliqué.

Le typage des tokens peut être utile car le tokenizateur peut, avec une grammaire, faire un fichier de coloration syntaxique si l'on indique dans le type la couleur du token.

---

## Spécifications

| technologie                  | outil              |
|:---------------------------- | ------------------:|
| Langage                      | Python             |
| Version                      | 3.10               |
| Gestionnaire des packets     | PIP                |
| Gestionnaire d'environnement | VirtualEnvironment |
| Environnement                | Windows 7/10       |
| Librairie                    | PyYaml, re         |

---

## To do list

- [x] Grammaire
- [x] Classe Token
- [x] Classe Node
- [x] Main
- [x] Gestion des erreurs
- [ ] Lecteur Yaml

# Grammaire

Oui, il faut une grammaire à l'outil de grammaire ! Grammaception !

## Corps

Le corps se compose d'au moins deux parties, `variables`, qui contient des expressions regexp, et les modules, dont `main`, seul module obligatoire.

- `variables`

- `main`

- `<modules>`

## Module

`main` est le seul module qui est appelé sans qu'on l'incluse manuellement.

Les `modules` traitent le code et s'occupe de la grosse part du travail, ils peuvent utiliser les variables définies dans le module, dans un module encore ouvert (variables locale) ou dans `variables`.

## Méthodes

- `include`, inclut un `module`.

- `match`, corresptond à un `SI token correspond FAIRE`, assigne à l'**objet courant** le token trouvé et éxécute le module donné (nommé ou non).

- `save`, assigne un type à l'**objet courant** et enregistre le token dans la liste des tokens.

- `if`, vérifie la condition donnée (liste de trois arguments, le premier l'opérateur, le second et le troisième les valeurs à tester). Exemple: `if: ['==', ;a, ;b]`

- `begin`, crée un nœud et le débute.

- `end`, ferme le nœud.

- `ignore`, ne fait pas avancer le texte.

- `var`, modifie les variables de la même manière que le module `variables`, la variable `_` représente le `token` trouvé.

- `error`, génère une erreur (équivalent au raise python)

- `print`, affiche le texte donné dans la console.

## Variables

Il y deux moyens d'utiliser les variables. Dans le cas d'une variable d'exemple appelée `var`, on peut faire :

- `;var`, seul dans l'élément.

- `{{var}}`, peut-être placé n'importe où dans l'élément.

- `str:n`, permet de supprimer n caractères à la chaîne str.

## Exemple

```yaml
variables:
  open: '\('
  close: '\)'
main:
  - match: ;open
    save: 'open'
    begin: # Ceci est un module non nommé
    - match: ;close
      save: 'close'
      end: 1
    - include: 'main'
  - match: '[^()]+' # pour éviter de prendre des parenthèses involontairement
    save: 'other'
  - match: ;close
    error: il y a une parenthèse de fermeture en trop
```

Cette grammaire fait de la parenthétisation simple, en simple, ça transforme ceci :

```
1 / (3 * (1 + 2))
```

en :

```yaml
---
- {value: '1 / ', type: 'other'}
- {value: '(', type: 'open'}
- - {value: '3 * ', type: 'other'}
  - {value: '(', type: 'open'}
  - - {value: '1 + 2', type: 'other'}
  - {value: ')', type: 'close'}
- {value: ')', type: 'close'}
```
