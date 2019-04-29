# Upload your results

Once your calculations are finished, it's time to export and upload
them to the tutorial server.

```console
$ verdi group list -t autogroup.run # note the PK of the latest group
$ verdi export create -G <PK> database.aiida
```

Finally, it's time to upload your results to the [tutorial server](http://34.244.178.26)
and compare your result to those of the others.

 * What is the highest deliverable capacity you got? 
 * Did you pick the same material as some other participants?
 * Since the upload includes the provenance of your calculations,
   you'll be able to check which parameters the others used
   by clicking on the points in the scatter plot.


**That's it** -- you've completed the AiiDA molsim tutorial, well done!
Keep posted for AiiDA news on the [AiiDA mailing list](http://groups.google.com/group/aiidausers/subscribe), in particular the upcoming AiiDA 1.0 release with many improvements and new features.

If you're interested in continuing along these lines, you may want to (optional):

 * screen a few more materials to get a higher deliverable capacity
   (**please do not run more than 5 at a time** in order not to block the queue for the other participants).
 * learn about [how to change force fields in RASPA](../theoretical/settings-raspa)
   and play with the parameters to see how they impact the deliverable capacity
 * have a look at the [extra challenge on CO2 capture](../theoretical/charged-adsorbates.md)
(advanced, with less detailed instructions).
