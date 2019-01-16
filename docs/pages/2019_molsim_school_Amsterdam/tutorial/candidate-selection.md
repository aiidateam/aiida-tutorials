# Selecting candidate materials

If we had unlimited computational resources, we would simply screen the whole
database.
From a tutorial perspective, however, there is not much difference between
screening 5 or screening 500 structures, except for the longer wait time.

Instead, you will now use what you've learned about extracting information from
the AiiDA database in order to select 3 good candidate materials, whose deliverable
capacities you are going to compute.

## What makes a good material for methane storage?

You've already learned this morning about some key descriptors that can be used to guess whether a nanoporous material can be suitable for methane storage.
You may want to consult the 
[SLIDES](https://docs.google.com/presentation/d/1F_bczGaH8n3CSR6rFoP3z8d6rPbRY1B7t_YuiaO0qgw/edit?usp=sharing)
in order to refresh your memory,
and have a look at a [brief description](../theoretical/geometric-properties) of some important geometrical properties computed by zeo++.

---
### Exercise

Pick two geometric descriptors to use for selecting your candidate materials.  
Load a `NetworkCalculation` node and identify the corresponding keys for these two descriptors (and their units).

---

## Finding good candidates

Let's use the QueryBuilder in order get the full range of the two descriptors in the database:

```python
qb=QueryBuilder()
qb.append(CifData, tag='cif')
qb.append(ParameterData, descendant_of='cif',
    project=['attributes.Density', 'attributes.Number_of_channels']
)
result = qb.all()
```
> **Note**  
> We are using `Density` and `Number_of_channels` here but this combination
> is just an example (and not an ideal choice).
> If you are wondering how to set up `ParameterData` and `CifData`, see
> [the previous section](queries#the-aiida-querybuilder).

Plot the result using the plotting library of your choice.
Using `matplotlib` you would do something like

```python
import matplotlib.pyplot as plt
x,y = zip(*result)
plt.plot(x,y,'o')
plt.show()
```

---
### Exercise

Use the information from the plots to identify a suitable target range for your
descriptors and filter the  structures within this range.


Once you've identified the range of your two parameters,
get the `label`s of the structure in this range.
Note that you can combine filters like so:
```
  filters = { "and": [
      { 'attributes.Density': {'and': [{'>': 1.0}, {'<': 1.5}] } },
      { 'attributes.Number_of_channels': {'>': 1}},
  ]},
```

For explanations on filters, see [the previous section](queries#filters).

---

Finally, put the structures you've identified into a group `candidates` 
so that you can refer to them easily from now on.
In addition to your three structures, also add 'HKUST1' in order to compare
to the reference calculation provided later on.

```python
candidate_labels = ['HKUST1']  # add your labels!
qb=QueryBuilder()
qb.append(CifData, filters={ 'label': {'in': candidate_labels}})
cifs = qb.all()
candidates = Group.get_or_create(name='candidates')  # create new group 
candidates.add_nodes([ cif[0] for cif in cifs])
```
After this, your group should show up in `verdi group list` 
and you can use `verdi group show candidates` to inspect its content.

In the python interface you can retrieve them back like so:
```python
candidates = Group.get_from_string('candidates')
for cif in candidates.nodes:
    print(cif)
```

