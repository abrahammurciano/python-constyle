# constyle
A Python library to add style to your console.

The name of the library comes from merging the words **CONSoLE** and **STYLE**. Also "con" means "with" in Spanish.

## Installation

You can install this package with pip or conda.
```sh
$ pip install constyle
```
```sh
$ conda install -c conda-forge constyle
```
```sh
$ conda install -c abrahammurciano constyle
```

## Links

[![Documentation](https://img.shields.io/badge/Documentation-C61C3E?style=for-the-badge&logo=Read+the+Docs&logoColor=%23FFFFFF)](https://abrahammurciano.github.io/python-constyle/constyle)

[![Source Code - GitHub](https://img.shields.io/badge/Source_Code-GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=%23FFFFFF)](https://github.com/abrahammurciano/python-constyle.git)

[![PyPI - constyle](https://img.shields.io/badge/PyPI-constyle-006DAD?style=for-the-badge&logo=PyPI&logoColor=%23FFD242)](https://pypi.org/project/constyle/)

[![Anaconda - constyle](https://img.shields.io/badge/Anaconda-constyle-44A833?style=for-the-badge&logo=Anaconda&logoColor=%23FFFFFF)](https://anaconda.org/abrahammurciano/constyle)

[![Discord - Community](https://img.shields.io/badge/Discord-Community-5865F2?style=for-the-badge&logo=Discord&logoColor=FFFFFF)](https://discord.gg/nUmsrhNDSs)

## Usage

There are a couple of ways to use this library.

### The `style` function

The simplest way is with the `style` function.

```py
from constyle import style, Attributes

print(style('Hello World', Attributes.GREEN, Attributes.BOLD, Attributes.ON_BLUE))
```

### `Style` objects

You can also use `Style` objects to create a reusable style with any number of attributes.

#### Calling a `Style` object

`Style` objects are callable and take a string as input and return a styled string.

```py
warning = Style(Attributes.YELLOW, Attributes.BOLD)
print(warning('You shall not pass!'))
```

#### Adding `Style` objects

Adding together `Style` objects will also create `Style` objects.

```py
whisper = Attributes.GREY + Attributes.DIM + Attributes.SUPERSCRIPT
print(whisper('Fly you fools'))
```

#### Converting `Style` objects to strings

`Style` objects can be converted to strings to obtain the ANSI escape sequence for that style.

```py
warning = Style(Attributes.YELLOW, Attributes.BOLD)
print(f"{warning}You shall not pass!{Attributes.RESET}")
```

### Attributes

The `Attributes` enum contains all the available ANSI attributes. You can read more about them [here](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters).

`Attributes` are also `Style` objects, and as such, as demonstrated above, they too can be called to style a string, added together and to other `Style` objects, and converted to strings to obtain their ANSI sequence.

You'll find there is limited support for all the ANSI attributes among some consoles.

If you find more attributes that aren't provided in this enum, you can create your own by constructing a `Style` with an integer.

### Nesting

In order to nest styles, you can use the `end=` keyword argument of the `style` function or the `Style` class. Usually when applying a style, the `RESET` attribute is appended to the end. This can be undesirable when nesting (see the example below).

```py
bold = Attributes.BOLD
yellow = Attributes.YELLOW
green = Attributes.GREEN

print(yellow(bold('This is bold and yellow')))
print(green(f"This is green. {yellow('This is yellow.')} This is no longer green"))
```

In order to achieve the desired result in the above example, you would have to use the `end=` keyword argument of the `style` function. You can pass any `Style` to `end`.

```py
print(green(f"This is green. {bold('This is green and bold.', end=Attributes.NO_BOLD)} This is still green but not bold anymore"))
print(green(f"This is green. {yellow('This is yellow.', end=green)} This is now green again"))
```

### Custom colours

The `constyle.custom_colours` module contains a few classes that can be used to create custom colours.

#### RGB colours

You can create a `Style` for a custom RGB colour by using the `RGB` class. This is not well supported by all consoles.

```py
from constyle.custom_colours import RGB

print(style('This is pink', RGB(255, 192, 203)))
```

#### 8-bit colours

Some consoles support 8-bit colours. You can create a `Style` for an 8-bit colour by using the `EightBit` class, passing a single integer to it, or you can use the `EightBitRGB` class to create an 8-bit colour style as close to the RGB values as possible.

## The command line interface

This package also provides a very basic command line interface to print styled strings.

You can pass it any number of strings and it will print them all together (like `echo`). You can pass `--attribute` (or `-a`) with the name of an attribute to apply to the other strings being printed. You can pass `--attribute` as many times as you like.

You can use `constyle --help` to see more specific details, as well as all available attributes.

For example you can use `constyle` from your shell to print some styled text.

```sh
$ constyle Hello World! -a green -a bold -a on_white
```

Or if you're writing a shell script you can make an alias or a function to reuse a certain style.

```sh
#!/bin/bash
alias error="constyle --attribute bold --attribute red" # With an alias
warn() { constyle $@ -a bold -a yellow } # With a function
error You shall not pass!
warn Fly you fools!
```