Getting set up
==============

.. _connect:

Connect to your virtual machine
-------------------------------

You should each have received from the instructors:

-  an IP address
-  a private SSH key ``aiida_tutorial_NUM``
-  a public SSH key ``aiida_tutorial_NUM.pub``

The steps below explain how to use these in order to connect to your
personal virtual machine (VM) on Amazon Elastic Cloud 2
using the `Secure Shell <http://en.wikipedia.org/wiki/Secure_Shell>`_ protocol.
The software on this VM is based on `Quantum Mobile
<https://materialscloud.org/work/quantum-mobile>`_ and already includes a
pre-configured AiiDA installation as well as some test data for the tutorial.

.. note::

   If you decide to work in pairs, one of you should forward their credentials
   to the other and you should both use the same IP address and ssh key.
   Since you will be sharing the VM and user account, be careful not to delete
   the work of your colleague.

Linux and MacOS
~~~~~~~~~~~~~~~

-  If not already present, create a ``.ssh`` directory in your home
   (``mkdir ~/.ssh``), and set its permissions: ``chmod 700 ~/.ssh``

-  Copy the two keys ``aiida_tutorial_NUM`` and ``aiida_tutorial_NUM.pub``
   in the ``~/.ssh`` directory

-  Set the correct permissions on the private key:
   ``chmod 600 ~/.ssh/aiida_tutorial_NUM``.
   You can check check with ``ls -l`` that the permissions of this file are now ``-rw-------``.

-  Create (or modify) the ``~/.ssh/config`` file, adding the following lines:

   .. code:: console

       Host aiidatutorial
         Hostname IP_ADDRESS
         User aiida
         IdentityFile ~/.ssh/aiida_tutorial_NUM
         ForwardX11 yes
         ForwardX11Trusted yes
         LocalForward 8888 localhost:8888

   where you replace ``IP_ADDRESS`` with the IP address provided to you.

-  You should now be able to ``ssh`` to your virtual machine using simply

   .. code:: console

         ssh -X -C aiidatutorial


Connecting with ``-X`` (sometimes ``-Y`` is needed instead) allows you
to run graphical programs such as ``xmgrace`` or ``gnuplot`` on the virtual machine,
with SSH *forwarding* the graphical output to your computer (can be slow).

.. note::

   On MacOS you may need to install `XQuartz <https://xquartz.macosforge.org/landing/>`_
   in order to use X-forwarding.

Windows
~~~~~~~

If you're running Windows 10, you may want to consider `installing the Windows Subsystem for Linux <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`_ (and then follow the instructions above). Alternatively:

-  Install the `PuTTY SSH client <https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html>`_.

-  Run PuTTYGen, load the ``aiida_tutorial_NN`` private key (button
   ``"Load"``). You may need to choose to show “All files (\*.\*)”,
   and select the file without any extension (Type: File).

-  In the same window, click on “Save private Key”, and save the key
   with the name ``aiida_tutorial_NN.ppk``.

-  Run Pageant: it will add a new icon near the clock, in the bottom
   right of your screen.

-  Right click on this Pageant icon, and click on “View Keys”.

-  Click on ``"Add key"`` and select the ``aiida_tutorial_NN.ppk`` you
   saved a few steps above.

-  Run PuTTY, put the given IP address as hostname. Write
   ``aiidatutorial`` in Saved Sessions and click ``Save``. Go to
   Connection Data and put ``aiida`` as autologin username. Under
   Connection, go to SSH Tunnels, type ``8888`` in the
   ``Source Port`` box and ``localhost:8888`` in ``Destination`` and
   click ``Add``. Click on ``Save`` again on the Session screen.

-  Now select ``aiidatutorial`` from the session list, click ``Load``
   and, finally, ``open``.


In order to enable X-forwarding:

-  Install the `Xming X Server for Windows <http://sourceforge.net/projects/xming/>`_.

-  Configure PuTTy as described in the `Xming wiki <https://wiki.centos.org/HowTos/Xming>`_.

.. _setup_jupyter:

Start jupyter
-------------

Once connected to your virtual machine, type in the remote terminal

.. code:: console

     workon aiida

This will enable the virtual environment in which AiiDA is installed,
allowing you to use AiiDA. Now type in the same shell:

.. code:: console

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


.. _setup_downloading_files:

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
 * asking in the `Slack channel of the tutorial <https://aiidaworkflows2019.slack.com>`_
 * opening a new issue on the `tutorial issue tracker <https://github.com/aiidateam/aiida-tutorials/issues>`_
 * asking your neighbor
 * asking a tutor
