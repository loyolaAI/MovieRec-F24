# This file will go over all the information people need to start working with the project

I must preface that I am nowhere near an expert on GitHub and you should refer to [this guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests) for a lot more information. If you get stuck or need help. Please email me at njohnson14@luc.edu or slack me on the *LAIC* slack. ChatGPT is also a very good resource for everything about github, so please ask it as many questions as you need. You will also need to be somewhat familiar with using the command line, but it's not very hard. If you feel like you need help, I would recommend you skim [this](https://gist.github.com/bradtraversy/cc180de0edee05075a6139e42d5f28ce) github article or ask ChatGPT how to do something you wanna do, it will tell you. [Here](https://education.github.com/git-cheat-sheet-education.pdf) is a github command cheat sheat. Which will be helpful for people working with github for the first time.

Now lets move onto this very **rushed** and **poorly** written guide. 

## Install python

To check if you have python installed, open a terminal on your computer and type
```
python3
```
If something like what is below is outputted, you already have python installed. If not, please refer to the instructions below
```
Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

If you don't already have python installed on your computer you will need to install it. I recommend installing it through [anaconda](https://www.anaconda.com/download). Anaconda will also allow you to manage and install packages like `numpy` and `pandas`, which we will be using in the code. Please follow the guide for installation on the anaconda web page.

## Install git

To check if you have git installed, open a terminal and type
```
git
```
If something like what is below is outputted, you already have git installed (it should be installed by default on most computers). If not, please refer to the instructions below
```
usage: git [-v | --version] [-h | --help] [-C <path>] [-c <name>=<value>]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p | --paginate | -P | --no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           [--super-prefix=<path>] [--config-env=<name>=<envvar>]
           <command> [<args>]

These are common Git commands used in various situations:
...
```

If you dont have `git` installed you will need to install it. Please refer to [this](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) guide for installation, and ask chatGPT if you get stuck (it's very good for installing things).

## Installing an IDE

IDE stands for integrated development environment and is what most people code in. I recommend using VSCode which can be downloaded as an application [here](https://code.visualstudio.com/download). You don't need an IDE to code, but it will more likely than not help a great deal (unless you're a wizard with VIM).

## Create a github account if you don't already have one

This should be pretty self explanatory. You will need a github account to work with the code, so make one if you dont have one.

## Fork this repository

You will need to create your own fork of this repository, to do that please refer to this [guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo).

## Create a github SSH key

You will need a github SSH key so that you will be able to communicate with the remote repository you just created (your own fork). To do this please refer to this [guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

## Create a new branch on github website.

It's considered good practice to work out of a specific branch for specific features. To create a new branch, while on your fork of the main repository. you need to 
- At the top left, near the branch dropdown menu, you'll see a button that displays the current branch (e.g., main).
- Click on the dropdown, and in the text box that appears, type a new branch name.
- Press **Enter** to create the new branch.

## Clone the repository and switch to the new branch.

To clone the repo, make sure you're on your own version of the repo, and click the green `<code>` section in the middle / left of the screen and make sure you click the `ssh` clone option, copy that link.

You then need to open up your IDE of terminal and go somewhere you want the repository to be placed. then type
```
git clone URL_YOU_JUST_COPIED
```
for me this looks like 
```
git clone git@github.com:nathanjohnsongithub/MovieRec-F24.git
```

### Switch to the new branch

To switch to the new branch you created, you need to make sure your code is up to date (it should be) so you need to type.
```
git fetch origin
```
Now you need to checkout your new branch
```
git checkout your-new-branch-name
```
**NOTE `your-new-branch-name` is the name you typed on the github website**

you can now type `git branch` to check which branch you're working out of. If it says something like
```
* your-new-branch-name
main
```
The star (*) means your currently on the branch titled `your-new-branch-name`

## Making changes 

Now you're free to edit and work with the code!!!! How exciting.

After you've edited the code and are ready to publish your changes (Or if you want to do a sample of publishing something, I would recommend you add a line in the `README.md` file to practice). First, you should type
```
git status
```
this will show you everything that has changed since you cloned the repository. For example, 
```
On branch README
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        data/archive.zip
        data/genome_scores.zip
        data/rating.zip

nothing added to commit but untracked files present (use "git add" to track)
```
Now lets say you want to add / publish the `README.md` file. you will need to first type
```
git add README.md
```
**NOTE : the name does not need to be `README.md` it should be any file you wish to add**
this will add the file, which you are about to commit.

After you've added all the files you wish, you need to commit them. to do that, type the command below.
```
git commit -m "MESSAGE TO ADD"
```
For the "Message to add" you should type whatever applies to what you've changed about the code. For example, If you fixed a bug. You would type `git commit -m "Bug fix"`

After everything has been commited and is ready to be added to the github.com remote repository, all you need to do is type
```
git push
```
This will push your changes to the remote repository. 

## Pull requests

Pull requests are a way for you to merge the things you've been working on with the main version of the code (not just your own fork). Please read about creating pull request [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)

## Thats all!

I think I've covered everything you need to know about working with the code. Some other things you guys will need to learn is installing packages that we will be using, but we can go over that once it becomes an issue. Once again please email me at njohnson14@luc.edu or DM me through the *LAIC* Slack if you have any questions and **GOOD LUCK**.
