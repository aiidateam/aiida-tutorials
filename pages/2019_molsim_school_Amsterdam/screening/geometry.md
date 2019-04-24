Perform geometric analysis of one MOF
=====================================

Use the [zeo++](http://www.zeoplusplus.org/) code to analyze the
structure, such as the volume inside the MOF that is accessible to
methane.

    -   Generate an SSH key pair for passwordless connection

        ```terminal
        $ ssh-keygen

        Generating public/private rsa key pair. 
        Enter file in which to save the key (/home/max/.ssh/id_rsa): <Enter> 
        Enter passphrase (empty for no passphrase): <Enter> 
        Enter same passphrase again: <Enter> 
        Your identification has been savedin /home/max/.ssh/id_rsa. 
        Your public key has been saved in /home/max/.ssh/id_rsa.pub. 
        The key fingerprint is: ... 
        The key's randomart image is: ... 
        ```

        ```terminal
        $ ssh-copy-id <user>@deneb1.epfl.ch 
        $ ssh <user>@deneb1.epfl.ch  # should now work without password
        ```

-   Compute the density, accessible volume and [accessible surface
    area](https://en.wikipedia.org/wiki/Accessible_surface_area) using
    zeo++.

    Use the [zeo++ web site](http://www.zeoplusplus.org/examples.html)
    to figure out what the `-ha`, `-res`, `-sa`, `-volpo` command line
    options do.

    What is an appropriate value for the probe radius `r`?

    ```python
    code = Code.get_from_string("zeopp@deneb-molsim") 
    calc = code.new_calc()

    # computational resources for calculation 
    calc.set_withmpi(False)
    calc.set_resources( {"num_machines": 1, "tot_num_mpiprocs":} )
    calc.set_max_wallclock_seconds(30*60) \# 30 minutes
    calc.set_max_memory_kb(2e6)

    # zeo++ command line parameters
    NetworkParameters = DataFactory('zeopp.parameters') d={
        'ha': True,
        'res': True,
        'sa': [<r (Angstrom)>, <r (Angstrom)>, 1000], 
        'volpo': [<r (Angstrom)>, <r (Angstrom)>, 1000],
    }
    parameters = NetworkParameters(dict=d)
    calc.use_parameters(parameters)

    # Load the cif node from the database, e.g. by PK
    # cif = load_node(<PK>)
    calc.use_structure(cif)

    # This places files in a subfolder "submit_test" instead of submitting.
    calc.submit_test()
    # Uncomment lines below when the script runs through
    # calc.store_all()
    # calc.submit()
    # print(calc)  # prints UUID and PK
    ```


**Remember:** Use `verdi run <script.py>` to run python scripts in the
same environment as in the `verdi shell`.
