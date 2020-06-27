# Contents

This folder contains the LaTeX source for the 2018 PRACE-MaX AiiDA tutorial.

**Note:** The LaTeX source is kept only for historical reasons
and has been replaced by the markdown/rst based version.

## Compiling LaTeX source

```
make
```

## Export to markdown/rst

The LaTeX source can be converted as follows:

### Prerequisites

* pandoc
* python3

### Conversion

```console
$ pip install -r requirements.txt
$ make markdown
$ make rst
```
