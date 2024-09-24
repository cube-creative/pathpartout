# Path Partout
## Introduction

Path Partout is a tool for manipulating information present in folder and file paths.

It addresses two specific needs:
  * Extracting information from a file or folder path belonging to a predetermined structure.
  * Constructing a file path from a dictionary of information according to a predetermined structure.


## Functioning Logic

### Building a predetermined structure: `path_partout.conf`

To be able to extract information from a path or construct a path from information, Path Partout relies on a configuration file that indicates the association between paths and information. This file must be named `path_partout.conf` and takes the form of a YAML file.

#### Structure of the `path_partout.conf` file

The structure of a configuration file follows the form of a folder hierarchy:

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

Each field in this structure can correspond to either a `Folder` or a `Label`.

A `Folder` is conventionally enclosed in quotes and always contains other `Folder` and/or `Label` fields. `"{{project_name}}"` in the example above represents a `Folder` containing two other `Folders`: `"asset"` and `"projet"`. These `Folders` are used to represent a folder structure related to a common organization, such as the folders used within an animation project, for example.

A `Label` is conventionally named without quotes and always contains a string of characters. `pushed` in the example above is a `Label` that contains a string of characters. Note that the indentation in YAML distinguishes between the field of a sub-object and a string of characters. Labels are used to target specific locations in the folder structure. They can then be used to retrieve a path or information present in that path.

The string of characters associated with the `Label` corresponds to a file name. If we want a `Label` to target the folder that contains it, we specify an empty string.

Note that the file must always describe a folder structure starting from the root of the disk volume, designated by the letter on which the disk volume is mounted (`p` in the example above).

#### Associating paths with information

To enable the association between the folder structure and useful information, the configuration includes a system of variables that can be specified as follows: `{{my_variable}}`

Variables are strings of characters and can contain letters, numbers, and the underscore character (`_`). They conceptually describe the name of folders and files. With these variables, Path Partout can attempt to match a given path with this set of variables and associate certain parts of a folder/file name with a variable name. Conversely, variables can also be used to construct a path from variables provided in advance.

In the context of the example above, if we provide Path Partout with a path like `P:\son_teaser\asset\am\sunset001\push\sunset001_high1.blend` and indicate that it is a path associated with the `pushed` `Label`, the tool will be able to understand that here the `project_name` has the value `son_teaser`, the `asset_name` has the value `sunset001`, and the `step` has the value `high1`.

Conversely, if I tell Path Partout that my `project_name` is `pfffirates_series`, my `asset_type` is `ch`, my `asset_name` is `mosquito001`, my `step` is `modeling`, and my `working_file_extension` is `blend`. If I now ask for the path associated with my `pushed` `Label`, I will get: `P:\pfffirates_series\asset\ch\mosquito001\push\mosquito001_modeling.blend`

Note that Path Partout is case-sensitive.

#### Advanced variable names

For more complex folder or file names, it is possible to set the number of characters contained in a variable using: `{{my_variable:x}}`. `x` is a number indicating the number of characters in the variable.

It is also possible to make the presence of a variable optional using: `{{my_variable?}}`. If the variable is not provided or is not present in the given path, it will not prevent the matching between path and information.

Both making a variable optional and limiting its size are possible, like this: `{{my_variable?:x}}`


### Location of the `path_partout.conf` file

Path Partout is a tool designed to work with different folder structures. Indeed, depending on production studios or simply projects, the folder organization may not be the same.

Configuration files can therefore be multiple depending on the contexts. To identify which `path_partout.conf` file the tool should refer to when given a path, Path Partout will simply look for the file at the location of the given path and then in its parent folders. It will consider the first configuration file found in this way.

