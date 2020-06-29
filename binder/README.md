# Binder Environment Creation

This Dockerfile is for use with <https://mybinder.org/>.
The template was initially created using [repo2docker](https://github.com/jupyter/repo2docker).

To create the docker container locally run in the root folder:

```console
$ docker build --file binder/Dockerfile --tag tutorial-binder:v1 .
$ docker run --rm -p 8888:8888 tutorial-binder:v1
```

The container uses [tini](https://github.com/krallin/tini) to act as the PID 1 (as used by [jupyter/docker-stacks](https://github.com/jupyter/docker-stacks/blob/master/base-notebook)), as opposed to[phusion/baseimage-docker](https://github.com/phusion/baseimage-docker). Actually you can enable this with `docker run --init`, but it doesn't appear that this option is used by binder.
