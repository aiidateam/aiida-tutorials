Instructions to SSH to the Amazon EC2 instance
----------------------------------------------

You should have received an IP address from the instructors, and two files with a private and a public SSH key (`aiida_tutorial_NUM` and `aiida_tutorial_NUM.pub`), where `NUM` is an integer. These allow you to connect to an Amazon EC2 instance (different for each participant of the tutorial). To connect via `ssh` to this machine follow the steps below, depending on the computer you have.

**Note!** *If you decide to work in pairs, one of the two people should discard his email. The other person should forward his email to the colleague, and both should then use the same virtual machine IP and account (ssh key). In this case, you will be both using the same account, so be careful not to delete the work of your colleague.*

### Linux and Mac

-   If needed, create a `.ssh` directory in your home (`mkdir ~/.ssh`), and set its permissions:
    `chmod 700 ~/.ssh`

-   Copy in this `.ssh` directory the two files `aiida_tutorial_NUM` and
    `aiida_tutorial_NUM.pub`

-   Set the correct permissions on the private key:
    `chmod 600 ~/.ssh/aiida_tutorial_NUM` (then check with `ls -l` that the permissions of this file are now `-rw-------`).

-   Create (or modify if it already exists) the `config` file in your `.ssh` directory, adding the following lines:

    ```console
    Host aiidatutorial
      Hostname IP_ADDRESS
      User aiida
      IdentityFile ~/.ssh/aiida_tutorial_NUM
      LocalForward 8888 localhost:8888
    ```

    where you have to replace `IP_ADDRESS` with the IP address provided to you.

-   You can then `ssh` to the Amazon EC2 instance from the terminal, using simply

    ``` terminal
      ssh -X -C aiidatutorial
     
    ```

    (connecting with `-X` — note that sometimes `-Y` is needed instead — will allow you to run graphical programs such as xmgrace or gnuplot interactively, even if they might not be very responsive as the Amazon virtual machines are in Ireland).

### Windows

-   Install PuTTY.

-   Run PuTTYGen, load the `aiida_tutorial_NN` private key (button `"Load"`). remember to choose to show “All files (\*.\*)” in the window, and select the file without any extension (Type: File).

-   In the same window, click on “Save private Key”, and save the key with the name
    `aiida_tutorial_NN.ppk`.

-   Run Pageant: it will add a new icon near the clock, in the bottom right of your screen.

-   Right click on this Pageant icon, and click on “View Keys”.

-   Click on `"Add key"` and select the `aiida_tutorial_NN.ppk` you saved a few steps above.

-   Run PuTTY, put the given IP address as hostname. Write `aiidatutorial` in Saved Sessions and click `Save`. Go to Connection \(\to\) Data and put `aiida` as autologin username. Under Connection, go to SSH \(\to\) Tunnels, type `8888` in the `Source Port` box and `localhost:8888` in `Destination` and click `Add`. Click on `Save` again on the Session screen.

-   Now select `aiidatutorial` from the session list, click `Load` and, finally, `open`.

Everybody: connect to the machine and start jupyter
---------------------------------------------------

Before starting the tutorial, connect via SSH to the Amazon machine as explained above (the Amazon machine already contains a pre-configured AiiDA installation and some test data for this tutorial).

Before starting
---------------

Once connected to your machine, type in the remote terminal

``` terminal
 workon aiida
```

This will enable the virtual environment in which AiiDA is installed, allowing you to use AiiDA. Now type in the same terminal

``` terminal
 jupyter notebook --no-browser
```

This will run a server with a web application called `jupyter`, which is used to create interactive python notebooks. To connect to this application, copy the URL that has been printed to the terminal (it will be something like `http://localhost:8888/?token=2a3ba37cd1...`) and paste it into the URL bar of a web browser. You will see a list of folders: these are folders on the remote Amazon computer. We will use `jupyter` in section [sec:querybuilder] and optionally in other sections as well.

Now launch an identical `ssh` connection (again, as explained above) in another terminal, and type `workon aiida` here too. This terminal is the one you will actually use in this tutorial.

Note: Since the port listening is set to a specific port (8888) in the section [sec:sshintro], you have to make sure on the server the Jupiter notebook is running on the port 8888. Otherwise, use an alternative port for listening.

A final note: for details on AiiDA that may not be fully explained here, you can refer to the full AiiDA documentation, available online at <http://aiida-core.readthedocs.io/en/latest/>.

Troubleshooting tips (in case you have issues later)
----------------------------------------------------

-   If you get an error like `ImportError: No module named aiida` or `No command ’verdi’ found` double check that you have loaded the virtual environment with `workon aiida` before launching python, ipython or the jupyter server.

-   If your browser cannot connect to the jupyter instance, check that you have correctly configured SSH tunneling/forwarding as described above. Also note that you should run the jupyter server from the terminal connected to the Amazon machine, while the web browser should be opened locally on your laptop or worstation.

-   The Jupyter Notebook officially supports the latest stable versions of Chrome, Safari and Firefox. See <http://jupyter-notebook.readthedocs.io/en/4.x/notebook.html#browser-compatibility> for more information on broswer compatibility (and update your browser if it is too old).
