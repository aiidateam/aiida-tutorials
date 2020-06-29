---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.9'
    jupytext_version: 1.5.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
language_info:
  file_extension: ".py"
  name: "python"
---

# AiiDA's QueryBuilder

```{important}
Make sure to execute the cell below this one (it may be hidden)
```

```{code-cell} ipython3
:tags: [hide-input]

from IPython.display import Image
from datetime import datetime, timedelta
import numpy as np
from aiida import load_profile
from matplotlib import gridspec, pyplot as plt
load_profile()
from aiida.orm import load_node, Node, Group, Computer, User, CalcJobNode, Code
from aiida.plugins import CalculationFactory, DataFactory

PwCalculation = CalculationFactory('quantumespresso.pw')
StructureData = DataFactory('structure')
KpointsData = DataFactory('array.kpoints')
Dict = DataFactory('dict')
UpfData = DataFactory('upf')

def plot_results(query_res):
    """
    :param query_res: The result of an instance of the QueryBuilder
    """
    smearing_unit_set,magnetization_unit_set,pseudo_family_set = set(), set(), set()
    # Storing results:
    results_dict = {}
    for pseudo_family, formula, smearing, smearing_units, mag, mag_units in query_res:
        if formula not in results_dict:
            results_dict[formula] = {}
        # Storing the results:
        results_dict[formula][pseudo_family] = (smearing, mag)
        # Adding to the unit set:
        smearing_unit_set.add(smearing_units)
        magnetization_unit_set.add(mag_units)
        pseudo_family_set.add(pseudo_family)

    # Sorting by formula:
    sorted_results = sorted(results_dict.items())
    formula_list = next(zip(*sorted_results))
    nr_of_results = len(formula_list)

    # Checks that I have not more than 3 pseudo families.
    # If more are needed, define more colors
    #pseudo_list = list(pseudo_family_set)
    if len(pseudo_family_set) > 3:
        raise Exception('I was expecting 3 or less pseudo families')

    colors = ['b', 'r', 'g']

    # Plotting:
    plt.clf()
    fig=plt.figure(figsize=(16, 9), facecolor='w', edgecolor=None)
    gs  = gridspec.GridSpec(2,1, hspace=0.01, left=0.1, right=0.94)

    # Defining barwidth
    barwidth = 1. / (len(pseudo_family_set)+1)
    offset = [-0.5+(0.5+n)*barwidth for n in range(len(pseudo_family_set))]
    # Axing labels with units:
    yaxis = ("Smearing energy [{}]".format(smearing_unit_set.pop()),
        "Total magnetization [{}]".format(magnetization_unit_set.pop()))
    # If more than one unit was specified, I will exit:
    if smearing_unit_set:
        raise ValueError('Found different units for smearing')
    if magnetization_unit_set:
        raise ValueError('Found different units for magnetization')

    # Making two plots, the top one for the smearing, the bottom one for the magnetization
    for index in range(2):
        ax=fig.add_subplot(gs[index])
        for i,pseudo_family in enumerate(pseudo_family_set):
            X = np.arange(nr_of_results)+offset[i]
            Y = np.array([thisres[1][pseudo_family][index] for thisres in sorted_results])
            ax.bar(X, Y,  width=0.2, facecolor=colors[i], edgecolor=colors[i], label=pseudo_family)
        ax.set_ylabel(yaxis[index], fontsize=14, labelpad=15*index+5)
        ax.set_xlim(-0.5, nr_of_results-0.5)
        ax.set_xticks(np.arange(nr_of_results))
        if index == 0:
            plt.setp(ax.get_yticklabels()[0], visible=False)
            ax.xaxis.tick_top()
            ax.legend(loc=3, prop={'size': 18})
        else:
            plt.setp(ax.get_yticklabels()[-1], visible=False)
        for i in range(0, nr_of_results, 2):
            ax.axvspan(i-0.5, i+0.5, facecolor='y', alpha=0.2)
        ax.set_xticklabels(list(formula_list),rotation=90, size=14, ha='center')
    plt.show()

def generate_query_graph(qh, out_file_name):

    def draw_vertice_settings(idx, vertice, **kwargs):
        """
        Returns a string with all infos needed in a .dot file  to define a node of a graph.
        :param node:
        :param kwargs: Additional key-value pairs to be added to the returned string
        :return: a string
        """
        if vertice['entity_type'].startswith('process'):
            shape = "shape=polygon,sides=4"
        elif vertice['entity_type'].startswith('data.code'):
            shape = "shape=diamond"
        else:
            shape = "shape=ellipse"
        filters = kwargs.pop('filters', None)
        additional_string = ""
        if filters:
            additional_string += '\nFilters:'
            for k,v in filters.items():
                additional_string += "\n   {} : {}".format(k,v)


        label_string = " ('{}')".format(vertice['tag'])

        labelstring = 'label="{} {}{}"'.format(
            vertice['entity_type'], #.split('.')[-2] or 'Node',
            label_string,
            additional_string)
        #~ return "N{} [{},{}{}];".format(idx, shape, labelstring,
        return "{} [{},{}];".format(vertice['tag'], shape, labelstring)
    nodes = {v['tag']:draw_vertice_settings(idx, v, filters=qh['filters'][v['tag']]) for idx, v in enumerate(qh['path'])}
    links = [(v['tag'], v['joining_value'], v['joining_keyword']) for v in qh['path'][1:]]

    with open('temp.dot','w') as fout:
        fout.write("digraph G {\n")
        for l in links:
            fout.write('    {} -> {} [label=" {}"];\n'.format(*l))
        for _, n_values in nodes.items():
            fout.write("    {}\n".format(n_values))

        fout.write("}\n")
    import os
    os.system('dot temp.dot -Tpng -o {}'.format(out_file_name))

def store_formula_in_extra():
    from aiida.orm import QueryBuilder
    qb = QueryBuilder()
    qb.append(StructureData, filters={'extras':{'!has_key':'formula'}})
    for structure, in qb.all():
        structure.set_extra('formula', structure.get_formula(mode='count'))

store_formula_in_extra()
```

