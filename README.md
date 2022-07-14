# Python Package Template

This repository contains the basic structure for a python package as well as some useful GitHub actions for maintaining the package.

In order to use this template you must perform the following steps. In each step I will explain how you can do it manually and I will also provide commands (sorry windows users, sucks to suck) to automate the process where possible.

## 1. Set command variables

In the following instructions, commands will make reference to several variables. You can set these variables now so you can run all subsequent commands without having to edit them. (Replace `...` with actual values.)

```sh
PACKAGE_NAME="..." # The name of your package. Use kebab-case.
MODULE_NAME=$(echo $PACKAGE_NAME | tr - _) # The name of your module. Should be the package name in snake_case.
PACKAGE_DESCRIPTION="..." # A short description of your package
YOUR_NAME="..." # Your name. Use spaces and start each word with an uppercase letter
YOUR_EMAIL="..." # Your email address
GITHUB_USERNAME="..." # Your GitHub username
ANACONDA_USERNAME="..." # Your Anaconda username
MIN_PYTHON_VERSION="..." # The minimum version of Python required to use this package
```

If you won't be using the commands below, just make a note of the values you would give to each variable for when they're needed.

## 2. Clone the template

Download the code and place it in a folder, then enter the folder. From now on all commands will be relative to this folder.

```sh
git clone https://github.com/abrahammurciano/python-package-template.git python-$PACKAGE_NAME
cd python-$PACKAGE_NAME
rm -rf .git
```

## 3. Replace placeholder text

There are several placeholders that you must replace with values from step 1. These match this regular expression: `<<[A-Z_]+>>`. You can use your IDE to find all such placeholders and replace them, or you can use the following commands to do the same.

```sh
find ./ -type f -exec sed -i -e "s/constyle/$PACKAGE_NAME/g" {} \;
find ./ -type f -exec sed -i -e "s/constyle/$MODULE_NAME/g" {} \;
find ./ -type f -exec sed -i -e "s/A Python library to add style to your console./$PACKAGE_DESCRIPTION/g" {} \;
find ./ -type f -exec sed -i -e "s/Abraham Murciano/$YOUR_NAME/g" {} \;
find ./ -type f -exec sed -i -e "s/abrahammurciano@gmail.com/$YOUR_EMAIL/g" {} \;
find ./ -type f -exec sed -i -e "s/abrahammurciano/$GITHUB_USERNAME/g" {} \;
find ./ -type f -exec sed -i -e "s/abrahammurciano/$ANACONDA_USERNAME/g" {} \;
find ./ -type f -exec sed -i -e "s/3.7/$MIN_PYTHON_VERSION/g" {} \;
```

Also don't forget to replace any occurences of a placeholder in folder and file names.

```sh
mv 'constyle' $MODULE_NAME
```

## 4. Create a GitHub repository

- Click [here](https://github.com/new) to create a new GitHub repository.
- Name it `python-$PACKAGE_NAME`.
- Enter the value of `$PACKAGE_DESCRIPTION` as the description.
- Don't initialize the repository with a readme, a .gitignore, a license, or any other files.

## 5. Give GitHub access to your PyPI and Anaconda accounts

- Create a [PyPI](https://pypi.org/account/register/) account if you don't have one.
- Create an [Anaconda](https://anaconda.org/account/register) account if you don't have one.
- Go to `your repository` > `Settings` > `Secrets` > `Actions`.
- Create four new repository secrets:
	- `PYPI_USERNAME`
	- `PYPI_PASSWORD`
	- `ANACONDA_USERNAME`
	- `ANACONDA_PASSWORD`

## 6. Push your code to GitHub

You can push your code with the following commands.

```sh
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/$GITHUB_USERNAME/python-$PACKAGE_NAME.git
git push -u origin main
```

## 7. Enable GitHub pages

Go to `your repository` > `Settings` > `Pages`.

TODO: finish this section

## 8. Enforce tests on pull requests to main

TODO: finish this section

## 9. Delete these instructions

Remove the text up to here from this file.

# constyle
A Python library to add style to your console.

## Installation

You can install this package with pip or conda.
```sh
$ pip install constyle
```
```sh
$ conda install -c abrahammurciano constyle
```

## Documentation

The full documentation is available [here](https://abrahammurciano.github.io/python-constyle/constyle).

## Usage
