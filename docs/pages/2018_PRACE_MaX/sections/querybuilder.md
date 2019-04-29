Queries in AiiDA: The Querybuilder
==================================

This part of the tutorial is provided only in interactive mode through a Jupyter notebook, which you will be able to run in your browser. To accomplish this we first need to start the Jupyter server, if you didn’t do it already at the very beginning of the tutorial. First make sure you are connected to the virtual machine with local forwarding enabled, as described in section [sec:sshintro]. Then, on the virtual machine, first make sure your are in the `aiida` virtual environment:

``` bash
workon aiida
```

If the virtual environment is successfully loaded, your prompt should be prefixed with `(aiida)`. To finally launch the Jupyter server, execute the following commands:

``` bash
cd ~/examples/aiida-demos/tutorial/
jupyter notebook --no-browser
```

If all went well, you should now be able to open up a browser on your local machine and point it to the following address `http://localhost:8888/?token=2a3ba3...` (replace the token with the one printed on output by the previous command). This should now show you a directory navigator. To open the notebook, click on `querybuilder` and then select the file `tutorial.ipynb`. Note that there is also a `solution.ipynb`, which is a copy of the same notebook, but which contains the solutions to all the exercises. You can use this version at your own discretion if you get stuck at some point (but we suggest that you try not to look at it at first).
