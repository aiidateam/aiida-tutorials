(workflows-debugging)=

# Debugging work chains

In this section, we reproduce a series of common mistakes you may commit yourself when writing your AiiDA work chains.

## AiiDA daemon

### Daemon not running

Sometimes, after submitting a work chain, the process status will read as _created_.
This means that the process was created and it is ready to be run.
However, if there is no daemon running, your process will continue with that status indefinetely.
Check if that is the case with

```{code-block} console
$ verdi daemon status
Profile: my_aiida_profile
The daemon is not running
```

In case the daemon is not running, start it with
```{code-block} console
$ verdi daemon start
Starting the daemon... RUNNING
```

### Restart the daemon

When you create a new work chain

```{code-block} console
$ verdi daemon start
Starting the daemon... RUNNING
```

## Reading the report


## Wrong data type for the input/output


## Wrong output label