## Introduction to the QueryBuilder

As you will use `AiiDA` to run your calculations, the database that stores all the data and the provenance will quickly grow to be very large. To help you find the needle that you might be looking for in this big haystack, we need an efficient search tool. `AiiDA` provides a tool to do exactly this: the `QueryBuilder`. The `QueryBuilder` acts as the gatekeeper to your database, to whom you can ask questions about the contents of your database (also referred to as queries), by specifying what are looking for. In this part of the tutorial, we will focus on how to use the `QueryBuilder` to make these queries and understand/use the results.

In order to use the `QueryBuilder`, we first need to import it. We can accomplish this by executing the `import` statement in the following cell. Go ahead and select the next cell, and press `Shift+Enter`.

```{code-cell} ipython3
from aiida.orm import QueryBuilder
```

Before we can ask the `QueryBuilder` questions about our database, we first need to create an instance of it (i.e., we create a new query):

```{code-cell} ipython3
qb = QueryBuilder()
```

Now that we have an instance of our `QueryBuilder` which we named `qb`, we are ready to start asking about the content of our database. For example, we may want to know exactly how many nodes there are in our database. To tell `qb` that we are interested in all the occurrences of the `Node` class in our database, we `append` it to the list of objects it should find. 

*Note*: The method is called `append` because, as we will see later, you can append multiple nodes to a `QueryBuilder` instance consecutively to search in the graph, as if you had a list: what we are doing is querying a graph, and for every vertice of the graph in our subquery, we will use one `append` call. But we'll see this use better in a few steps.

```{code-cell} ipython3
qb.append(Node)
```

We have now narrowed down the scope of `qb` to just the nodes that are present in our database. To learn how many nodes there are exactly, all we have to do is to ask `qb` to count them.

```{code-cell} ipython3
qb.count()
```

