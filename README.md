# EzyAPI

---

## Introduction

L'API (pour "Application Programming Interface" ou en français "Interface de Programmation d'Application")
 est un outil essentiel dans la réalisation de projets (à partir de projets de moyenne envergure).
Ici, l'EzyAPI est utilisée en tant que Librairie : son rôle est donc de contenir, partager et fournir
 des lignes de code, qui seront donc accessible par les différentes partitions du projet.

Cette API-ci est faite pour gérer la communication entre le Launcher, la Base de Données et les différents
 jeux auxquels les joueurs peuvent participer.
Elle va donc faire en sorte de télécharger les ressources manquantes depuis la Base de Données,
 d'ajouter ou de retirer des points aux joueurs en fonctions de leurs victoires ou leurs défaites,
 et de mettre à jour le tout dans la Base de Données.

<br>

## Informations complémentaires

__**Nom**__ : EzyAPI<br>
__**Version**__ : `v2.3`<br>
__**Version de Python**__ : Python 1.10<br>
__**Developpeur**__ : Luzog<br>
__**Dépendances**__ : [os, sys, shutil, subprocess, hashlib, mysql-connector-python]

__**Encodage**__ : `UTF-8`

<br>

## Manuel d'Utilisation

### Ce qu'il faut retenir

Aux flemmards, cette section est faite pour vous.
Voilà tout ce qu'il faut retenir pour le bon fonctionnement de l'API.
<br>

- **Au début du programme :**<br>
*On initialise la connexion avec MySQL ; on essaye de voir si on peut connecter un utilisateur ;
 on initialise les constantes de jeu `GAME_UUID` et `GAME_VERSION` ; on setup le manager.*
```py
import ezyapi.game_manager as manager
from ezyapi.UUID import UUID

GAME_UUID = UUID.parseUUID("<... uuid du jeu ...>")
GAME_VERSION = manager.GameVersion("<... version ...>")

manager.setup(GAME_UUID, GAME_VERSION)
```
*Si on veut que le jeu soit jouable meme sans passer par le Launcher, on peut directement ajouter la ligne :*
```py
manager.start_new_game()
```
<br>

- **Ensuite on peut récupérer des informations :**
```py
manager.get_user()     # Retourne le joueur (None si aucun joueur) : ezyapi.sessions.User or None
manager.linked()       # Retourne si le joueur est donné           : bool
manager.verification() # Vérifie que tout vas bien ou lève des err : None
manager.verification() # Vérifie que tout vas bien ou lève des err : None

u = manager.get_user()
u.exists()            # Le joueur existe ?       : bool
u.connected()         # Le joueur est connecté ? : bool
u.get_uuid()          # Retourne le UUID         : ezyapi.UUID.UUID
u.get_username()      # Retourne le username     : str
u.get_complete_name() # Retourne le nom          : str
u.get_lvl()           # Retourne le niveau       : int
u.get_exp()           # Retourne l'experience    : int
u.get_gp()            # Retourne les GP          : int
...
```
<br>

- **Pour enregistrer une partie et distribuer les récompenses :**
```py
if manager.linked():  # Ca nous évite des erreurs si le joueur n'est pas connecté
    manager.start_new_game()  # Uniquement si on ne l'a pas précisé avant
    manager.commit_new_set(victoire_ou_non?, exp_gagnés?, gp_gagnés?)
```
<br>

Voilà. C'est tout pr les flemmards.<br>
Les autres, (et mon futur moi quand je me relirais xD), on est partie pour une explication...<br>
<br>

### **Module** &nbsp;-&nbsp; *ezyapi.constants*

Pour commencer, c'est plutôt soft...<br>
Ce module est simplement utile pour la charte graphique (pour définir les éléments graphiques communs à tous...
 donc, couleurs, text et disposition) et pour une utilisation de couleur plus facile et *userfriendly*.<br>
Il référence pour l'instant uniquement les 27 couleurs les plus utilisées et naturelles pour et par l'ordinateur
 ainsi que les teintes *tkinter* et *hexadécimales* utilisé dans le Launcher et les autres jeux:
