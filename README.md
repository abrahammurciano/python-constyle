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

## Documentation

The full documentation is available [here](https://abrahammurciano.github.io/python-constyle/constyle).

## Usage

There are a couple of ways to use this library.

### The `style` function

The simplest way is with the `style` function.

```py
from constyle import style, Attributes

print(style('Hello World', Attributes.GREEN, Attributes.BOLD, Attributes.ON_BLUE))
```

### `Style` objects

You can also use `Style` objects to create a reusable style. `Style` objects are callable and take a string as input and return a styled string.

```py
from constyle import Style, Attributes

warning = Style(Attributes.YELLOW, Attributes.BOLD)

print(warning('You shall not pass!'))
```

### Attributes

The `Attributes` enum contains all the available ANSI attributes. You can read more about them [here](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters).

You'll find there is limited support for all the ANSI attributes among consoles.

If you need more attributes than the ones provided in this enum, you can create your own by using the `Attribute` class.

### Nesting

You can nest styled strings. This will replace all "reset" ANSI escape codes in the inner string with those of the outer style.

```py
from constyle import Style, Attributes

bold = Style(Attributes.BOLD)
yellow = Style(Attributes.YELLOW)
green = Style(Attributes.GREEN)

print(yellow(bold('This is bold and yellow')))
print(green(f"This is green. {yellow('This is yellow.')} This is still green"))
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