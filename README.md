[![Documentation Status](https://readthedocs.org/projects/aiida-tutorials/badge/?version=latest)](https://aiida-tutorials.readthedocs.io/en/latest/?badge=latest)

# AiiDA tutorials

The official place to find materials from AiiDA tutorial events,
interactive demos and videos.

Visit <http://aiida-tutorials.readthedocs.org>

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

* python 3.5 or greater

### Build instructions

```bash
git clone https://github.com/aiidateam/aiida-tutorials.git
cd aiida-tutorials
pip install -r requirements.txt
pre-commit install   # enable pre-commit hooks (optional)
cd docs/
make
# open build/html/index.html
```

Note that `make` will run with the nitpick option, treating warnings as errors.
If you are updating the documentation and warnings are expected, run `make html` instead.
This does not use the nitpick exception and will ensure that the documentation compiles despite the warnings.

## Writing and testing interactive content

When writing tutorial content that demonstrates interaction with AiiDA, it may be desirable to write and test this in a reproducible environment.
In the root of this project, the `docker-compose.yml` provides one way to achieve this, by configuring and starting up a Docker container (naturally this requires you to have installed [Docker](https://www.docker.com/)).
The container initialises an AiiDA environment, exposes ports for you to access locally, and mounts the `./docs/source/` inside the container.

To change what python packages are installed, alter `.docker/aiida-environment.yml`.
Also, if you place an AiiDA archive at `./docs/source/archive.aiida`, this will be imported on startup.

To start the container and wait for it to initialise:

```console
$ docker-compose up -d --build
$ docker exec aiida-core wait-for-services
```

To enter the container:

```console
$ docker exec -it --user aiida aiida-core /bin/bash
```

To run a verdi command:

```console
$ docker exec -it --user aiida aiida-core /bin/bash -c 'verdi shell'
```

To start a notebook server that you can access locally:

```console
$ docker exec -it --user aiida aiida-core /bin/bash -c "jupyter notebook --port=8888 --ip=0.0.0.0 --no-browser"
```

Then open <http://localhost:8888/?token=...> in your browser.

To start the REST API:

```console
$ docker exec -it --user aiida aiida-core /bin/bash -c "verdi restapi --port 5000 --hostname=0.0.0.0"
```

Then open <http://127.0.0.1:5000/api/v4> in your browser.
(TODO this currentl gives error: `172.21.0.1 - - [05/Jul/2020 05:35:45] "GET /api/v4 HTTP/1.1" 404 -`)

Once finished, shut down the container (**NOTE**, this will reset the aiida database):

```console
$ docker-compose down
```

## Acknowledgements

This work is supported by the [MARVEL National Centre for Competency in Research](<http://nccr-marvel.ch>)
funded by the [Swiss National Science Foundation](<http://www.snf.ch/en>), as well as by the [MaX
European Centre of Excellence](<http://www.max-centre.eu/>) funded by the Horizon 2020 EINFRA-5 program,
Grant No. 676598.

![MARVEL](docs/_static/images/MARVEL.png)
![MaX](docs/_static/images/MaX.png)