Now as you may have learned in previous sections of the tutorial, nodes come in different kinds and flavors. For example, all our crystal structures that we have stored in the database are saved in nodes that are of the type `StructureData`. If instead of all the nodes, we would rather like to count only the crystal structure nodes, we simply tell our `QueryBuilder` to narrow its scope only to objects of type `StructureData`. Since we want to create a new independent query, we must create a new instance of the `QueryBuilder`. In the next cell, we have typed part of the code to count all the structure nodes. See if you can finish the line with the comment, to tell the `QueryBuilder` that you are only interested in `StructureData` nodes.

```{code-cell} ipython3
#TUT_USER_START
qb = QueryBuilder()
qb.append() # How do we finish this line to tell the query builder to count only the structure nodes?
qb.count()
#TUT_USER_END
#TUT_SOLUTION_START
qb = QueryBuilder()
qb.append(StructureData)
qb.count()
#TUT_SOLUTION_END
```

Instead of just counting how many structure nodes we have, we may also actually want to see some of them. This is as easy as telling our `QueryBuilder` that we are not interested in the `count` but rather that we want to retrieve `all` the nodes.

```{code-cell} ipython3
qb = QueryBuilder()
qb.append(StructureData)
qb.all()
```

Note that this command is very literal and does in fact retrieve **all** the structure nodes that are stored in your database, which may be very slow if your database becomes very large. One solution is to simply tell the `QueryBuilder` that we are, for example, only interested in 5 structure nodes. This can be done with the `limit` method as follows:

```{code-cell} ipython3
qb = QueryBuilder()
qb.append(StructureData)
qb.limit(5)
qb.all()
```

Another option is to simply use the concept of array slicing, native to python, to specify a subset of the total return set to be returned. Notice that this example can be very slow in big databases. When you want performance, use the functionality native to the QueryBuilder like `limit`, that limit the number of results directly at the database level!

```{code-cell} ipython3
qb.limit(None)
qb.all()[:7]
```

If we want to know a little bit more about the retrieved structure nodes, we can loop through our results. This allows you, for instance, to print the formula of the structures:

```{code-cell} ipython3
qb = QueryBuilder()
qb.append(StructureData)
qb.limit(5)
for structure, in qb.all():
    print(structure.get_formula())
```

This is just a simple example how we can employ the `QueryBuilder` to get details about the contents of our database. We have now seen simple queries for the `Node` and `StructureData` classes, but the same rules apply to all the `AiiDA` node classes. For example we may want to count the number of entries for each of the node classes in the following list:

```{code-cell} ipython3
class_list = [Node, StructureData, KpointsData, Dict, UpfData, Code]
```

Using the tools we have learned so far, we can build a table of the number of occurrences of each of these node classes that are stored in our database. We simply loop over the `class_list` and create a `QueryBuilder` for each and count the entries.

```{code-cell} ipython3
for class_name in class_list:
    qb = QueryBuilder()
    qb.append(class_name)
#TUT_USER_START
    print() # Finish this line to print the results!
#TUT_USER_END
#TUT_SOLUTION_START
    print('{:>15} | {:6}'.format(class_name.__name__, qb.count()))
#TUT_SOLUTION_END
```

If all went well, you should see something like the following, where of course the numbers may differ for your database

Class name     | Entries
---------------|--------
 Node          | 10273 
 StructureData | 271   
 KpointsData   | 953   
 Dict          | 2922  
 UpfData       | 85    
 Code          | 10

+++

## Projection and filters

Up until now we have always asked the `QueryBuilder` to return the node class. However, we might not necessarily be interested in all the node's properties, but rather just a selected set or even just a single property. We can tell the `QueryBuilder` which properties we would like to be returned, by asking it to **project** those properties in the result. For example, we may only want to get the `uuid`s of a set of nodes. 

```{code-cell} ipython3
qb = QueryBuilder()
qb.append(Node, project=['uuid'])
qb.limit(5)
qb.all()
```

By using the `project` keyword in the `append` call, we are informing the `QueryBuilder` that we are only interested in the `uuid` property of the `Node` class. Note that the value that we assign to `project` is a list, since we may want to specify more than one property. See if you can get the `QueryBuilder` to return *both* the `id` and the `uuid` of the first 5 `Node`s in the following cell.

```{note}
In the context of the QueryBuilder, the `id` is the `pk` of the node.
```

