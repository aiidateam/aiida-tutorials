(matsci-pseudos)=

# Pseudopotentials

From the graph you generated in section (**TODO FIX LINK**), find the UUID of the pseudopotential file (LDA).
Load it and show what elements it corresponds to by typing:

```{code-block} ipython

In [1]: upf = load_node('<UUID>')
   ...: upf.element

```

All methods of `UpfData` are accessible by typing `upf.` and then pressing `TAB`.

Pseudopotentials in AiiDA are grouped in 'families' that contain one single pseudo per element.
We will see how to work with UPF pseudopotentials (the format used by Quantum ESPRESSO and some other codes).
Download and untar the SSSP pseudopotentials via the commands:

```{code-block} console

$ mkdir sssp_pseudos
$ wget 'https://archive.materialscloud.org/record/file?filename=SSSP_1.1_PBE_efficiency.tar.gz&record_id=23&file_id=d2ce4186-bf76-4e05-8b39-444b4da30273' -O SSSP_1.1_PBE_efficiency.tar.gz
$ tar -C sssp_pseudos -zxvf SSSP_1.1_PBE_efficiency.tar.gz

```

Then you can upload the whole set of pseudopotentials to AiiDA by using the following `verdi` command:

```{code-block} console

$ verdi data upf uploadfamily sssp_pseudos 'SSSP' 'SSSP pseudopotential library'

```

In the command above, `sssp_pseudos` is the folder containing the pseudopotentials, `'SSSP'` is the label given to the family, and the last argument is its description.
Finally, you can list all the pseudo families present in the database with

```{code-block} console

$ verdi data upf listfamilies

```
