# Path Partout

## Présentation

Path Partout est un outil permettant de manipuler des informations présentes dans des chemins de dossiers et fichiers.

Il répond particulièrement à deux besoins :
    * Extraire des informations d'un chemin de fichier ou dossier appartenant à une structure pré-déterminée.
    * Construire un chemin de fichier à partir d'un dictionnaire d'informations selon une structure pré-déterminée.


## Logique de fonctionnement

### Construction d'une structure pré-déterminée : `path_partout.conf`
Pour pouvoir extraire les informations présentes dans un chemin, ou construire un chemin à partir d'informations, 
Path Partout a besoin de s'appuyer sur un fichier de configuration lui indiquant l'association à faire entre chemins 
et informations. Ce fichier doit être nommé `path_partout.conf`, et prend la forme d'un fichier au format YAML.

#### Structure du fichier `path_partout.conf`
La structure d'un fichier de configuration reprend la forme d'une arborescence de dossiers :
```yaml
"p:":
  "{{project_name}}":
    "asset":
      "{{asset_type}}":
        "{{asset_name}}":
          "push":
            asset_push_folder: ""
            pushed: "{{asset_name}}_{{step}}.{{working_file_extension}}"
          "{{step}}":
            "wip":
              asset_working_file: "{{asset_type}}_{{asset_name}}_{{step}}_v{{version_number:3}}.{{working_file_extension}}"
    "projet":
      "episode":
          "e{{season_number:2}}{{episode_number:2}}_{{episode_name}}":
            "shot_{{shot_type?:2}}":
                shot_working_file: "e{{season_number:2}}{{episode_number:2}}_s{{sequence_number:3}}_p{{shot_number:3}}_{{step}}_v{{version_number:3}}.{{working_file_extension}}"
```
Chaque champ, dans cette structure, peut correspondre soit à un `Dossier`, soit à un `Label`.

Un `Dossier` va conventionnellement être nommé entre guillemets, et contient toujours d'autres champs `Dossier`, et/ou 
`Label` à son tour. `"{{project_name}}"` désigne dans l'exemple ci-dessus un `Dossier`, contenant deux autres `Dossier`: 
`"asset"` et `"folder"`. 
Ces `Dossier` vont permettre de représenter une structure de dossiers liées à une organisation commune, comme celle 
des dossiers utilisés au sein d'un projet d'animation, par exemple.

Un `Label` va conventionnellement être nommé sans guillemet, et contient toujours une chaîne de caractères.
`pushed` est dans l'exemple ci-dessus un `Label`, il contient une chaîne de caractères. (Attention, c'est l'indentation 
en YAML qui fait la différence entre le champ d'un sous-object, et une chaîne de caractères)
Les `Label` vont être utilisés pour cibler des emplacements particuliers dans la structure de dossiers. Ils pourront ensuite 
être exploités pour récupérer un chemin, ou des informations présentes dans ce chemin.

La chaîne de caractères associée au `Label` correspond à un nom de fichier. Dans le cas où l'on souhaite qu'un `Label`
cible le dossier qui le contient, on indique une chaîne de caractères vide.