```py
COLOR_BG = "gray"
COLOR_BG2 = "dim gray"
COLOR_BG3 = "dark gray"

COLOR_LVL = "#00FFFF"
COLOR_EXP = "#00FF00"
COLOR_GP = "#FFFF00"
COLOR_SPECIAL = "#FF00FF"

COLOR_BLACK = "#000000"
COLOR_GRAY = "#808080"
COLOR_WHITE = "#FFFFFF"

COLOR_DARK_RED = "#800000"
COLOR_RED = "#FF0000"
COLOR_LIGHT_RED = "#FF8080"
COLOR_ORANGE = "#FF8000"
COLOR_PINK = "#FF0080"

COLOR_DARK_GREEN = "#008000"
COLOR_GREEN = "#00FF00"
COLOR_LIGHT_GREEN = "#80FF80"
COLOR_LIME = "#80FF00"
COLOR_MINT = "#00FF80"

COLOR_DARK_BLUE = "#000080"
COLOR_BLUE = "#0000FF"
COLOR_LIGHT_BLUE = "#8080FF"
COLOR_PURPLE = "#8000FF"
COLOR_AZURE = "#0080FF"

COLOR_DARK_YELLOW = "#808000"
COLOR_YELLOW = "#FFFF00"
COLOR_LIGHT_YELLOW = "#FFFF8080"

COLOR_DARK_AQUA = "#008080"
COLOR_AQUA = "#00FFFF"
COLOR_LIGHT_AQUA = "#80FFFF"

COLOR_DARK_MAGENTA = "#800080"
COLOR_MAGENTA = "#FF00FF"
COLOR_LIGHT_MAGENTA = "#FF80FF"
```
<br>

### **Module** &nbsp;-&nbsp; *ezyapi.mysql_connection*

__**Dépendances**__ : [mysql-connector-python]

Celui-ci sert à faire la connexion brute avec la Base de Données.<br>
On y trouve deux variables globales :
- **connection** : Qui est la connexion directe avec la Base de Données, qui va donc recevoir les différentes
 informations et réponses des requêtes (à None part défaut : avant l'initialisation).
- **cursor** : Qui va permettre d'envoyer des requites SQL (à None part défaut : avant l'initialisation).

Il y est également défini une classe **DatabaseConnexionError(Exception)**, raisons de praticité.<br>
Et enfin, 5 fonctions globales :
- **connexion()** : Établit une connexion avec la Base de Données et lève **DatabaseConnexionError**
 si le résultat n'est pas fructueux.
- **execute(...)** : Fait exécuter à **cursor** une requête SQL. Prend en compte un paramètre obligatoire :
 *operation: str* (qui est la requête en elle-même), et deux paramètres facultatifs.
 ([Voir la documentation](https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html))
- **commit()** : Après une requête de type `INSERT`, `UPDATE` ou encore `MODIFY`, `ALTER`, ...,
 l'exécution de cette fonction est indispensable pour valider l'action.
- **fetch(...)** : Utilisable pour récupérer le résultat d'une requête. Renvoie la réponse sous forme de *list[tuple]*.
 Prend en compte un paramètre facultatif : *size: int = None* (la taille maximale de la liste finale.
 Si == 1, alors renvoie le tuple simplement).
- **close()** : Ferme la connexion.

<br>

### **Module** &nbsp;-&nbsp; *ezyapi.UUID*

__**Dépendances**__ : [random, hashlib]

Comprend une unique classe : **UUID**
- **`__init__(...)`** : Si *raw*, 
- **@static hash(...)** : Retourne le HASH MD5 128bits en HEXCHARS (donc 32 caractères hexadécimaux).
 Args : *something* (la chose à hasher an appelant *`__str__()`*).
