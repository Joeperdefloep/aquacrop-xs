# aquacrop-xs
xarray-simlab implementation of AquaCrop-OSPy. This allows to run aquacrop on
array-like structures, such as rasters.

# Installing
Simply
```
conda env create -f environment.yml
```

Currently, it may be that you need to install the development branch of
`xarray-simlab`
[here](https://github.com/Joeperdefloep/xarray-simlab/tree/docs). This depends
on whether this branch is merged already.

Clone the repository, and make a (development install):

```
cd /path/to/xarray-simlab
git switch docs
pip install -e .
```
