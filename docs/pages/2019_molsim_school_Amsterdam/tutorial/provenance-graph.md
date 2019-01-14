Browsing the provenance graph
=============================

Before we start creating data ourselves, we are going to look at an
AiiDA database already created by someone else. Let’s import one from the web:

```terminal
$ verdi import https://www.dropbox.com/s/9xzpzb3mzg16jqy/mof_database.aiida?dl=1
```

Contrary to most databases, AiiDA databases contain not only results of
calculations but also their inputs and information on how a particular
result was obtained.
This information (provenance) is stored in the form of a directed acyclic graph (DAG).
 (provenance).

In the following, we are going to introduce you to different ways of browsing this graph
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

Now we can [connect our REST API](http://34.244.178.26:5001/explore/connect) to the 
provenance explorer by providing the (local) URL 
`http://127.0.0.1:5000/api/v2` of our REST API.

> **Note**  
> The provenance browser is also [available on Materials Cloud](https://www.materialscloud.org/explore/connect) but we are using a more recent development version.

Once the provenance explorer has been loaded by your browser, it is communicating directly with the
REST API and your data never leaves your computer.

Start by clicking on the Details of a `NetworkCalculation` node
(if you ever get lost, [here](http://34.244.178.26:5001/explore/ownrestapi/details/5a92d1e2-e243-4386-8ba1-e6c540e93b20?nodeType=CALCULATION) 
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