- **@static parseUUID(...)** : Renvoie un UUID. Alias de *UUID(...)*.
- **@static randomUUID()** : Renvoie un UUID aléatoire. Alias de *UUID()*.
- **getUUID()** : Alias de *`__str__()`*.
- **`__str__`** : Alias de *`__repr__()`*.
- **`__repr__`** : Renvoie sous la forme `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.
- **`__eq__`** : Renvoie si les deux *`__repr__()`* donne le même *str*.

<br>

### **Module** &nbsp;-&nbsp; *ezyapi.sessions*

__**Dépendances**__ : [ezyapi.mysql_connection, ezyapi.UUID]

Ce module comporte les classes en rapport avec l'utilisateur.<br>
On a d'abord deux classes héritées d' **Exception** : **UserNotFoundException(Exception)**
 *(comprend 2 args: username=None, password=None)* et **UserAlreadyExistsException(Exception)**.<br>
Et une classe **User** (Args : *connection_id: str | UUID*, *password: str = ""*) :
- Attribut **uuid** : de type *UUID* ou *str*. Contient d'id de connexion du joueur.
- Attribut **password** : de type *str*. Contient le mot de passe de connexion du joueur.
- **exists()** : Renvoie *True* si un joueur avec l'id de connexion *uuid* existe (sinon *False*).
- **connected()** : Renvoie *True* si un joueur avec l'id de connexion *uuid* et un mot de passe *password* existe
  (donc si on a un lien entre le joueur et la Base de Données) (sinon *False*).
- **reconnect(...)** : Alias de *`__init__(...)`*.
- **get_uuid()** -> *UUID or str* : Retourne *uuid*.
- **get_username()** -> *str* : Retourne le nom d'utilisateur du joueur.
- **get_completename()** -> *str or None* : Retourne le nom du joueur.
- **get_mail()** -> *str* : Retourne l'adresse mail du joueur.
- **get_password()** -> *str* : Retourne le mot de passe du joueur.
- **get_creation()** : Retourne la date de création du compte.
- **is_admin()** -> *bool* : Retourne si le compte est Administrateur.
- **is_frozen()** -> *bool* : Retourne si le compte est Freeze (si oui, il ne peut pas enregistrer de parties).
- **get_lvl()** -> *int* : Retourne le niveau du joueur.
- **get_exp()** -> *int* : Retourne l'experience du joueur.
- **get_gp()** -> *int* : Retourne les GP du joueur.
- **get_theme()** -> *int* : Retourne l'id du thème utilisé.
- **get_played_games()** -> *int* : Retourne le nombre de parties jouées par le joueur.
- **get_total_wins()** -> *int* : Retourne le nombre de parties gagnées par le joueur.

<br>

### **Module** &nbsp;-&nbsp; *ezyapi.game_manager*

__**Dépendances**__ : [os, sys, shutil, subprocess, ezyapi.UUID, ezyapi.sessions, ezyapi.mysql_connection]

Et enfin, le principal pour la fin, le GameManager.<br>
Contient 12 classes Héritées d' **Exception** :
- **GameError** : Le jeu a rencontré une erreur. Arg : *mess=None* (message à écrire).
  - **GameNotFound** : Le jeu n'existe pas. Héritée de **GameError**. Arg : *uuid=None*.
  - **VersionsNotFound** : Le jeu ne possède pas cette version. Héritée de **GameError**.
   Args : *uuid=None*, *version=None*.
  - **TooOldVersion** : Le jeu est obsolète. Héritée de **GameError**. Args : *current=None*, *expected=None*.
  - **InaccessibleGame** : Le jeu est inaccessible. Héritée de **GameError**. Arg : *uuid=None*.
- **UserError** : Le LSP (Processus de Lien de Session) a rencontré une erreur. Arg : *mess=None*.
  - **UserParameterExpected** : Les paramètres de sessions ne sont pas spécifiés. Héritée de **UserError**.
  - **NoUserLinked** : Aucun joueur n'est lié/connecté. Héritée de **UserError**.
  - **UserFrozen** : Le joueur est Freeze, il ne peut pas enregistrer de parties. Héritée de **UserError**.
- **AlreadyCommitted** : Partie déjà enregistrée.
- **FormatError** : Le format de la version est incorrect. Arg : *ver=None*.
- **ResourceNotFound** : La ressource est introuvable. Args : *id=None*, *specification=None*.

Contient également 3 autres classes :
- **GameVersion** : Nouveau système de classement des versions,
 qui permet de définir une version simple à une ressource ou une application.
 Très simple d'utilisation car elle permet de comparer plusieurs autres versions et est très intuitive.<br>
 (Explication et exemples à la fin des infos théoriques.)<br>
 Génère une GameVersion à partir de *version_to_parse* et simplifiée si *reduce_indicator*.<br>
 Args : *version_to_parse: str | int | float | list = None*, *reduce_indicator: bool = False*.<br>
 L'argument *version_to_parse* doit s'écrire avec la syntaxe `[<lettre>][<nombre>[.<nombre> ...]]`
 (où `lettre` est `a` ou `alpha` pour une version alpha, `b` ou `beta` pour bêta,
 `d` ou `delta` pour delta et `v`, `ver`, `version` ou *rien* pour une version normale
 => sachant que `a` < `b` < (`d` == `v`)).<br>
 Lève **FormatError** si le format n'est pas correct.
  - Attribut **indicator** -> *list[str or int]* : Liste dont le premier élément est une lettre,
   et dont tous les autres éléments sont des nombres entiers.
  - **@static parse_version(...)** : Alias de *GameVersion(...)* mais renvoie directement une liste si *raw*.
  - **reduce_indicator()** : Simplifie la version (transforme "v1.7.0" en "v1.7").
  - **set_precision(...)** : Modifie la précision. KWArg : *precision: int = -1*.
  ```py
  GameVersion("v1.7").set_precision(precision=5)   # Donne "v1.7.0.0"
  GameVersion("v1.7").set_precision(precision=3)   # Donne "v1.7"
  GameVersion("v1.7").set_precision(precision=2)   # Donne "v1"
  GameVersion("v1.7").set_precision(precision=-1)  # Donne "v1.7" (-1 == par défaut)
  ```
  - **set_version(...)** : Alias de *@static parse_version(...)*.
  - **get_precision()** -> *int* : Renvoie la précision de la version.
  - **get_indicator()** -> *list[str or int]* : Renvoie *indicator*.
  - **get_version(...)** -> *str* : Renvoie sous forme "zX.X.X...". Args : *precision: int = -1*,
   *reduce_version: bool = False*.
  - **compare(...)** : Compare deux GameVersion. Renvoie 1 si la version actuelle est plus récente,
   -1 si elle est plus vielle, et 0 si elles sont égales.
  - **`__str__()`** : Alias de *get_version()*.
  - **`__repr__()`** : Renvoie sous le format `<ver version='{get_version()}' indicator='{indicator}'>`.
  - **Autres Magic Methods** : `__len__`, `__contains__`, `__getitem__`, `__setitem__`, `__delitem__`,
   `__lt__`, `__le__`, `__eq__`, `__ne__`, `__ge__`.
  
  <br>__**Exemples :**__
  ```py
  GameVersion().get_version()  # Renvoie v0.0
  GameVersion("v1").get_version()  # Renvoie v1
  GameVersion("v1.").get_version()  # Renvoie v1.0
  GameVersion("b1..17").get_version()  # Renvoie b1.0.17
  
  v1 = GameVersion("alpha5.2.12")
  v1.get_version(precision=8)  # Renvoie a5.2.12.0.0.0.0
  v1.get_indicator()           # Renvoie ['a', 5, 2, 12]
  v2 = GameVersion("v1.12.2....")
  v2.get_version(reduce_version=True)  # Renvoie v1.12.2
  v2.get_indicator()                   # Renvoie ['v', 1, 12, 2, 0, 0, 0, 0]
  
  GameVersion("1.7") < GameVersion("1.16")  # Renvoie True
  GameVersion("v1.0") == GameVersion("1.0")  # Renvoie True
  GameVersion("a8.22.3") >= GameVersion("b0.0.1")  # Renvoie False car beta > alpha
  
  repr(GameVersion("a8.22.3"))  # <ver version='a8.22.3' indicator='["a", 8, 22, 3]'>
  ```

- **GameInfo** : Elle sert à contenir les informations du jeu SELON la Base de Donnée
 (donc sa version la plus récente, s'il est accessible, son créateur, sa description, etc...).<br>
 Arg : *fetched: tuple | list* (les réponses de la Base de Données à propos du jeu).<br>
 **À savoir** : tous les attributs seront égaux à None si *fetched* est *None*, ou incomplet.
  - Attribut **uuid** -> *UUID* : Identifiant.
  - Attribut **name** -> *str* : Nom.
  - Attribut **accessible** -> *bool* : Est accessible ?
  - Attribut **creation** : Date de création.
  - Attribut **creator** -> *UUID* : Créateur.
  - Attribut **exp_earnable** -> *str* : Experience gagnée.
  - Attribut **gp_earnable** -> *str* : GP gagnée.
  - Attribut **other** -> *str* : Autre(s) récompense(s).
  - Attribut **catchphrase** -> *str* : Phrase d'accroche.
  - Attribut **description** -> *str* : Description.
  - Attribut **version** -> *GameVersion* : Version la plus récente.
  - **exists()** : Le jeu existe ?
  
  <br>__**Utilisation possible :**__
  ```py
  import ezyapi.mysql_connection as connect
  import ezyapi.game_manager as manager
  
  connect.execute(f"SELECT * FROM games WHERE id='{GAME_UUID}'")
  info = manager.GameInfo(connect.fetch(1))
  
  # On peut maintenant récupérer les informations :
  if GAME_VERSION < info.version:
      # Alors le jeu est obsolète donc on le met à jour
      print("Mise à Jour du jeu", info.name, "...")
      manager.update()
      ...
  ```

- **Resource** : Permet de cibler et de manipuler un élément appartenant à la table `resources`.<br>
 Args : *n: int*, *id: str*, *name: str*, *type: str*, *bin: bytes*, *specification: str*,
 *info: str = None*, *resource_version: GameVersion = GameVersion("v1.0")*, *creator: str = None*, *creation=None*.
  - Attribut **n** -> *int* : Cible le numéro unique de ressource.
  - Attribut **id** -> *str* : Identifiant principal de ressource.
  - Attribut **name** -> *str* : Nom du fichier stocké.
  - Attribut **type** -> *str* : Extension du fichier stocké.
  - Attribut **bin** -> *bytes* : Données binaires de la ressource.
  - Attribut **specification** -> *str* : Identifie le rôle de la ressource.
  - Attribut **info** -> *str* : Informations complémentaires.
  - Attribut **resource_version** -> *GameVersion* : Version de la ressource.
  - Attribut **creator** -> *str* : Créateur de la ressource.
  - Attribut **creation** : Date de création de la ressource.
  - **save_if_doesnt_exists(...)** : Sauvegarde le fichier de ressource s'il n'existe pas.
   Args : *dir_path: str = ""*, *name: str = None*, *type: str = None*.
  - **save_by_erasing(...)** : Force la sauvegarde de la plus récente version de la ressource.
   Args : *dir_path: str = ""*, *name: str = None*, *type: str = None*.


Enfin, ce module contient 6 variables et 16 fonctions globales :<br>
**Faites attention !** Toutes les variables sont automatiquement mises-à-jour,
ne les modifiez que si vous savez ce que vous faites.
- Constante **\_\_API_VERSION** -> *GameVersion* : Explicite.
- Variable **\_\_current_version** -> *GameVersion* : Version du jeu.
- Variable **\_\_game_info** -> *GameInfo* : Explicite.
- Variable **\_\_user** -> *User* : Explicite.
- Variable **\_\_committed** -> *bool* : Explicite.
- Variable **\_\_can_be_commit** -> *bool* : Explicite.
- **linked()** -> *bool* : En rapport avec le joueur. Explicite.
- **verification()** : Avant tout commit ou tentative d'enregistrer la partie, *verification()* est indispensable pour
 voir ce qu'il ne va pas en levant les différentes erreurs si nécessaires
 (dans l'ordre : **GameNotFound**, **InaccessibleGame**, **NoUserLinked**, **UserFrozen**, **TooOldVersion**).
- **start_new_game()** : Vérifie via *verification()* et met à jour *\_\_committed*. **>> À utiliser avant de commit.**
- **client_initialization()** : Tente de faire le lien grâce aux arguments système de lancement
 et met à jour automatiquement *\_\_user*. Peut lever **UserParameterExpected** ou **UserNotFoundException**.
- **export_resource(...)** -> *int* : Exporte une ressource dans la Base de Données et renvoie *n*.
 Args : *id: str*, *name: str*, *type: str*, *bin: bytes*, *specification: str*,
 *info: str = None*, *creator: str = None*, *resource_version: GameVersion = GameVersion("v1.0")*.
- **import_resource(...)** -> *Resource* : Une des fonctions des plus utiles.
 Retourne la resource depuis la Base de Données. Peut lever **ResourceNotFound**.
 Args : *id: str | UUID*, *specification: str*.
- **import_ressources(...)** -> *list[Resource]* : Renvoie la totalité des resources avec l'id *id*.
 Arg : *id: str | UUID*.
- **updated()** -> *bool* : Renvoie si la version de jeu actuelle est la plus récente.
- **update()** : Importe la version la plus récente, supprime tous les autres fichiers, réinstalle
 toutes les ressources (pour garantir une experience au top du top) et execute la nouvelle version automatiquement.
- **import_missing_resources()** : Explicite.
- **clear_temp_files()** : Explicite.
- **get_user()** : Explicite.
- **is_committed()** : Explicite.
- **set_user(...)** : Explicite. Peut lever **UserNotFoundException**. Arg : *user: User*.
- **setup(...)** : Instore la connexion MySQL, met à jour les variables et Explicite selon args.
 Peut lever **DatabaseConnexionError**, **GameNotFound**.
 Args : *game_uuid: UUID*, *version: GameVersion*, *\_\_update: bool = True*,  *\_\_client_initialization: bool = True*,
 *\_\_clear_temp_files: bool = True*, *\_\_import_missing_resources: bool = True*.
- **commit_new_set(...)** : Effectues des vérifications et si tout vas bien, enregistre la partie,
 donne les récompenses aux joueurs, si *query*, alors execute la requête *query* et met à jour les variables.
 Peut lever **AlreadyCommitted** et toutes les erreurs de *verification()*.
 Args : *won: bool*, *exp_earned: int = 0*, *gp_earned: int = 0*, *other: str = None*, *query: str = None*.


__**À savoir**__ : Si on trouve un ".dev" dans le dossier principal, aucune mise-à-jour,
 ni aucun fichier ne sera téléchargé ou supprimé.
<br>

### Bilan / En vrac

Voilà la documentation officielle de l'EzyAPI.<br>
Si de gros changements sont effectués, alors elle sera mise à jour.

Maintenant voyons voir quelques exemples de tâches possibles à réaliser :

- **Importer une ressource spécifique** avec *id = "icon"*, *role = "image*, *si elle n'existe pas*,
 et lui donner le nom de *"Icon.PNG"* :
```py
manager.import_resource("icon", "image").save_if_doesnt_exists("rsrc/images", "Icon", "PNG")
```

- **Importer une ressource spécifique** avec *id = "icon"*, *role = "image*, *si elle n'existe pas*,
 et lui donner le nom de *"Icon.PNG"* :
```py
manager.import_resource("icon", "image").save_if_doesnt_exists("rsrc/images", "Icon", "PNG")
```

- **Faire en fonction des erreurs** :
```py
try:
    manager.setup(GAME_UUID, GAME_VERSION)
except manager.UserParameterExpected as e:
    Error("UserParameterExpected", str(e) + "\nYou must run the game from the Launcher to avoid this error.")
except mysql_connection.DatabaseConnexionError as e:
    Error("DatabaseConnexionError", str(e) + "\nThe SQL Serveur is potentially down for maintenance...\nWait and Retry Later.")
except sessions.UserNotFoundException as e:
    Error("UserNotFoundException", str(e) + "\nThe user information given does not match with any user.")
```

- **Faire une animation de Mise-à-Jour dans un menu pendant celle-ci** :
```py
manager.setup(GAME_UUID, GAME_VERSION, __update=False)

if not manager.updated():
    # ... doSomething ...
    manager.update()
    # ... end ...
```
<br>

### Conclusion

C'est tout pour aujourd'hui.<br>
Vous possédez maintenant le savoir.<br>
Je vous laisse aller voir au récapitulatif plus haut xD.

<br>