```{code-cell} ipython3
qb = QueryBuilder()
#TUT_USER_START
qb.append(Node, project=)#? What should the value be for the project key
#TUT_USER_END
#TUT_SOLUTION_START
qb.append(Node, project=['id', 'uuid'])
#TUT_SOLUTION_END
qb.limit(5)
qb.all()
```

To give you an idea of the various properties that you can project for some of the `AiiDA` node classes you can consult the following table.
Note that this is by no means an exhaustive list:

Class    | Properties
---------|-----------
Node     | `id`, `uuid`, `node_type`, `label`, `description`, `ctime`, `mtime`
Computer | `id`, `uuid`, `name`, `hostname`, `description`, `transport_type`, `scheduler_type`
User     | `id`, `email`, `first_name`, `last_name`, `institution`
Group    | `id`, `uuid`, `label`, `type_string`, `time`, `description`

+++

The same properties can also be used to *filter* for specific nodes in your database. Indeed, up until now, we only asked the `QueryBuilder` to return *all* the instances of a certain type of node, or at best a limited number of those (without specifying which ones). But in general we might be interested in a very specific node. For example, we may have the `id` of a certain node and we would like to know when it was created and last modified. We can tell the `QueryBuilder` to select nodes that only match that criterion, by telling it to **filter** based on that property.

```{code-cell} ipython3
qb = QueryBuilder()
qb.append(Node, project=['ctime', 'mtime'], filters={'id': {'==': 1}})
qb.all()
```

Note the syntax of the `filters` keyword. The value is a dictionary, where the keys indicate the node property that it is supposed to operate on, in this case the `id` property. The value of that key is again itself a dictionary, where the key indicates the logical operator `==` and the value corresponds to the value of the property.

You may have multiple criteria that you want to filter for, in which case you can use the logical `or` and `and` operators. Let's say, for example, that you want the `QueryBuilder` to retrieve all the `StructureData` nodes that have a certain `label` **and** were created no longer than 12 days ago. You can translate this criterion by making use of the `and` operator which allows you to specify multiple filters that all have to be satisfied.

```{code-cell} ipython3
qb = QueryBuilder()
qb.append(
    Node, 
    filters={
        'and': [
            {'ctime': {'>': datetime.now() - timedelta(days=12)}},
            {'label': {'==':'graphene'}}
        ]
    }
)
qb.all()
```

You will have noticed that the `>` operator, and its related operators, can work with python `datetime` objects. These are just a few of the operators that `QueryBuilder` understands. Below you find a table with some of the logical operators that you can use:

Operator             | Data type             | Example                            | Description
---------------------|-----------------------|------------------------------------|------------------
`==`                 | all                   | `{'==': '12'}`                     | equality operator
`in`                 | all                   | `{'in':['FINISHED', 'PARSING']}`   | member of a set
`<`, `>`, `<=`, `>=` | float, int, datetime  | `{'>': 5.2}`                       | size comparison operator
`like`               | char, str             | `{'like': 'calculation%'}`         | string comparison, `%` is wildcard
`ilike`              | char, str             | `{'ilike': 'caLCulAtion%'}`        | string comparison, capital insensitive
`or`                 |                       | `{'or': [{'<': 5.3}, {'>': 6.3}]}` | logical or operator
`and`                |                       | `{'and': [{'>=': 2}, {'<=': 6}]}`  | logical and operator

+++

As an exercise, try to write a query below that will retrieve all `Group` nodes whose `label` property starts with the string `tutorial`.

```{code-cell} ipython3
# Write your query here
#TUT_SOLUTION_START
qb = QueryBuilder()
qb.append(Group, filters={'label': {'like': 'tutorial%'}})
qb.limit(5)
qb.all()
#TUT_SOLUTION_END
```

## Defining relationships between query clauses

So far we have seen how we can use the `QueryBuilder` to search the database for entries of a specific node type, potentially projecting only specific properties and filtering for certain property values. However, our nodes do not live in a vacuum, but they are part of a graph and thus are linked one another. Therefore, we typically want to be able to search for nodes based on a certain relationship that they might have with other nodes. Consider for example that you have a `StructureData` node that was produced by some calculation. How would we be able to retrieve that calculation?

