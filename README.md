# constyle
A Python library to add style to your console.

The name of the library comes from merging the words **CONSoLE** and **STYLE**. Also "con" means "with" in Spanish.

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

Join the support Discord server [here](https://discord.gg/nUmsrhNDSs).

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

Use `constyle --help` to see how to use it.