For example, if I request information from the path `P:\son_teaser\asset\am\sunset001\push\sunset001_high1.blend`, Path Partout will first look for a `path_partout.conf` file in the `P:\son_teaser\asset\am\sunset001\push\` folder. If it doesn't find it, it will look in `P:\son_teaser\asset\am\sunset001\` and so on until the `P:\` folder.

If no configuration file is found, an error is returned.

Only **one configuration file** is always considered during this process. Even if multiple configuration files are present in the parent folders, only the one in the folder furthest from the root of the disk volume will be considered.

### Configuring configuration folders

Another possibility for gathering configuration files in the same place is to define configuration folders.

To do this, simply specify the desired folders in the `PATH_PARTOUT_CONF_FOLDERS` environment variable. Example: `PATH_PARTOUT_CONF_FOLDERS = "C:/my/path/1/;C:/my/path/2/`. It is also possible to specify these paths via the Path Partout API using `pathpartout.config_folders.set_paths()`.

Path Partout will search for all files with the `.conf` extension present in the folders defined as configuration folders, as well as in their subfolders.

For Path Partout to be able to identify which configuration file to refer to when you provide it with a path, you must define a `scopes` field in the configuration files, listing the folders in which the configuration file will be active. Path Partout will always consider the file with the most specific scope compared to the path being processed.

For example, if I have a configuration file with a scope of `P:/` and another with `P:/son`, and I'm looking for information from the file `P:/son/asset/my_file.ext`, then the second configuration file with the more specific scope `P:/son` will be considered.

Note that even if configuration folders are specified, files present in the folder hierarchy will still be processed if they exist. In case of identical scopes, the file present in the hierarchy, not the one in the configuration folders, will be taken into account.

### Searching for files in configuration folders

The use of configuration folders allows you to search for files in the configuration files of your folders. 
You can give a name to your configuration files using the `name` field, and then search for the path of a configuration using the API with `pathpartout.config_folders.get_config_path_by_name()`.

You can also define search terms in your configurations, like this:

```yaml
search_term:
  "projects":
    - "son_teaser"
    - "WLC"
```

You can then retrieve the path of this configuration file using the API by doing:
`pathpartout.config_folders.search_config_path("projects", "son_teaser")`


### Linking two `path_partout.conf` files (advanced usage)

Sometimes, you may want to consider the folder structure present on multiple disk volumes in a unified way. In this case, to be able to find the configuration files from a path, it is important to have a configuration file in each disk volume. However, it is possible to link these different configuration files by adding in each file a list of paths to the other associated `path_partout.conf` files in the `linked` field at the root of the YAML documents.

If, for example, I want to link the configuration files located at `P:/path_partout.conf` and `I:/path_partout.conf`, I would have in the first file:

```yaml
"p:":
  "{{project_name}}":
    label:""
linked:
   - "i:/path_partout.conf"
```

And in the second file:

```yaml
"i:":
  "{{asset_name}}":
    label:""
linked: 
   - "p:/path_partout.conf"
```

When one of the configuration files is used, the dependent files will be automatically included. It is important that the files are always mutually associated to avoid any conflicts. Similarly, the associated files must never have labels with identical names.


### Configuring path roots per platform

In the case of a production carried out on multiple platforms (e.g., Linux, Windows, etc.), the path roots may vary on each machine depending on mount points and the operating system.

Pathpartout allows you to configure different roots via the `PATH_PARTOUT_ROOTS` environment variable. This variable should include the labels of the roots and their values as follows: `Label1=Path1&Label2=Path2`.

For example, on Windows: `PATH_PARTOUT_ROOTS: fabrication=D:&rendu=G:`

On Linux: `PATH_PARTOUT_ROOTS: fabrication=/mnt/d&rendu=/mnt/g`

Once defined, it is possible to specify the roots for the `scopes` and `trees` of the configuration file using the following syntax: `{{root:Label1}}`.
For example:

```yaml
scopes:
  - "{{root:fabrication}}"

trees:
  "{{root:fabrication}}":
    "{{project_name}}":
      "projet":
        "asset":
          "{{asset_type}}_{{asset_type_name}}":
              ...
        "episode":
          ...
  "{{root:rendu}}":
          ...
```

The roots will be interpreted when reading the configuration.



## Performance

For applications where many Pathpartout calls are made, reading times for the pathpartout configuration can be problematic. To improve performance, it is possible to enable configuration caching by setting the `PATHPARTOUT_ENABLE_CONF_CACHE` environment variable to `true` (any other value will disable the cache). **This cache will be cleared upon application restart, so a configuration change will require an application restart to take effect**.

