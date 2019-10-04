Getting set up
==============

.. note:: If you are using the Quantum Mobile virtual machine locally inside VirtualBox, you can skip this section.

.. _2019_mandi_connect:

Connect to your virtual machine
-------------------------------

You should each have received from the instructors:

- an IP address
- a private SSH key ``aiida_tutorial_NUM``
- a public SSH key ``aiida_tutorial_NUM.pub``

The steps below explain how to use these in order to connect to your personal virtual machine (VM) on Amazon Elastic Cloud 2 using the `Secure Shell <http://en.wikipedia.org/wiki/Secure_Shell>`_ protocol.
The software on this VM is based on `Quantum Mobile <https://materialscloud.org/work/quantum-mobile>`_ and already includes a pre-configured AiiDA installation as well as some test data for the tutorial.

.. note::

   If you decide to work in pairs, one of you should forward their credentials to the other, and you should both use the same IP address and ssh key.
   Since you will be sharing the VM and user account, be careful not to delete the work of your colleague.

Linux and MacOS
~~~~~~~~~~~~~~~

It's recommended for you to place the ssh key you received in a folder dedicated to your ssh configuration, to do so:

-  If not already present, create a ``.ssh`` directory in your home (``mkdir ~/.ssh``), and set its permissions: ``chmod 700 ~/.ssh``
-  Copy the two keys ``aiida_tutorial_NUM`` and ``aiida_tutorial_NUM.pub``
   in the ``~/.ssh`` directory
-  Set the correct permissions on the private key:
   ``chmod 600 ~/.ssh/aiida_tutorial_NUM``. You can check check with ``ls -l``
   that the permissions of this file are now ``-rw-------``.

After that ssh key is in place, you can add the following block your ``~/.ssh/config`` file:

.. code:: bash

   Host aiidatutorial
      Hostname IP_ADDRESS
      User max
      IdentityFile ~/.ssh/aiida_tutorial_NUM
      ForwardX11 yes
      ForwardX11Trusted yes
      LocalForward 8888 localhost:8888
      LocalForward 5000 localhost:5000
      ServerAliveInterval 120

replacing the IP address (``IP_ADDRESS``) and the ``NUM`` by the one you received.

Afterwards you can connect to the server using this simple command:

.. code:: console

   ssh aiidatutorial

.. note::

   Here's a copy-paste ready command for you to use directly with zero configuration:

   .. code:: console

      ssh \
            -i ~/.ssh/aiida-tutorial-max.pem \
            -L 8888:localhost:8888 \
            -L 5000:localhost:5000 \
            -o ServerAliveInterval=120 \
            -X -C \
            max@IP_ADDRESS

.. note::

   On MacOS you need to install `XQuartz <https://xquartz.macosforge.org/landing/>`_ in order to use X-forwarding.

Windows
~~~~~~~

If you're running Windows 10, you may want to consider `installing the Windows Subsystem for Linux <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`_ (and then follow the instructions above).
Alternatively:

-  Install the `PuTTY SSH client <https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html>`_.

-  Run PuTTYGen

   -  Load the ``aiida_tutorial_NN`` private key (button "Load").
      You may need to choose to show "All files (*.*)", and select the file without any extension (Type: File).
   -  In the same window, click on "Save private Key", and save the key with the name ``aiida_tutorial_NN.ppk`` (don't specify a password).

-  Run Pageant

   -  It will add a new icon near the clock, in the bottom right of your screen.
   -  Right click on this Pageant icon, and click on “View Keys”.
   -  Click on "Add key" and select the ``aiida_tutorial_NN.ppk`` you saved a few steps above.

-  Run PuTTY

   -  Put the given IP address as hostname, type ``aiidatutorial`` in "Saved Sessions" and click "Save".
   -  Go to Connection > Data and put ``max`` as autologin username.
   -  Go to Connection > SSH > Tunnels, type ``8888`` in the "Source Port" box, type ``localhost:8888`` in "Destination" and click "Add".
   -  Repeat the previous step for port ``5000`` instead of ``8888``.
   -  Go back to the "Session" screen, select "aiidatutorial" and click "Save".
   -  Finally, click "Open" (and click "Yes" on the putty security alert to add the VM to your known hosts).
      You should be redirected to a bash terminal on the virtual machine.

.. note:: Next time you open PuTTY, select ``aiidatutorial`` and click "Load" before clicking "Open".

In order to enable X-forwarding:

-  Install the `Xming X Server for Windows <http://sourceforge.net/projects/xming/>`_.

-  Configure PuTTy as described in the `Xming wiki <https://wiki.centos.org/HowTos/Xming>`_.

.. _2019_mandi_setup_jupyter:

Start jupyter
-------------

Once connected to your virtual machine, type in the remote terminal

.. code:: bash

   workon aiida

This will enable the virtual environment in which AiiDA is installed, allowing you to use AiiDA.
Now type in the same shell:

.. code:: bash

   jupyter notebook --no-browser

This will run a server with a web application called ``jupyter``, which is used to create interactive python notebooks.
In order to connect to the jupyter notebook server:

 - Copy the URL that has been printed to the terminal (similar to ``http://localhost:8888/?token=2a3ba37cd1...``).
 - Open a web browser **on your laptop** and paste the URL.
 - You will see a list of folders on your personal VM.

While keeping the first ``ssh`` connection running, open a second ``ssh`` connection in a separate terminal and execute ``workon aiida`` there as well.
We will use the second terminal to directly interact with the virtual machine on the command line, while we use the first one to only serve the jupyter notebook.


.. _2019_mandi_setup_downloading_files:

Downloading files
-----------------

Throughout this tutorial, you will encounter links to download python scripts, jupyter notebooks and more.
These files should be downloaded to the environment/working directory you use to run the tutorial.
In particular, when running the tutorial on a Linux VM, copy the link address and download the files to the machine using ``wget`` in the terminal:

.. code:: bash

   wget <LINK>

where you replace ``<LINK>`` with the actual HTTPS link copied from the tutorial text in your browser.
This will download the file in your current directory.


Troubleshooting
---------------

-  If you get errors ``ImportError: No module named aiida`` or ``No command ’verdi’ found``, double check that you have loaded the virtual environment with ``workon aiida`` before launching ``python``, ``ipython`` or the ``jupyter`` notebook server.

-  If your browser cannot connect to the jupyter notebook server, check that you have correctly configured SSH tunneling/forwarding as described above.
   Keep in mind that you need to start the jupyter server from the terminal connected to the VM, while the web browser should be opened locally on your laptop.

-  See the `jupyter notebook documentation <https://jupyter-notebook.readthedocs.io/en/stable/notebook.html#browser-compatibility>`_ for compatibility of jupyter with various web browsers.
