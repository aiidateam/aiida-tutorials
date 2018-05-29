Ranking the structures
======================

We've prepared an interactive jupyter app that helps you with ranking
and visualizing the structures. Use at your convenience.

To get the app please download it using the following link:

```bash
wget https://www.dropbox.com/s/hced3imzvqoij0g/molsim.tar.gz?dl=1 \
  -O molsim.tar.gz 
tar -xzf molsim.tar.gz
```

If you are working with Quantum Mobile, simply place the extracted
folder inside `/project/apps` and it should already work.

In case you have configured AiiDA on your own computer please install
additional packages:

```bash
pip install jupyter matplotlib bokeh plotly ase 
tar -xzf molsim.tar.gz
```

We also recommend to have jupyter appmode installed. For more details
and installation instructions please visit [this
page](https://github.com/oschuett/appmode).

To use the application please open `dc_group.ipynb` (in case you were
following the section 4.1 route) or `dc_wf.ipynb` (in case you have
chosen 4.2) and switch to the Appmode for the convenience. For the users
of Quantum Mobile it is enough to launch "Jupyter Apps" icon on the
desktop and chose corresponding notebook from the "Molsim course" app.
Once you have opened the notebook, specify the group of structures (if
required) and press the "Plot" button.

We recommend to use the "bokeh" framework as it shows the corresponding
structure pk once you put the cursor on top of a point.
