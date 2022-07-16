# constyle
A Python library to add style to your console.

The name of the library comes from merging the words **CONSoLE** and **STYLE**.

## Installation

You can install this package with pip or conda.
```sh
$ pip install constyle
```
```sh
$ conda install -c abrahammurciano constyle
```

## Links

The full documentation is available [here](https://abrahammurciano.github.io/python-constyle/constyle).

The source code is available [here](https://github.com/abrahammurciano/python-constyle).

## Usage

There are a couple of ways to use this library.

### The `style` function

The simplest way is with the `style` function.

```py
from constyle import style, Attributes

print(style('Hello World', Attributes.GREEN, Attributes.BOLD, Attributes.ON_BLUE))
```

### `Attribute` objects

`Attribute` objects are all callable, and calling them will apply their style to the given input string.

```py
from constyle import Attributes

underline = Attributes.UNDERLINE
print(underline("You wanna experience true level? Do you?"))
```

### `Style` objects

You can also use `Style` objects to create a reusable style with several attributes. `Style` objects are callable and take a string as input and return a styled string.

Adding together `Attribute` objects will also create `Style` objects, as will adding `Attribute`s to existing `Style` objects.

```py
from constyle import Style, Attributes

warning = Style(Attributes.YELLOW, Attributes.BOLD)
whisper = Attributes.GREY + Attributes.DIM + Attributes.SUPERSCRIPT

print(warning('You shall not pass!'))
print(whisper('Fly you fools'))
```

### Attributes

The `Attributes` enum contains all the available ANSI attributes. You can read more about them [here](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters).

You'll find there is limited support for all the ANSI attributes among consoles.

If you need more attributes than the ones provided in this enum, you can create your own by using the `Attribute` class.

### Nesting

Nesting strings is not supported. The inner string will cause the rest of the outer string to lose its formatting.

> NOTE: I would like to implement a fix for this in future, but I am uncertain if it is even possible, let alone feasible. If you have any suggestions, feel free to open an issue.

```py
from constyle import Attributes

bold = Attributes.BOLD
yellow = Attributes.YELLOW
green = Attributes.GREEN

print(yellow(bold('This is bold and yellow')))
print(green(f"This is green. {yellow('This is yellow.')} This is no longer green"))
```

### RGB and 8-bit colours

You can create an attribute for whichever colour you want with the classes `ForegroundRGB`, `BackgroundRGB` and `Foreground8Bit` and `Background8Bit`. For example:

```py
from constyle import ForegroundRGB, style

print(style("This is a pink string", ForegroundRGB(255, 128, 255)))
```

### The command line interface

This package also provides a very basic command line interface to print styled strings.

Use `constyle --help` to see how to use it.