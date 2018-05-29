Ranking the structures
======================

We've prepared an interactive jupyter app that helps you with ranking
and visualizing the structures. Use at your convenience.

### Installation
To get the app please download it using the following link:

```bash
wget {{ site.url }}/assets/2018_EPFL_molsim/ranking.tar.gz
tar -xf ranking.tar.gz
```

If you are working with Quantum Mobile, simply place the extracted
folder inside `/project/apps` and it should already work.

In case you have configured AiiDA on your own computer please install
additional packages:

```bash
pip install jupyter matplotlib bokeh plotly ase appmode
jupyter nbextension     enable --py --sys-prefix appmode
jupyter serverextension enable --py --sys-prefix appmode
```

### Usage

To use the application please open 

 - `dc_group.ipynb`, if you followed the *quick and simple* route
 - `dc_wf.ipynb`, if you followed the *elegant and robust* route

Switch to the Appmode for the convenience. 

For the users of Quantum Mobile it is enough to launch "Jupyter Apps" icon on
the desktop and chose corresponding notebook from the "Molsim course" app.

Once you have opened the notebook, specify the group of structures (if
required) and press the "Plot" button.

We recommend to use the "bokeh" framework as it shows the corresponding
structure pk once you put the cursor on top of a point.