To accomplish this, we need to be able to tell the `QueryBuilder` what the relationship is between the nodes that we are interested in. With the `QueryBuilder`, we can do the following to find all the structure nodes that have been created as an output by a `PwCalculation` process.

```{important}
In the graph, we are not looking for a `PwCalculation` process (since processes do not live in the graph, as you have learnt). We are actually looking for a `CalcJobNode` whose `process_type` column indicates that it was run by a `PwCalculation` process. Since this is a very common pattern, the `QueryBuilder` allows to directly append the `PwCalculation` process class as a short-cut, but it internally unwraps this into a query for a `CalcJobNode` with the appropriate filter on the `process_type`.
```

```{code-cell} ipython3
qb = QueryBuilder()
qb.append(PwCalculation, tag='calculation')
```

Since we are looking for pairs of nodes, we need to `append` the second node as well to the `QueryBuilder` instance. In the next line, to specify the relationship between the nodes, we need to be able to reference back to the `CalcJobNode` that is matched by the previous clause: therefore, we give it a `tag` with the `tag` keyword.

```{code-cell} ipython3
qb.append(StructureData, with_incoming='calculation')
```

The goal was to find `StructureData` nodes, so we `append` that to the `qb`. However, we didn't want to find just any `StructureData` nodes; they had to be an output of `PwCalculation`.

Note how we expressed this relation by the `with_incoming` keyword, because we want a `StructureData` node having an *incoming* link from the `CalcJobNode` referenced by the `calculation` tag (i.e., the `StructureData` must be an *output* of the calculation).

Now all we have to do is execute the query to retrieve our structures:

```{code-cell} ipython3
qb.limit(5)
qb.all()
```

What we did can be visualized schematically, thanks to a little tool we have written for you.

```{code-cell} ipython3
generate_query_graph(qb.get_json_compatible_queryhelp(), 'query1.png')
Image(filename='query1.png')
```

