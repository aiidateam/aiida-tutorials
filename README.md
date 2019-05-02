[![Documentation Status](https://readthedocs.org/projects/aiida-tutorials/badge/?version=latest)](https://aiida-tutorials.readthedocs.io/en/latest/?badge=latest)

# AiiDA tutorials

The official place to find materials from AiiDA tutorial events,
interactive demos and videos.

Visit http://aiida-tutorials.readthedocs.org

## Contributing

We highly welcome contributions of

 * links to new tutorial materials
 * corrections of existing tutorial materials

If you would like to contribute a fix or a link to a new tutorial resource, please:

 * Fork this repository
 * Make your changes
 * Submit a [pull request](https://github.com/aiidateam/aiida-tutorials/pulls)

If you have a question, feel free to just [open an issue](https://github.com/aiidateam/aiida-tutorials/issues/new).

## Building the web site locally

### Prerequisites

 * python 2.7 or greater
 * [pandoc](https://pandoc.org/)

### Build instructions

```
git clone https://github.com/aiidateam/aiida-tutorials.git
cd aiida-tutorials/docs
pip install -r requirements.txt
make
# open build/html/index.html
```

Note that `make` will run with the nitpick option, treating warnings as errors.
If you are updating the documentation and warnings are expected, run `make html` instead.
This does not use the nitpick exception and will ensure that the documentation compiles despite the warnings.

## Acknowledgements

This work is supported by the [MARVEL National Centre for Competency in Research](<http://nccr-marvel.ch>)
funded by the [Swiss National Science Foundation](<http://www.snf.ch/en>), as well as by the [MaX
European Centre of Excellence](<http://www.max-centre.eu/>) funded by the Horizon 2020 EINFRA-5 program,
Grant No. 676598.

![MARVEL](docs/assets/images/MARVEL.png)
![MaX](docs/assets/images/MaX.png)
