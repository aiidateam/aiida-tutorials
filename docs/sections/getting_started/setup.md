---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.8'
    jupytext_version: 1.4.1+dev
kernelspec:
  display_name: Python 3
  name: python3
notebookmetadatakey: val
notebookmetadatakey2: val2
---

(fundamentals-setup)=

# Setup on AiiDAlab

It is assumed that most users will find it easiest to follow the tutorial on the dedicated AiiDAlab instance accessible at [https://aiida-intro-tutorial-2021.aiidalab.net](https://aiida-intro-tutorial-2021.aiidalab.net).
This instance of AiiDAlab is pre-configured with all the software needed for the tutorial and is the fastest way to get started for anyone who does not already have AiiDA installed and configured on their own machine.

This is how you access the server:

  1. If you do not have a GitHub account yet, create one at [https://github.com/login](https://github.com/login).
  2. Open [https://aiida-intro-tutorial-2021.aiidalab.net](https://aiida-intro-tutorial-2021.aiidalab.net) in your browser (we tested Firefox and Chrome).
  3. Click on "Sign in with GitHub".
  4. At this point you might be asked to log into your GitHub account unless you are already logged in.
     If you do not have an account yet, create one now.
  5. When asked to authorize the "AiiDA Intro Tutorial 2021" app, click on "Authorize aiidalab".
  6. The server is then prepared for your account, and you will be redirected to the JupyterLab interface after 1-2 minutes.

Subsequent logins should take you directly to the server as long as you have cookies enabled within your browser.

```{figure} include/images/first-login.gif
:align: center

Demonstration of the (first) login procedure.

```

```{important} The tutorial server will be kept online for a few more days after the tutorial has eneded.
After that it will be shut down and **all data will be removed**.
Please see the instructions below to download your data from the server.
```

## How download your data

To download your data from the server prior to its destruction:

  1. Open a terminal by clicking on "Terminal" on the start screen.
  2. Execute `zip -r home.zip .`.
  3. Right-click on the `home.zip` file within the file browser tab.
  4. Click on "Download".

```{tip} You do not have to download the whole home directory of course, you can just download the files or directories that you would like to preserve.
```

# Setup on your own machine

```{warning} The tutorial was tested on the AiiDAlab server introduced above.
It might be advisable to follow the tutorial on the AiiDAlab instance even after installing AiiDA on your own machine.
```

To run the tutorial on your own machine, you need to install

- [AiiDA](https://aiida.readthedocs.io/projects/aiida-core/en/latest/intro/get_started.html) (version 1.6.3)
- [aiida-quantumespresso](https://aiida-quantumespresso.readthedocs.io/en/latest/#installation) (version 3.4.2)
- [QuantumEspresso](https://www.quantum-espresso.org/) (version 6.6)

```{note} Version numbers indicate the versions with which the tutorial was tested.
```