## Use cases overview

Once the configuration file(s) are written and placed in the folder structure(s), it is relatively simple to use them via Path Partout.

### Retrieving a TreePath object

In all use cases, the first step is to retrieve a `TreePath` object that allows interaction with a folder structure based on a specific configuration file.

To obtain a `TreePath` object, there are several ways:

```python
# Retrieves a TreePath linked to the given configuration file, but without any information.
tree_path = pathpartout.tree.get_from_config("P:/path_partout.conf")
# Finds the configuration file associated with the given folder/file, but without any information.
tree_path = pathpartout.tree.get_from_path("P:/path/file.ext")
# Finds the configuration file associated with the given folder/file and retrieves the information present in the given path.
tree_path = pathpartout.tree.get_from_label("my_label", "P:/path/file.ext")
```

### Working with the data in the TreePath

Each TreePath provides different information related to the associated configuration file.

```python
# Provides a list of all variables present in the entire configuration.
tree_path.available_info # ["project_name", "asset_name", "episode_number"]
# Provides a list of all labels present in the entire configuration.
tree_path.available_label # ["asset_push_folder", "pushed"]
# Provides a dictionary of all variables in the configuration and their associated values (default is None)
tree_path.info # {"project_name": "son_teaser", "asset_name": "sunset001", "episode_number": None}
# Returns the path to the currently considered configuration file.
tree_path.config_filepath # "P:/path_partout.conf"
```

### Adding information to a TreePath

Once a TreePath is retrieved, or even partially filled through a path and a label (`get_from_label`), it is possible to assign or modify the value of variables present in the configuration:

```python
# Add/Modify the value of the project_name and asset_name variables
tree_path.info["project_name"] = "pfffirates_serie"
tree_path.info["asset_name"] = "mosquito001"

# Perform the same action
tree_path.populate_info({"project_name": "pfffirates_serie", "asset_name": "mosquito001"})
```

You can also add information to an existing TreePath using a label or an aggregate:

```python
filepath = 'P:\Pfffirates_Serie\projet\episode\e0143_surgonflette\shot\s005\p016\clean\wip\e0143_s005_p016_clean_v001.blend'
# Extracts the information from the path using the label.
tree_path.fill_with_label("shot_working_file", filepath)
# Extracts the information present in the aggregate defined in the configuration.
tree_path.fill_with_aggregate("episode_full_name", "e0143_surgonflette")
```

### Retrieving the path associated with a label

If a Treepath contains sufficient information, you can request the path of a label present in the configuration:

```python
# Returns the path associated with the label "pushed"
path = tree_path.get_label_path("pushed")
```

If the information to create the path is not sufficient, an error will be raised, specifying the missing information.

### Retrieving the value of an aggregate

In your configuration file, you can define aggregates whose value is generally a combination of several pieces of information from the configuration.

Example:

```yaml
aggregates: 
  "episode_full_name": "s{{season_number:2}}e{{episode_number:3}}_{{episode_name}}"
```

From a TreePath that already has the necessary information, you can retrieve the value of an aggregate:

```python
tree_path.get_aggregate("episode_full_name") # output: "s01e043_surgonflette"
```

## Example of specific Cube usage

### Retrieving information from the path of a shot's working file

```python
filepath = 'P:\Pfffirates_Serie\projet\episode\e0143_surgonflette\shot\s005\p016\clean\wip\e0143_s005_p016_clean_v001.blend'
tree_path = pathpartout.tree_path.get_from_label("shot_working_file", filepath)
print(tree_path.info)

Output : {'episode_name': 'surgonflette', 'task': 'clean', 'variant': 'clean', 'version_number': '001', 'asset_type_name': None, 'asset_name': None, 'season_number': '01', 'episode_number': '43', 'sequence_number': '005', 'asset_description': None, 'asset_type': None, 'extension': 'blend', 'project_name': 'Pfffirates_Serie', 'letter': 'P', 'shot_number': '016'}
```

### Retrieving the render .mov path of a shot from the working file path of a shot

