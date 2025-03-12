If you run into an error with something like

```
ImportError ... Library not loaded @rpath/liblapack.d.dylib
```

This can be resolved by installation through conda:

```
conda install -c conda-forge libcblas
```
