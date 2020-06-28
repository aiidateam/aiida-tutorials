Queries in AiiDA: The QueryBuilder {#sec:querybuilder}
==================================

In this part of the tutorial we will focus on how to query our database
using a querying tool for AiiDA called the *QueryBuilder*. Queries are,
very loosely defined, questions to your database. We will first show you
some simple examples and tasks on how to explore your database. Then we
will proceed to a more concrete exercise on the screening of magnetic
and metallic perovskites.\

Task 1 - Introduction to QueryBuilder
-------------------------------------

| Node & subclasses |  Number in DB
|-------------------| --------------
|       Node        |      4707
|   StructureData   |      621
|   ParameterData   |      1338
|    KpointsData    |      861
|      UpfData      |       99
|  JobCalculation   |      448

  : List of some Node subclasses and how many times they occur in our
  test database.

[fig.types]

In this task we will use the QueryBuilder to do some basic queries and
understand our database. As a first step we should import our querying
tool, the *QueryBuilder*.

from aiida.orm.querybuilder import QueryBuilder

After the above import, we create our first query. To do so, we will
have to instantiate a QueryBuilder instance:

```python
qb = QueryBuilder()
```

Our query is still empty, we have not yet defined what we want to see.
For example, we will ask for all the nodes of our database. This is as
simple as appending the Node class to the query that we construct.

```python
qb.append(Node)
```

At this point, we can finish our query by asking back all nodes and by
typing

```python
qb.all() # Returns all nodes in the database
```

However, this command will return us all the Nodes directly, which may
not be the most wise thing to do considering that is the biggest family
of AiiDA stored objects that we can query. To understand the size of the
result, we can type the following command:

```python
qb.count() # Returns an integer, the number of nodes in the database
```

If you are interested to retrieve a subclass of a node, append that
specific subclass instead of Node:

```python
CifData = DataFactory('cif')
qb = QueryBuilder() # Creating a new QueryBuilder instance
qb.append(CifData) # Telling the QueryBuilder instance that I want a cif data type
qb.all() # Asking for all the results!
```

**Exercise:**

- Try now to find the number of instances for some subclasses of Node
  (e.g. StructureData, ParameterData, etc.) that are stored in your
  database. The result should look like . Of course, the numbers can
  be different!

**Comment:** If you are familiar with the SQL (Structured Query
Language) syntax then you may wonder what the issued SQL command is.
This can be easily seen by typing:

```python
str(qb)
```

**Comment:** If you want to get inspired by the available QueryBuilder
options you can just press the *tab* key in an interactive shell (after
typing `qb.`) to see the available options.

**Comment:** After you run a query, a new `QueryBuilder` instance needs
to be defined if you want to make a new query.

Task 2 - Projections and filters
--------------------------------

|  Operator   |         Datatype         |               Example
|-------------| -------------------------| ------------------------------------
|     ==      |            All           |              {'==':12}
|     in      |            All           |    {'in':['FINISHED', 'PARSING']}
| >,<,<=,>= |  floats, integers, dates |             {'>':5.2}
|    like     |           Chars          |       {'like':'calculation%'}
|    ilike    |           Chars          |       {'ilike':'caLculAtioN%'}
|     or      |                          |  {'or':[{'<':5.3}, {'>':6.3}]}
|     and     |                          |  {'and':[{'>':5.3}, {'<':6.3}]}

  : Operators currently implemented for all backends.

[tab.filterops]

In database language performing a projection means to extract one or
more specific columns from a table. In the AiiDA language this is
equivalent to say that we select what properties a query should return
out of the queried objects. For example, we might be interested only in
the id of a set of nodes (or their creation date, or any stored value).
To this purpose we should suitably instruct a QueryBuilder object by
means of the "project" key. For example, if we would like to get all the
ids of the nodes, we would type the following:

```python
qb = QueryBuilder() qb.append(Node, project=["id"]) qb.all()
```

|---------| -------------------------|
|Entity   | Properties               |
|---------| -------------------------|
|Node     | id, uuid, type, label, description, ctime, mtime|
|Computer | id, uuid, name, hostname, description, enabled, transport_type, scheduler_type|
|User     | id, email, first_name, last_name, institution|
|Group    | id, uuid, name, type, time, description|
|---------| -------------------------|

  : A selection of entities and some of their properties.

[tab.properties]

Please note that if you would like to perform an operation on the *pk*
of a node, you should use the keyword *id* in QueryBuilder queries.

Most likely, performing a query implies to select only those elements
that fulfill certain criteria. For example, we might want to select all
the calculations that were launched on a specific date. In database
language, this is called "adding a filter" to a query. A filter is a
boolean operator that returns True or False. lists all operators that we
implemented. A selection of entities and some of their properties that
you can use at your projections and filters can be found at table .

If you want to add filters to your query, you simply add the *filters*
keyword with a dictionary. Suppose you want to know the creation date of
a structure of which you know the uuid:

```python
qb = QueryBuilder() # Instantiating a new QueryBuilder
qb.append(CifData, # I want structures!
  project=["ctime"], # I'm interested in creation time!
  filters={"uuid": {"==":"b84e8d4c-908b-45b4-8015-3ace540f7dd6"}}
)  # I want the structure with this UUID
qb.all()
```

Try it out! There is also the possibility to combine multiple filters on
the same object using the "and" or the "or" keyword in the filter
section. Let's see an example.

```python
from datetime import datetime, timedelta
qb = QueryBuilder()
qb.append(CifData,
  project=["uuid"],   # I want to see only the UUID
  filters={ "or":[    # First filter is an or statement
            { "ctime": {">":datetime.now() - timedelta(days=12) }},
            { "label": "Raspa test" }
           ]}
)
qb.all()
```

In the above example we added an "or" keyword between the two filters.
The query return every structure in the database that was created in the
last 12 days or is named "graphene".

**Hints for the exercises:**

- The operator '>', '<' works with date-type properties with the expected behavior.

- For your date comparisons you will need to create a `datetime`
  object to which you can assign a date of your preference. You will
  have to do the necessary import (`from datetime import datetime`)
  and create an object by giving a specific date. E.g.
  `datetime(2015, 12, 26)`. For further information, you can consult the Python's
  online documentation.

**Exercises:**

- Write a query that returns all instances of StructureData that have been created after the 1st of January 2016.

- Write a query that returns all instances of Group whose name starts with "tutorial".
