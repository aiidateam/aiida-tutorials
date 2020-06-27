Exporting your database
=======================

Let's put the nodes to be exported into a new group `report`:

```python
CifData=DataFactory('cif')
qb=QueryBuilder()
qb.append(Group, filters={'name':'mofs'}, tag='mofs') # filter by 'mofs' group
qb.append(CifData, member_of='mofs', tag='cifs')
cifs = qb.all()

qb.append(Node, descendant_of='cifs') # get all children
children = qb.all()

report, created = Group.get_or_create(name='report')
report.add_nodes([ n[0] for n in cifs + children ])
```

Once you've grouped your nodes, check the contents of the group and
export it:

```console
$ verdi group show report
$ verdi export create -g report database.aiida
```

*Note:* AiiDA automatically exports the direct outputs of calculations,
i.e. we don't need to add them to our group explicitly.
