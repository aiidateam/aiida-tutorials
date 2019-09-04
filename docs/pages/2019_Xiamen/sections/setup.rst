Getting set up
==============

.. _2019_xmn_connect:

Start your virtual machine
---------------------------

On your Huawei cloud account:

 * Add a new security group ``aiida-tutorial``, open ports 22, 5000, 8888
 * Start a new server: 
    * Flavor ``s6.large.2`` (2 vCPUs, 4 GB RAM) should be sufficient
    * Use shared image ``aiida-tutorial``
    * Use security group ``aiida-tutorial``
 * Copy the IP address of your new server

Please read the instructions below on how to connect using your operating system.
  
Linux and MacOS
~~~~~~~~~~~~~~~

It's recommended for you to place the ssh key you received in a folder
dedicated to your ssh configuration, to do so:

-  If not already present, create a ``.ssh`` directory in your home
   (``mkdir ~/.ssh``), and set its permissions: ``chmod 700 ~/.ssh``

Add the following block your
``~/.ssh/config`` file:

   .. code:: bash

     Host aiidatutorial
         Hostname IP_ADDRESS
         User max
         ForwardX11 yes
         ForwardX11Trusted yes
         LocalForward 8888 localhost:8888
         LocalForward 5000 localhost:5000
         ServerAliveInterval 120

replacing the IP address (``IP_ADDRESS``) and the ``NUM`` by
the one you received.

Afterwards you can connect to the server using this simple command:

.. code:: console

     ssh aiidatutorial

.. note::

   Here's a copy-paste ready command for you to use directly with zero
   configuration:

   .. code:: console

      ssh \
            -L 8888:localhost:8888 \
            -L 5000:localhost:5000 \
            -o ServerAliveInterval=120 \
            -X -C \
            max@IP_ADDRESS

.. note::

   On MacOS you need to install `XQuartz <https://xquartz.macosforge.org/landing/>`_
   in order to use X-forwarding.

Windows
~~~~~~~

If you're running Windows 10, you may want to consider `installing the Windows Subsystem for Linux <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`_ (and then follow the instructions above). Alternatively:

-  Install the `PuTTY SSH client <https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html>`_.

-  Run PuTTY

   -  Put the given IP address as hostname, type ``aiidatutorial`` in "Saved Sessions"
      and click "Save".
   -  Go to Connection > Data and put ``max`` as autologin username.
   -  Go to Connection > SSH > Tunnels, type ``8888`` in the
      "Source Port" box, type ``localhost:8888`` in "Destination" and click "Add".
   -  Repeat the previous step for port ``5000`` instead of ``8888``.
   -  Go back to the "Session" screen, select "aiidatutorial" and click "Save"
   -  Finally, click "Open" (and click "Yes" on the putty security alert
      to add the VM to your known hosts).
      You should be redirected to a bash terminal on the virtual machine.

.. note::
    Next time you open PuTTY, select ``aiidatutorial`` and click "Load"
    before clicking "Open".


In order to enable X-forwarding:

-  Install the `Xming X Server for Windows <http://sourceforge.net/projects/xming/>`_.

-  Configure PuTTy as described in the `Xming wiki <https://wiki.centos.org/HowTos/Xming>`_.

.. _2019_xmn_setup_jupyter:

Start jupyter
-------------

Once connected to your virtual machine, type in the remote terminal

.. code:: bash

     workon aiida

This will enable the virtual environment in which AiiDA is installed,
allowing you to use AiiDA. Now type in the same shell:

.. code:: bash

     jupyter notebook --no-browser

This will run a server with a web application called ``jupyter``, which
is used to create interactive python notebooks.
In order to connect to the jupyter notebook server:

 - copy the URL that has been printed to the terminal (similar to ``http://localhost:8888/?token=2a3ba37cd1...``)
 - open a web browser **on your laptop** and paste the URL
 - You will see a list of folders on your personal VM.

While keeping the first ``ssh`` connection running, open another ``ssh``
connection in a second terminal and type ``workon aiida`` here too. This
terminal is the one we will actually use in this tutorial.

.. note::

   Our SSH configuration assumes that ``jupyter`` will serve the notebooks on port 8888.
   If you want to serve notebooks on different ports, you'll also need to adjust
   the SSH configuration.


.. _2019_xmn_setup_downloading_files:

Downloading files
-----------------

Throughout this tutorial, you will encounter links to download python scripts, jupyter notebooks and more.
These files should be downloaded to the environment/working directory you use to run the tutorial.
In particular, when running the tutorial on a linux virtual machine, copy the link address and download the files to the machine using the ``wget`` utility on the terminal:

   wget <LINK>

where you replace ``<LINK>`` with the actual HTTPS link that you copied from the tutorial text in your browser.
This will download that file in your current directory.


Troubleshooting
---------------

-  If you get errors ``ImportError: No module named aiida`` or
   ``No command ’verdi’ found``, double check that you have loaded the
   virtual environment with ``workon aiida`` before launching ``python``,
   ``ipython`` or the ``jupyter`` notebook server.

-  If your browser cannot connect to the jupyter notebook server, check that
   you have correctly configured SSH tunneling/forwarding as described
   above. Keep in mind that you need to start the jupyter server from the
   terminal connected to the VM, while the web browser should be opened locally
   on your laptop.

-  See the `jupyter notebook documentation <https://jupyter-notebook.readthedocs.io/en/stable/notebook.html#browser-compatibility>`_ for compatibility of jupyter with various web browsers.

Getting help
------------

There are a number of helpful resources available to you for getting more information about AiiDA.
Please consider:

 * consulting the extensive `AiiDA documentation <https://aiida-core.readthedocs.io/en/latest/>`_
 * asking in the `Slack channel of the tutorial <https://dwz.cn/WPIahDr5>`_
 * opening a new issue on the `tutorial issue tracker <https://github.com/aiidateam/aiida-tutorials/issues>`_
 * asking your neighbor
 * asking a tutor
