Browsing the provenance graph
=============================

Before we start creating data ourselves, we are going to look at an
AiiDA database already created by someone else. Let’s import one from the web:

```terminal
$ verdi import https://www.dropbox.com/s/3f4895jq9eskqw3/export.aiida?dl=1
```

While the database (90 MB) is importing, let's recall a few things:
Contrary to most databases, AiiDA databases contain not only results of
calculations but also their inputs and information on how a particular
result was obtained.
This information (provenance) is stored in the form of a directed acyclic graph (DAG).
 (provenance).

In the following, we are going to introduce different ways of browsing this graph
and ask you find out some information regarding the database you just imported.

The EXPLORE interface
---------------------

The most intuitive way to browse AiiDA graphs is to use the interactive provenance
explorer available on [Materials Cloud](www.materialscloud.org).

For it to work, we first need to start the AiiDA REST API:

```terminal
$ verdi restapi
 * Serving Flask app "aiida.restapi.run_api" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Now we can [connect our REST API](www.materialscloud.org/explore/connect) to the 
provenance explorer by providing the (local) URL 
`http://127.0.0.1:5000/api/v2` of our REST API.

> **Note**  
> Once the provenance explorer has been loaded by your browser, it is communicating directly with the
> REST API and your data never leaves your computer.

Start by clicking on the Details of a `RaspaCalculation` node
(if you ever get lost, [here](https://www.materialscloud.org/explore/ownrestapi/details/66dc9791-27e5-411b-b414-5224023f8ee1?nodeType=CALCULATION) 
is a link to one).

---
### Exercise

Use the graph explorer in order to figure out:

 * What code was used and what was the name of the executable?
 * When was the calculation run and who run it?
 * How much memory was requested for the calculation?
 * What inputs did the calculation take?
 * What other types of calculation was the `Cif` input structure used in?

---
