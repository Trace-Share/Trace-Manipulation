# Trace-Manipulation
[![Build Status](https://travis-ci.org/Trace-Share/Trace-Manipulation.svg?branch=master)](https://travis-ci.org/Trace-Share/Trace-Manipulation)

Library for manipulation of network traffic traces

## Table of Contents

- [Trace-Manipulation](#trace-manipulation)
  - [Table of Contents](#table-of-contents)
  - [Setting up the library](#setting-up-the-library)
  - [Usage](#usage)
    - [SubMng](#submng)
    - [TMdict](#tmdict)
    - [ReWrapper](#rewrapper)
    - [Transformation functions](#transformation-functions)
  - [Examples](#examples)
  - [Contribution](#contribution)

## Setting up the library

Clone the repository into your project...

`git clone https://github.com/Trace-Share/Trace-Manipulation.git`

...or add it as a submodule into your repository.

`git submodule add https://github.com/Trace-Share/Trace-Manipulation`

You can also specify the a diretory to add the submodule into.

`git submodule add https://github.com/Trace-Share/Trace-Manipulation directory/Trace-Manipulation`

Install the requirement from the `requirements.txt` file.

`pip install -r requirements.txt`

And to be able to call the library in your code, add the directory into the system path.

```python
import sys
from pathlib import Path
## __file__ points to the path of the current file
sys.path.insert(0, str(Path( Path(__file__).parent / Path('<folder>/Trace-Manipulation') ).resolve()) )
```

## Usage

Trace-Manipulation library comes with scapy_extend module. This module contains all additional protocols.

The core library modules are the `ReWrapper`, `SubMng` (subscriber manager) and `TMdict` (trace manipulation dictionaries).

### SubMng

This module serves to collect all the transformation function in one place. It handles adding all of the required fuctions into the `ReWrapper` instance. It prescribes a specific format for addition of new functions. Further details can be found in the docstrings.

### TMdict

This module servers to contain all the data required by transformation functions. It consists of dict class extensions with predefined methods and support for executing validation functions. Further details on the data dictionaries can be found in the docstrings.

### ReWrapper

This module contains the packet processing class. It provides functionality for building transformation function queues for specified protocols and facilitates packet processing. Further details can be found in the docstring of the module.

### Transformation functions

Transformation functions can be found in `TMLib.trasnf.` module (directory). Thissubmodule contains definitions of all of the trasnfromation functions. `TMLib.subscribers` submodules handle subscribing the functions into the `SubMng` module. **Subscriber submodule must be manually imported to load them into the `SubMng` module.** Such as `from TMLib.subscribers import default_fs`. This is done to allow choosing which extensions are included in the `SubMng`.

## Examples

Some examples of projects using `TMLib`.

> [Trace-Normalizer](https://github.com/Trace-Share/Trace-Normalizer)

> [ID2T Trace-Mixing](https://github.com/Trace-Share/ID2T/tree/dev-restructure)

## Contribution

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

*If you are interested in research collaborations, don't hesitate to contact us at  [https://csirt.muni.cz](https://csirt.muni.cz/about-us/contact?lang=en)!*
