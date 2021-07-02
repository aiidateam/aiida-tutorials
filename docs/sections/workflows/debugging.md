(workflows-debugging)=

# Debugging work chains

In this section, we reproduce a series of common mistakes you may suffer from when writing your AiiDA work chains.


## Python syntax error

```{code-block} ipython
In [1]: from aiida.engine import run
In [2]: from my_first_workchain import OutputInputWorkChain
In [3]: result = run(OutputInputWorkChain, x=Int(4) )
In [4]: result
Out[2]:
{'product': <Int: uuid: 9c5c29de-6176-41fe-a051-672a5348e631 (pk: 1909) value: 4>}
```

## AiiDA daemon

Daemon not running

Daemon needs to be restarted

## Reading the report


## Wrong data type for the input/output


## Wrong output label
