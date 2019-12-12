Getting set up
==============

.. _2019_chiba_connect:


Choice of web browser
---------------------

During the use of AiIDA infrastructure, we sometimes or often use web
browser. The recommended browser is Chrome or Firefox. Safari on macOS
is not recommended.


Connect to your virtual machine
-------------------------------

The steps below explain how to connect to your personal `Quantum
Mobile <https://materialscloud.org/work/quantum-mobile>`_ virtual
machine (VM) on virtualbox using the `Secure Shell
<http://en.wikipedia.org/wiki/Secure_Shell>`_ protocol. The software
on this VM already includes a pre-configured AiiDA installation as
well as some test data for the tutorial.
It's recommended for you to place the ssh key you will create in a
folder dedicated to your ssh configuration, to do so:

-  If not already present, create a ``.ssh`` directory in your home
   (``mkdir ~/.ssh``), and set its permissions: ``chmod 700 ~/.ssh``
-  Generate private and pubilc ssh key pair by ``ssh-keygen -f
   aiida_tutorial``.
-  Copy the public key to VM by ``ssh-copy-id -i
   ~/.ssh/aiida-tutorial.pub max@127.0.0.1 -p 2222`` and type the
   default password ``moritz``.


Linux and MacOS
~~~~~~~~~~~~~~~

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

Windows 10
~~~~~~~~~~

If you're running Windows 10, it is recommended to consider
`installing the Windows Subsystem for Linux (WSL)
<https://docs.microsoft.com/en-us/windows/wsl/install-win10>`_ (and
then follow the instructions above for linux). `VcXsrv
<https://sourceforge.net/projects/vcxsrv/>`_ is also installed with
WSL in order to use X-forwarding. Some WSL setup (networking and
X-forwarding) is written `here
<https://atztogo.github.io/AiiDA-tutorial-ISSP/windows-WSL-setup.html>`_.
Short summary of the configuration is as follows. After the ssh key
files are in place, add the following block to your ``~/.ssh/config``
file:

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
      RemoteForward 6010 localhost:6000
      ServerAliveInterval 120

``RemoteForward`` is for X-forwarding with VcXsrv. In this
configuration, in WSL

.. code:: bash

   $ echo 'export DISPLAY=:0.0' >> ~/.bashrc

and in Quantum Mobile VM

.. code:: bash

   $ echo 'export DISPLAY=:10.0' >> ~/.bashrc

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