The `with_incoming` keyword is only one of many potential relationships that exist between the various `AiiDA` nodes and that are implemented in the `QueryBuilder`. The table below gives an overview of the implemented relationships, which nodes they are defined for and what relation it implicates. The full documentation can be found [on this page of the AiiDA documentation](https://aiida-core.readthedocs.io/en/latest/querying/querybuilder/append.html#joining-entities).

+++

Entity from | Entity to | Relationship     | Explanation
------------|-----------|------------------|------------
Node        | Node      | with_outgoing    | One node as input of another node
Node        | Node      | with_incoming    | One node as output of another node
Node        | Node      | with_descendants | One node as the ancestor of another node
Node        | Node      | with_ancestors   | One node as descendant of another node
Group       | Node      | with_node        | The group of a node
Node        | Group     | with_group       | The node is a member of a group
Computer    | Node      | with_node        | The computer of a node
Node        | Computer  | with_computer    | The node of a computer
User        | Node      | with_node        | The creator of a node is a user
Node        | User      | with_user        | The node was created by a user

+++

As an exercise, see if you can write a query that will return all the `UpfData` nodes that are a member of a `Group` whose name starts with the string `SSSP`.

```{code-cell} ipython3
#TUT_USER_START
qb = QueryBuilder()
#TUT_USER_END
#TUT_SOLUTION_START
qb = QueryBuilder()
qb.append(Group, filters={'label': {'like': 'SSSP%'}}, tag='group')
qb.append(UpfData, with_group='group')
qb.all()
#TUT_SOLUTION_END
# Here I also visualize what's going on:
generate_query_graph(qb.get_json_compatible_queryhelp(), 'query2.png')
Image(filename='query2.png')
```

## Attributes and extras

In section 2, we showed you how you can `project` specific properties of a `Node` and gave a list of properties that a `Node` instance possesses. Since then, we have come across a lot of different `AiiDA` data nodes, such as `StructureData` and `UpfData`, that were secretly `Node`'s in disguise. Or to put it correctly, as `AiiDA` employs the object-oriented programming paradigm, both `StructureData` and `UpfData` are examples of subclasses of the `Node` class and therefore inherit its properties. That means that whatever property a `Node` has, both `StructureData` and `UpfData` will have too. However, there is a semantic difference between a `StructureData` node and a `UpfData`, and so we may want to add a property to one that would not make sense for the other. To solve this, `AiiDA` introduces the concept of `attributes`. These are similar to properties, except that they are specific to the `Node` type that they are attached to. This allows you to add an `attribute` to a certain node, without having to change the implementation of all the others.

For example, the `Dict` nodes that are generated as output of `PwCalculation`'s may have an attribute named `wfc_cutoff`. To project for this particular `attribute`, one can use exactly the same syntax as shown in section 2 for the regular `Node` properties, and one has to only prepend `attributes.` to the attribute name. Demonstration:

```{code-cell} ipython3
qb = QueryBuilder()
qb.append(PwCalculation, tag='pw')
qb.append(Dict, with_incoming='pw', project=["attributes.wfc_cutoff"])
qb.limit(5)
qb.all()
```

Note that not every `Dict` node has to have this attribute, in which case the `QueryBuilder` will return the python keyword `None`. Similar to the `attributes`, nodes also can have `extras`, which work in the same way, except that `extras` are mutable, which means that their value can be changed even after a node instance has been stored.

If you are not sure which attributes a given node has, you can use the `.attributes` property to simply retrieve them all. It will return a dictionary with all the attributes the node has.

Note that a node also has a number of additional methods. For instance, you can do `list(node.attributes_keys())` to get only the attribute keys, or `node.get_attribute('wfc_cutoff')` to get the value of a single attribute (these two variants are more efficient if the node has a lot of attributes and you don't need all data). Similarly, for extras, you have `node.extras`, `list(node.extras_keys())`, and `node.get_attribute('SOME_EXTRA_KEY')`.

```{code-cell} ipython3
qb = QueryBuilder()
qb.append(PwCalculation)
node, = qb.first()
node.attributes
```

The chemical-element symbol of a pseudopotential, that is represented by a `UpfData` node, is stored in the `element` attribute. Using the knowledge that filtering on attributes works exactly as for normal node properties, see if you can write a query that will search your database for pseudopotentials for silicon.

```{code-cell} ipython3
qb = QueryBuilder()
#TUT_SOLUTION_START
qb.append(UpfData, filters={'attributes.element': {'==': 'Si'}})
qb.all()
#TUT_SOLUTION_END
```

```{seealso}
For more exercises on relationships and attributes/extras, have a look at the appendix section on queries.
```

+++

## A small high-throughput study

The following section assumes that a specific dataset is present in your current AiiDA profile. If you are not running this script on the Virtual Machine of the AiiDA tutorial, this script will not produce the desired output.
You can download the Virtual Machine image from [https://aiida-tutorials.readthedocs.io](https://aiida-tutorials.readthedocs.io) along with the tutorial text (choose the correct version of the tutorial, depending on which version of AiiDA you want to try).

```{note}
If you are not following the tutorial on the official virtual machine that comes with this data, but you are working with your own database, you first have to {download}`import this archive <tutorial_perovskites_v0.1.aiida>` using `verdi import`.
```

+++

In this part of the tutorial, we will focus on how to systematically retrieve, parse and analyze the results of
multiple calculations using AiiDA. We know you’re able to do this yourself, but to save time, a set of calculations
have already been done with AiiDA for you on 57 perovskites, using three different pseudopotential families (LDA,
PBE and PBESOL, all from GBRV 1.2).

These calculations are spin-polarized (without spin-orbit coupling), use a Gaussian smearing and perform a variable-cell relaxation of the full unit cell. The idea of this part of the tutorial is to “screen” for magnetic and metallic perovskites in a “high-throughput” way. As you learned in the first part of the tutorial, AiiDA allows to organize calculations in groups. Once more check the list of groups in your database by typing:

```{code-cell} ipython3
!verdi group list -A
```

The calculations needed for this task were put in three different groups whose names start with "tutorial" (one for each pseudopotential family). The main task is to make a plot showing, for all perovskites and for each pseudopotential family, the total magnetization and the $-TS$ contribution from the smearing to the total energy.

+++

### Start building the query

So we first of all need to instantiate a QueryBuilder instance. We `append` the groups of interest, which means that we select only groups that start with the string `tutorial_`. We can execute the query after this append (this will not affect the final results) and check whether we have retrieved 3 groups.

```{code-cell} ipython3
# Instantiating QB:
qb = QueryBuilder()
# Appending the groups I care about:
qb.append(Group, filters={'label':{'like':'tutorial_%'}}, project='label', tag='group')
# Visualize:
print("Groups:", ', '.join([g for g, in qb.all()]))
generate_query_graph(qb.get_json_compatible_queryhelp(), 'query3.png')
Image(filename='query3.png')
```

### Append the calculations that are members of each group

```{code-cell} ipython3
# I want every PwCalculation that is a member of the specified groups:
#TUT_USER_START
qb.append(PwCalculation, tag='calculation', with_group=) # Complete the function call with the correct relationship-tag!
#TUT_USER_END
#TUT_SOLUTION_START
qb.append(PwCalculation, tag='calculation', with_group='group')
#TUT_SOLUTION_END
#Visualize
generate_query_graph(qb.get_json_compatible_queryhelp(), 'query4.png') 
Image(filename='query4.png')
```

### Append the structures that are input of the calculation

We extend the query to include the structures that are input of the calculations that match the query so far.
This means that we `append` StructureData, and defining the relationship with the calculation with corresponding keyword.

For simplicity the formulas have been added in the extras of each structure node under the key `formula`.
(The function that does this is called `store_formula_in_extra` and can be found in the top cell of this notebook. It also uses the QueryBuilder!)

Project the formula, stored in the extras under the key `formula`.

```{code-cell} ipython3
#TUT_USER_START
# Complete the function call with the correct relationship-tag!
qb.append(StructureData, project=, tag='structure', with_outgoing=)
#TUT_USER_END
#TUT_SOLUTION_START
qb.append(StructureData, project=['extras.formula'], tag='structure', with_outgoing='calculation')
#TUT_SOLUTION_END
# Visualize:
generate_query_graph(qb.get_json_compatible_queryhelp(), 'query5.png')
Image(filename='query5.png')
```

### Append the output of the calculation

Every successful PwCalculation outputs a `Dict` node that stores the parsed results as key-value pairs. You can find these pairs among the attributes of the `Dict` node. To facilitate querying, the parser takes care of storing values always in the same units, and these are documented. For convenience, the units are also added as key/value pairs (with the same key name, but with `_units` appended).
Extend the query so that also the output `Dict` of each calculation is returned. Project only
the attributes relevant to your analysis.

In particular, project (in this order):

* The smearing contribution
* The units of the smearing contribution
* The magnetization
* The units of the magnetization

(to know the projection keys, you can try to load one `CalcJobNode` from one of the groups, get its output `Dict` and inspect its `attributes` as discussed before, to see the key-value pairs that have been parsed).

```{code-cell} ipython3
#TUT_USER_START
# Complete the function call with the correct relationship-tag!
qb.append(Dict, tag='results', project=['attributes.energy_smearing', ...], with_incoming=)
#TUT_USER_END
#TUT_SOLUTION_START
qb.append(Dict, tag='results',
        project=['attributes.energy_smearing', 'attributes.energy_smearing_units',
           'attributes.total_magnetization', 'attributes.total_magnetization_units',
        ], with_incoming='calculation'
    )
#TUT_SOLUTION_END

generate_query_graph(qb.get_json_compatible_queryhelp(), 'query6.png')
Image(filename='query6.png')
```

### Print the query results

We can print the results to see if everything worked.

```{code-cell} ipython3
results = qb.all()
for item in results:
    print(', '.join(map(str, item)))
```

### Plot the results

Getting a long list is not always helpful, and a graph can be much more clear and useful. To help you, we have already prepared a function that visualizes the results of the query. Run the following cell and, if you did everything correctly, you should get a graph with the results of your queries!

```{code-cell} ipython3
plot_results(results)
```