```python
filepath = 'P:\Pfffirates_Serie\projet\episode\e0143_surgonflette\shot\s005\p016\clean\wip\e0143_s005_p016_clean_v001.blend'
tree_path = pathpartout.tree_path.get_from_label("shot_working_file", filepath)
if "episode_mov" in tree_path.available_labels:
    print(tree_path.get_label_path("episode_mov"))
    
Output: 'I:/Pfffirates_Serie/projet/episode/e0143_surgonflette/shot/s005/p016/clean/v001/all/e0143_s005_p016_clean.mov'
```

### Retrieving the working file path of a shot from its information on the Pfffirates project

```python
info = {'episode_name': 'surgonflette', 'task': 'clean', 'variant': 'clean', 'version_number': '001', 'season_number': '01', 'episode_number': '43', 'sequence_number': '005', 'extension': 'blend', 'project_name': 'Pfffirates_Serie', 'letter': 'P', 'shot_number': '016'}
config_path = pathpartout.config_folders.search_config_path("projects", "Pfffirates_serie")
tree_path = pathpartout.config_folders.get_from_config(config_path)
tree_path.populate_info(info)
print(tree_path.get_label_path("shot_working_file")) 
    
Output: 'P:\Pfffirates_Serie\projet\episode\e0143_surgonflette\shot\s005\p016\clean\wip\e0143_s005_p016_clean_v001.blend'
```

### Creating the working file of a shot for the next version

```python
filepath = 'P:\Pfffirates_Serie\projet\episode\e0143_surgonflette\shot\s005\p016\clean\wip\e0143_s005_p016_clean_v001.blend'
tree_path = pathpartout.tree_path.get_from_label("shot_working_file", filepath)
tree_path.info["version_number"] = "002"
print(tree_path.get_label_path("shot_working_file")) 
    
Output: 'P:\Pfffirates_Serie\projet\episode\e0143_surgonflette\shot\s005\p016\clean\wip\e0143_s005_p016_clean_v002.blend'
```

### Retrieving information from a working file, without knowing if it's a shot or an asset

The paths and labels to process a working file path for a shot and an asset are different: `shot_working_file` and `asset_working_file`.

You can test if the path matches the label:

```python
is_shot = pathpartout.tree.is_label_matching_path("shot_working_file", my_path)
print(is_shot) # true if shot path, false if asset path
```

Or you can directly ask to match the path with either of the two labels.

```python
tree = pathpartout.tree.get_from_labels(["shot_working_file", "asset_working_file"], my_path)
```

## Auto arbo

Path Partout is also capable of generating the base folder structure of a project, i.e., the main folders that are not specific to episodes or assets.

To use this feature, you need to define in the relevant `path_partout.conf` file the list of variables that are necessary to initialize the base structure. This list should be in an `auto_arbo` field at the root of the configuration.

Here is an example:

```yaml
"p:":
  "{{project_name}}":
    "projet":
      "asset":
        "{{asset_type}}_{{asset_type_name}}":
            ...
      "episode":
        ...
        
auto_arbo:
  - "project_name"
```

Here we indicate that we want a value for the `project_name` variable to initialize the structure.

Once this element is defined, you simply need to call the `auto_arbo.get_info_needed` function, specifying the path of the `path_partout.conf` file of interest (or a location covered by this configuration).

```python
from pathpartout import auto_arbo

path = "P:/path_partout.conf"
required_info = auto_arbo.get_required_info(path)
# required_info => { "project_name": None }
```

The function returns a dictionary whose fields are the information that needs to be provided. The value of each field is currently `None`.

You can then fill in the dictionary with the values you want. You can then call the `auto_arbo.generate` function, passing the configuration path and the completed info dictionary:

```python
from pathpartout import auto_arbo

path = "P:/path_partout.conf"
required_info = auto_arbo.get_required_info(path)
required_info["project_name"] = "my-new-project-name"
auto_arbo.generate(path, required_info)
```

The `auto_arbo.generate` function will generate all the folders of a new architecture. Path Partout will create as many folders as possible with the information you have provided: if it encounters a subfolder name consisting of a variable it does not know, it will not create that folder or its subfolders.
