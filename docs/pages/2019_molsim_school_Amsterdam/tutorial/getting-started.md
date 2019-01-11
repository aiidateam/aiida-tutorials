Getting started
===============

Start the Quantum Mobile virtual machine, open a terminal window and
type

```terminal
$ workon aiida
```

This activates the virtual environment, in which AiiDA is installed.

Since Quantum Mobile focuses on *ab initio* calculations, it is missing
some aiida plugins we are going to need. Let’s install them (this can
take 3 minutes):

```terminal
$ pip install --upgrade aiida-raspa aiida-zeopp
```

Before we start creating data ourselves, we are going to look at an
existing AiiDA database. Let’s import one from the web:

```terminal
$ verdi import https://www.dropbox.com/s/3f4895jq9eskqw3/export.aiida?dl=1
```
