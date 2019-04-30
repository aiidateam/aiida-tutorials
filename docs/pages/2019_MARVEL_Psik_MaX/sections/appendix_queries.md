Queries in AiiDA - Examples and Exercises
=========================================

Optional exercises on relationships (Task 3)
--------------------------------------------

**Hint for the exercises:**

-   You can have projections on properties of more than one entity in your query. You just have to add the *project* key (specifying the list of properties that you want to project) along with the corresponding entity when you append it.

**Exercises:**
 
Try to write the following queries:

-   Find all descendants of a StructureData with a certain uuid. Print both the StructureData and the descendant.

-   Find all the FolderData created by a specific user.

Optional exercises on attributes and extras (Task 4)
----------------------------------------------------

**Hint for the exercises:**

-   You can easily order or limit the number of the results by using the *order\_by()* and *limit()* methods of the QueryBuilder. For example, we can order all our job calculation by their *id* and limit the result to the first 10 as follows:

    ``` python
    qb = QueryBuilder()
    qb.append(JobCalculation, tag='calc')
    qb.order_by({'calc':'id'})
    qb.limit(10)
    qb.all()
    ```

**Exercises:**

-   Write a code snippet that informs you how many pseudopotentials you have for each element.

-   Smearing contribution to the total energy for calculations:

    1.  Write a query that returns the smearing contribution to the energy stored in some instances of ParameterData.

    2.  Extend the previous query to also get the input structures.

    3.  Which structures have a smearing contribution to the energy smaller or equal to -0.02?

Summarizing what we learned by now - An example
-----------------------------------------------

At this point you should be able to do queries with projections, joins and filters. Moreover, you saw how to apply filters and projections even on attributes and extras. Let’s discover the full power of the QueryBuilder with a complex graph query that allows you to project various properties from different nodes and apply different filters and joins.

Imagine that you would like to get the smearing energy for all the calculations that have finished and have a \(\mathrm{Sn_{2}O_{3}}\) as input. Moreover, besides from the smearing energy, you would like to print the units of this energy and the formula of the structure that was given to the calculation. The graphical representation of this query can be seen in Figure [fig:qb2] and the actual query follows:

![Complex graph query.]({{ site.baseurl}}/assets/2018_PRACE_MaX/qb_example_2.png)

[fig:qb2]

``` python
qb = QueryBuilder()
qb.append(
        StructureData,
        project=["extras.formula"],
        filters={"extras.formula":"Sn2O3"},
        tag="structure"
    )
qb.append(
        Calculation,
        tag="calculation",
        output_of="structure"
    )
qb.append(
        ParameterData,
        tag="results",
        filters={"attributes.energy_smearing":{"<=":-0.0001}},
        project=[
            "attributes.energy_smearing",
            "attributes.energy_smearing_units",
        ],
        output_of="calculation"
)
qb.all()
```
