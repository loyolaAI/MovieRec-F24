# Create a Virtual Environment with Python

The present gist is a hybrid between a 'go-to' **cheat sheet** and a **tutorial** when starting a new **Data Science Project**.

Its purpose is to create a **virtual environment** with Python using the '**venv**' module.

&nbsp;

---

Table of contents

- [Create a Virtual Environment with Python](#create-a-virtual-environment-with-python)
  - [System Settings](#system-settings)
    - [Microsoft Windows Operating System](#microsoft-windows-operating-system)
    - [Microsoft Visual Studio Code](#microsoft-visual-studio-code)
    - [Python](#python)
  - [Steps to creating a 'venv'](#steps-to-creating-a-venv)
    - [Create a folder for the project](#create-a-folder-for-the-project)
    - [Create a virtual environment for the project](#create-a-virtual-environment-for-the-project)
    - [Activate the new virtual environment ```venv```](#activate-the-new-virtual-environment-venv)
    - [Create 'default' folders and files](#create-default-folders-and-files)
    - [Record the dependencies for the project](#record-the-dependencies-for-the-project)
    - [Install a Python Library](#install-a-python-library)
    - [Save the new dependencies](#save-the-new-dependencies)
      - [Install dependencies from a file](#install-dependencies-from-a-file)
    - [Check dependency clashes after installing all packages](#check-dependency-clashes-after-installing-all-packages)
    - [Deactivate the virtual environment](#deactivate-the-virtual-environment)
    - [Bonus: Linting & Formatting](#bonus-linting--formatting)

---

---

## System Settings

Settings at the time of writing this gist (12<sup>th</sup> of January 2021).

### Microsoft Windows Operating System

    Edition: Windows 10 Home
    Version: 1909
    OS build: 18363.1256
    System type: 64-bits operating, x64-based processor

### Microsoft Visual Studio Code

    Version: 1.52.1 (user setup)
    Electron: 9.3.5
    Chrome: 83.0.4103.122
    Node.js: 12.14.1
    V8: 8.3.110.13-electron.0
    OS: Windows_NT x64 10.0.18363

### Python

    Version:  Python 3.9.1

**NOTE**: this gist does not explain how to install Python.

---

---

## Steps to creating a 'venv'

### Create a folder for the project

There are 2 options:

1. Create a repository on [GitHub.com](https://github.com "GitHub.com") BEFORE creating the project folder on the local machine.

    Once the repository is created, clone it onto the local machine.

    **NOTE**: This procedure will not be covered here but it will be in a future Gist.

    OR

2. Create the project folder locally (see below gist)

   - First, open a **Terminal Prompt within VS Code**.

   - Then, go to the folder where the new project is to be created, *i.e.* go to the 'working folder'.

        For example, if the main folder is called ```python_projects```, go to

            C:\python_projects

        Hence, for the **relative path**, type:

            cd /python_projects

   - Create a folder for the project called ```project_name``` and check if it is present in the working folder

            mkdir project_name && dir

   - ```cd``` into this folder

            cd project_name

   - Open the project folder ```project_name``` from the menu in VS Code

---

### Create a virtual environment for the project

- Create a ```.py``` python file into ```project_name``` and ```cd``` into it

        echo >> python_script.py

    Alternatively, create the ```.py``` file from VS Code menu.

- Open ```python_script.py``` file

    **NOTE**: it is important to **create** AND **open** a ```.py``` file BEFORE creating and activating the venv, as it helps with its activation

- Create a virtual environment called ```venv_name```

    The command below will create a new folder called ```venv_name```

        python -m venv venv_name

    NOTE: the virtual environment name can be anything (like ```banana```).
    However, it is common practice to use just ```venv```. This is handy when copying/pasting code snippets.

    Hence, use the following command:

        python -m venv venv

    NOTE: a message will appear (bottom right) asking to use the new environment, click 'Yes'.

    Alternatively, choose from the list of environments (bottom left). The Python version should be listed with ```venv``` in parentheses, *e.g.*

        Python 3.9.1 64-bit ('venv')

---

### Activate the new virtual environment ```venv```

If using the default command prompt (```cmd```), type:

    .\venv\Scripts\activate

If using Windows PowerShell (```PS```), type:

    .\venv\Scripts\Activate.ps1

IMPORTANT: if no changes seem to occur, open a new terminal prompt to activate the environment.

The active path should now be preceded by ```(venv)``` or ```(banana)``` if a specific venv name was chosen.

---

### Create 'default' folders and files

These will be needed for the project, *e.g.*:

    mkdir data, docs, tests, sources, scripts, figures
    
    echo >> __init__.py
    echo >> main.py
	echo >> config.py
	echo >> setup.py
    echo >> requirements.txt

OPTION: if the project is to be hosted on GitHub, the following files can be created, or done automatically when creating a repository.

    echo >> README.md
    echo >> LICENSE
    echo >> .gitignore
    echo >> .gitkeep

NOTE 1: the 'LICENSE' and '.gitignore' files do NOT take a file extension. Only 'README.md' does.

NOTE 2: add a copy of .gitkeep into each folder in order to commit empty folders to GitHub.

---

### Record the dependencies for the project

- First, update the ```pip``` library

        python -m pip install --upgrade pip

- Then, create the dependencies file named ```requirements.txt```

        pip list > requirements.txt

---

### Install a Python Library

    pip install package_name

If installing more than one package, type:

    pip install package_name_1 package_name_2

If installing a specific version of a package, type:

    pip install package_name=1.6

---

### Save the new dependencies

It is better to use ```pip freeze``` instead of ```pip list``` as it allows to pin the dependencies version.

    pip freeze > requirements.txt

#### Install dependencies from a file

The ```requirements.txt``` file can be used within a **new environment** to install dependencies cleanly with the following command:

    python -m pip install -r requirements.txt

IMPORTANT: this only works if ```requirements.txt``` was produce with ```pip freeze``` and NOT ```pip list```.

---

### Check dependency clashes after installing all packages

    pip check

---

### Deactivate the virtual environment

    deactivate

---

### Bonus: Linting & Formatting

The following linters can be "pip-installed" and ran from the terminal:

    pydocstyle main.py
    pycodestyle main.py
    autoflake main.py
    flake8 main.py

Similarly, the formatter called `black` can be run:

    black main.py

NOTE: do not forget to `pip freeze` the linter/formatter libraries to `requirements.txt`.

---

### Bonus 2: `pipreqs`, or `pip freeze` made eazy

With the `pipreqs` library, all the dependancies are removed, thus simplifying the structure of the `requirements.txt` file.

- First, pip-install the `pipreqs` library

- Then, run the code below to create a `requirements.txt` file:

        pipreqs .

Note: if the `requirements.txt` file already exists, run the following code to overwrite it:

    pipreqs . --force

COPIED FROM: https://gist.github.com/loic-nazaries/c25ce9f7b01b107573796b026522a3ad