Attention, le fichier doit toujours décrire une structure de dossiers en partant de la racine du volume disque, désigné 
par la lettre sur laquelle le volume disque est monté (`p` dans l'exemple ci-dessus).

#### Association chemins / informations
Pour permettre l'association entre la structure de dossiers et des informations utiles, la configuration comprend un 
système de variables, qu'il est possible de spécifier comme ceux-ci : `{{my_variable}}`

Les variables correspondent à des chaînes de caractères et peuvent contenir des lettres et des chiffres ainsi que le 
caractère underscore (`_`). Elles permettent de décrire conceptuellement le nom des dossiers et fichiers. Grace à elles,
Path Partout pourra chercher à faire correspondre un chemin qui lui ait donnée avec ce jeu de variables, et ainsi associé
certaines parties d'un nom de dossier/fichier à un nom de variable. Inversement, les variables permettront aussi de 
construire un chemin à partir de variables que l'on fournira au préalable. 

Dans le contexte de l'exemple ci-dessus, si l'on fournit à Path Partout un chemin comme 
`P:\son_teaser\asset\am\sunset001\push\sunset001_high1.blend`, en lui indiquant qu'il s'agit d'un chemin associé au `Label`
`pushed`, l'outil sera en mesure de comprendre qu'ici le `project_name` a pour valeur `son_teaser`, l'`asset_name`
a pour valeur `sunset001` ou encore que le `step` a pour valeur `high1`.

Inversement maintenant, si j'indique à Path Partout que mon `project_name` est `pfffirates_series`, mon `asset_type`
est `ch`, mon `asset_name` est `mosquito001`, mon `step` est `modeling` et mon `working_file_extension` est `blend`. Si
je lui demande maintenant le chemin associé à mon label `pushed`, j'obtiendrai : 
`P:\pfffirates_series\asset\ch\mosquito001\push\mosquito001_modeling.blend`

A noté que l'outil Path Partout n'est pas sensible à la casse.

#### Noms de variables avancés
Pour des noms dossiers ou fichiers plus complexes, il est possible de fixer le nombre de caractères contenu dans une 
variable avec : `{{my_variable:x}}`. `x` sera un nombre indiquant le nombre de caractères de la variable.

Il est aussi possible de rendre la présence d'une variable facultative avec : `{{my_variable?}}`. Si la variable n'est
pas fourni ou n'est pas présente dans le chemin fourni, cela n’empêchera pas la correspondance entre chemin et informations.

On peut à la fois rendre une variable facultative et limitée en taille, comme ceux-ci : `{{my_variable?:x}}`


### Emplacement du fichier `path_partout.conf`
Path Partout est un outil construit pour pouvoir fonctionner avec différentes structures de dossiers. En effet, en 
fonction des studios de production, ou simplement des projets, l'organisation des dossiers n'est pas nécessairement
la même.

Les fichiers de configuration peuvent donc être multiples en fonction des contextes. Pour identifier à quel fichier
`path_partout.conf` l'outil doit se référer, lorsqu'on lui fourni un chemin, Path Partout va simplement chercher le fichier
à l'emplacement du chemin fourni, puis dans ses différents dossiers parents. Il considérera le premier fichier de 
configuration ainsi trouvé.

Par exemple, si je demande les informations présentes dans le chemin `P:\son_teaser\asset\am\sunset001\push\sunset001_high1.blend`,
Path Partout cherchera d'abord dans le dossier `P:\son_teaser\asset\am\sunset001\push\` un fichier `path_partout.conf`.
S'il ne le trouve pas, il le cherchera dans `P:\son_teaser\asset\am\sunset001\` et ainsi de suite jusqu'au dossier `P:\`.

Si aucun fichier de configuration n'est trouvé, une erreur est retournée.

Un **seul fichier** de configuration est toujours considéré lors de ce processus. Même si plusieurs fichiers de 
configuration sont présents dans les dossiers parents, seul celui dans le dossier le plus éloigné de la racine du volume disque sera considéré.

### Liaison de deux fichiers `path_partout.conf` (utilisation avancée)
Il arrive que l'on souhaite considérer de façon unifiée, la structure de dossiers présente sur plusieurs volumes disques 
en même temps.
Dans ce cas, pour permettre de retrouver les fichiers de configuration à partir d'un chemin, il est important d'avoir 
un fichier de configuration positionnés dans chaque volume disques.
Il est toutefois possible de lier ces différents fichiers de configuration en ajoutant dans chaque fichier la liste des 
chemins vers les autres fichiers `path_partout.conf` associés dans le champs `linked` à la racine des documents YAML.

Si je veux par exemple liés les fichiers de configurations présents aux emplacements `P:/path_partout.conf` et 
`I:/path_partout.conf`, j'aurai dans le premier :
```
"p:":
  "{{project_name}}":
    label:""
linked:
   - "i:/path_partout.conf"
```
Dans le second : 
```
"i:":
  "{{asset_name}}":
    label:""
linked: 
   - "p:/path_partout.conf"
```

Lorsque l'un des fichiers de configuration sera utilisé, les fichiers dépendants seront automatiquement inclues. Il est 
important que les fichiers soient toujours mutuellement associés, pour évité tout conflit. De la même façon, les fichiers
associés ne doivent jamais avoir de labels avec des noms identiques.

## Présentation de cas d'usages
Une fois le ou les fichiers de configuration rédigés et positionnés dans la ou les structures de dossiers, il est 
relativement simple de l'exploiter via Path Partout. 


### Récupérer un objet TreePath
Dans l'ensemble des cas d'usages, il s'agit d'abord de récupérer un objet de type `TreePath` permettant d'interagir
avec une structure de dossiers en fonction d'un fichier de configuration particulier.

Pour obtenir un objet `TreePath`, il existe plusieurs façons:
```python
# Récupère un TreePath lié au fichier de configuration donnée, mais sans informations.
tree_path = pathpartout.tree.get_from_config("P:/path_partout.conf")
# Retrouve le fichier de configuration associé au dossier/fichier donné, mais sans informations.
tree_path = pathpartout.tree.get_from_path("P:/path/fichier.ext")
# Retrouve le fichier de configuration associé au dossier/fichier donné, et récupère les informations présentes dans le chemin donné.
tree_path = pathpartout.tree.get_from_label("my_label", "P:/path/fichier.ext")
```

### Exploiter les données présentes dans le TreePath
Chaque TreePath fournit différentes informations liés au fichier de configuration associé.
```python
# Fournit une liste de toutes les variables présentes dans l'ensemble de la configuration.
tree_path.available_info # ["project_name", "asset_name", "episode_number"]
# Fournit une liste de tous les labels présents dans l'ensemble de la configuration.
tree_path.available_label # ["asset_push_folder", "pushed"]
# Fournit un dictionnaire de toutes les variables dans la configuration et de leur valeur associés (None par défaut)
tree_path.info # {"project_name": "son_teaser", "asset_name": "sunset001", "episode_number": None}
# Retourne le chemin vers le fichier de configuration actuellement considéré.
tree_path.config_filepath # "P:/path_partout.conf"
```

### Ajouter des informations au sein d'un TreePath
Une fois un TreePath récupéré, ou même partiellement rempli par le biais d'un chemin et d'un label (`get_from_label`), 
il est possible d'attribuer, ou de modifier la valeur des variables présentes dans la configuration:
```python
# Ajoute/Modifie la valeur de la variable project_name et asset_name
tree_path.info["project_name"] = "pfffirates_serie"
tree_path.info["asset_name"] = "mosquito001"

# Effectue la même action
tree_path.populate_info({"project_name": "pfffirates_serie", "asset_name": "mosquito001"})
```

### Récupérer le chemin associé à un label
Si un Treepath contient les informations suffisantes, on peut demander le chemin d'un label présent dans la configuration:
```python
# Retourne le chemin associé au label pushed
path = tree_path.get_label_path("pushed")
```
Si les informations pour créer le chemin ne sont pas suffisantes, une erreur sera levée, spécifiant les informations
manquantes.


## Exemple d'utilisation Cube spécifique
### Récupérer les informations présentes dans le chemin d'un fichier de travail d'un shot
```python
filepath = 'P:\Pfffirates_Serie\projet\episode\e0143_surgonflette\shot\s005\p016\clean\wip\e0143_s005_p016_clean_v001.blend'
tree_path = pathpartout.tree_path.get_from_label("shot_working_file", filepath)
print(tree_path.info)

Output : {'episode_name': 'surgonflette', 'task': 'clean', 'variant': 'clean', 'version_number': '001', 'asset_type_name': None, 'asset_name': None, 'season_number': '01', 'episode_number': '43', 'sequence_number': '005', 'asset_description': None, 'asset_type': None, 'extension': 'blend', 'project_name': 'Pfffirates_Serie', 'letter': 'P', 'shot_number': '016'}
```


### Récupérer le chemin du rendu .mov d'un shot à partir du chemin du fichier de travail d'un shot
```python
filepath = 'P:\Pfffirates_Serie\projet\episode\e0143_surgonflette\shot\s005\p016\clean\wip\e0143_s005_p016_clean_v001.blend'
tree_path = pathpartout.tree_path.get_from_label("shot_working_file", filepath)
if "episode_mov" in tree_path.available_labels:
    print(tree_path.get_label_path("episode_mov"))
    
Output: 'I:/Pfffirates_Serie/projet/episode/e0143_surgonflette/shot/s005/p016/clean/v001/all/e0143_s005_p016_clean.mov'
```

### Récupérer le chemin de travail d'un shot à partir de ses informations sur le projet Pfffirates
```python
info = {'episode_name': 'surgonflette', 'task': 'clean', 'variant': 'clean', 'version_number': '001', 'season_number': '01', 'episode_number': '43', 'sequence_number': '005', 'extension': 'blend', 'project_name': 'Pfffirates_Serie', 'letter': 'P', 'shot_number': '016'}
tree_path = pathpartout.tree_path.get_from_path("P:/Pfffirates_serie")
tree_path.populate_info(info)
print(tree_path.get_label_path("shot_working_file")) 
    
Output: 'P:\Pfffirates_Serie\projet\episode\e0143_surgonflette\shot\s005\p016\clean\wip\e0143_s005_p016_clean_v001.blend'
```

### Créer le fichier de travail d'un shot de la version suivante
```python
filepath = 'P:\Pfffirates_Serie\projet\episode\e0143_surgonflette\shot\s005\p016\clean\wip\e0143_s005_p016_clean_v001.blend'
tree_path = pathpartout.tree_path.get_from_label("shot_working_file", filepath)
tree_path.info["version_number"] = "002"
print(tree_path.get_label_path("shot_working_file")) 
    
Output: 'P:\Pfffirates_Serie\projet\episode\e0143_surgonflette\shot\s005\p016\clean\wip\e0143_s005_p016_clean_v002.blend'
```