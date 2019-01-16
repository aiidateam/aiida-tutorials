You learned that the lengths of your simulation box should bigger than twice the cutoff value.\\
Therefore, for an orthogonal cell you should multiply you cell until its length
meets this criterion in every direction.

But what if the cell is not orthogonal?

You should not speak in terms of "lengths" but in terms of "perpendicular lengths",
as shown in the figure for the two-dimensional case. While in the orthogonal case
one can simplify pwa = b and pwb = a, in a tilted unit cell we have to compute
pwa and pwb and then evaluate if the cell needs to be expanded,
and the multiplication coefficients.



|![perp_width.png](../../../assets/2019_molsim_school_Amsterdam/perp_width.png){:width="98%"}|
|:--:|
| Perpendicular widths in orthogonal and tilted 2D cells. |


This explains why we need so much math in the function `multiply_unit_cell(cif)`,
to compute the Raspa input "UnitCells".

Note that if you do not multiply correctly the unit cell,
Raspa will complain in the output:

```terminal
WARNING: INAPPROPRIATE NUMBER OF UNIT CELLS USED
```

and you will (usually) get an uptake that is less then the correct one. Why?
