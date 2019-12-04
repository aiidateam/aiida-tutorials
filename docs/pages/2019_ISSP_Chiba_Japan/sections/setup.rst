Getting set up
==============

.. _2019_chiba_connect:

Connect to your virtual machine
-------------------------------

The steps below explain how to connect to your personal `Quantum
Mobile <https://materialscloud.org/work/quantum-mobile>`_ virtual
machine (VM) on virtualbox using the `Secure Shell
<http://en.wikipedia.org/wiki/Secure_Shell>`_ protocol. The software
on this VM already includes a pre-configured AiiDA installation as
well as some test data for the tutorial.

Linux and MacOS
~~~~~~~~~~~~~~~

It's recommended for you to place the ssh key you will create in a
folder dedicated to your ssh configuration, to do so:

-  If not already present, create a ``.ssh`` directory in your home
   (``mkdir ~/.ssh``), and set its permissions: ``chmod 700 ~/.ssh``
-  Generate private and pubilc ssh key pair by ``ssh-keygen -f
   aiida_tutorial``.
-  Copy the public key to VM by ``ssh-copy-id -i
   ~/.ssh/aiida-tutorial.pub max@127.0.0.1 -p 2222`` and type the
   default password ``moritz``.

After the ssh key files are in place, add the following block to your
``~/.ssh/config`` file:

.. code:: bash

   Host aiidatutorial
      Hostname 127.0.0.1
      Port 2222
      User max
      IdentityFile ~/.ssh/aiida_tutorial
      ForwardX11 yes
      ForwardX11Trusted yes
      LocalForward 8888 localhost:8888
      LocalForward 5000 localhost:5000
      ServerAliveInterval 120

Afterwards you can connect to VM using this simple command:

.. code:: console

   ssh aiidatutorial

.. note::

   Here's a copy-paste ready command for you to use directly with zero
   configuration:

   .. code:: console

      ssh \
            -i ~/.ssh/aiida-tutorial \
            -L 8888:localhost:8888 \
            -L 5000:localhost:5000 \
            -o ServerAliveInterval=120 \
            -X -C \
            max@127.0.0.1 -p 2222

.. note::

   On MacOS you need to install `XQuartz
   <https://xquartz.macosforge.org/landing/>`_ in order to use
   X-forwarding.

Windows
~~~~~~~

If you're running Windows 10, you should consider `installing the
Windows Subsystem for Linux
<https://docs.microsoft.com/en-us/windows/wsl/install-win10>`_ (and
then follow the instructions above for linux).

Alternatively:

-  Install the `PuTTY SSH client
   <https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html>`_.
   PuTTY, PuTTYGen, and Pageant are included in the package or
   individually downloaded from this web page.

-  Run PuTTYGen

   -  Generate private and public key pair ``aiida_tutorial``.

-  Run Pageant

   -  It will add a new icon near the clock, in the bottom right of your screen.
   -  Right click on this Pageant icon, and click on “View Keys”.
   -  Click on "Add key" and select the ``aiida_tutorial`` you
      generated a few steps above.

-  Run PuTTY

   -  Put the given IP address as hostname, type ``aiidatutorial`` in
      "Saved Sessions" and click "Save".
   -  Go to Connection > Data and put ``max`` as autologin username.
   -  Go to Connection > SSH > Tunnels, type ``8888`` in the "Source
      Port" box, type ``localhost:8888`` in "Destination" and click
      "Add".
   -  Repeat the previous step for port ``5000`` instead of ``8888``.
   -  Go back to the "Session" screen, select "aiidatutorial" and click
      "Save".
   -  Finally, click "Open" (and click "Yes" on the putty security
      alert to add the VM to your known hosts).  You should be
      redirected to a bash terminal on the virtual machine.

.. note:: Next time you open PuTTY, select ``aiidatutorial`` and click
          "Load" before clicking "Open".

In order to enable X-forwarding:

-  Install the `Xming X Server for Windows
   <http://sourceforge.net/projects/xming/>`_.

-  Configure PuTTy as described in the `Xming wiki
   <https://wiki.centos.org/HowTos/Xming>`_.

.. _2019_chiba_setup_jupyter:

Start jupyter
-------------

Once connected to your virtual machine, type in the remote terminal

.. code:: bash

   workon aiida

This will enable the virtual environment in which AiiDA is installed,
allowing you to use AiiDA.  Now type in the same shell:

.. code:: bash

   jupyter notebook --no-browser

This will run a server with a web application called ``jupyter``,
which is used to create interactive python notebooks.  In order to
connect to the jupyter notebook server:

 - Copy the URL that has been printed to the terminal (similar to
   ``http://localhost:8888/?token=2a3ba37cd1...``).
 - Open a web browser **on your laptop** and paste the URL.
 - You will see a list of folders on your personal VM.

While keeping the first ``ssh`` connection running, open a second
``ssh`` connection in a separate terminal and execute ``workon aiida``
there as well.  We will use the second terminal to directly interact
with the virtual machine on the command line, while we use the first
one to only serve the jupyter notebook.

.. note::

    You can safely ignore all warnings related to port forwarding when
    opening a second ssh connection.  Those are caused by the fact
    that the ports are now already in use which in this context is
    perfectly fine.


.. _2019_chiba_setup_downloading_files:

Downloading files
-----------------

Throughout this tutorial, you will encounter links to download python
scripts, jupyter notebooks and more. These files should be downloaded
to the environment/working directory you use to run the tutorial.  In
particular, when running the tutorial on a Linux VM, copy the link
address and download the files to the machine using ``wget`` in the
terminal:

.. code:: bash

   wget <URL>

where you replace ``<URL>`` with the actual HTTPS URL copied from the
tutorial text in your browser.  This will download the file to the
current directory.


Troubleshooting
---------------

-  If you encounter errors such as ``ImportError: No module named
   aiida`` or ``No command ’verdi’ found``, double check that you
   have loaded the virtual environment with ``workon aiida`` before
   launching ``python``, ``ipython`` or the ``jupyter`` notebook
   server.  Your command line prompt should start with ``(aiida)``,
   e.g., ``(aiida) max@workhorse:~$``.

-  If your browser cannot connect to the jupyter notebook server, check
   that you have correctly configured SSH tunneling/forwarding as
   described above.  Keep in mind that you need to start the jupyter
   server from the terminal connected to the VM, while the web browser
   should be opened locally on your laptop.

-  See the `jupyter notebook documentation
   <https://jupyter-notebook.readthedocs.io/en/stable/notebook.html#browser-compatibility>`_
   for compatibility of jupyter with various web browsers.
