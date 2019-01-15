# Upload your results

Once your calculations are finished, it's time to export and upload
them to the tutorial server.

Let's put the nodes to be exported into a new group `results`:

```python
qb=QueryBuilder()
qb.append(Group, filters={'name':'candidates'}, tag='candidates') # filter by 'mofs' group 
qb.append(CifData, member_of='candidates', tag='cifs')
cifs = qb.all()   # these are your candidate structures

qb.append(Node, descendant_of='cifs') # get all children 
children = qb.all()

results = Group(name='results')
results.store() 
results.add_nodes([ n[0] for n in cifs + children ])
```

Once you've grouped your nodes, check the contents of the group and
export it:

```terminal
$ verdi group show results
$ verdi export create -g results database.aiida
```

Finally, it's time to upload your results to the [tutorial server](http://34.244.178.26)
and compare your result to those of the others.

Since the upload includes the provenance of your calculations,
you'll be able to check which parameters the others used
by clicking on the points in the scatter plot.
