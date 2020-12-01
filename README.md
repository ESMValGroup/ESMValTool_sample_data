# Sample data for use with ESMValTool

This repository will contain samples of real data for use with [ESMValTool](https://github.com/ESMValGroup/ESMValTool) for demonstration purposes and automated testing.
The goal is to keep the repository size small (~ 100 MB), so it can be easily downloaded. We strive to include data that adhere well to the CMIP6 standard and can be loaded using simple [iris](https://github.com/SciTools/iris) commands.

At present, the repository contains 44 monthly, and 35 daily timeseries datasets. The specifications can be found in [`datasets.yml`](esmvaltool_sample_data/datasets.yml).

## Usage

The functionality of this repository is kept simple.

Data can be loaded using the following command for daily or monthly timeseries data.

```python
import esmvaltool_sample_data

# load monthly timeseries data
ts_amon_cubes = load_timeseries_cubes(mip_table='Amon')

# load daily timeseries data
ts_day_cubes = load_timeseries_cubes(mip_table='day')
```

## config-user.yml

If you want to use this dataset in your ESMValTool projects, add the following lines to your `config-user.yml`:

```yaml
rootpath:
  CMIP6: <path_to_repository>/esmvaltool_sample_data/data/timeseries/default_inputpath

drs:
  CMIP6: default
```

If you have installed `esmvaltool_sample_data`, you can find the `rootpath` using `python -c 'from esmvaltool_sample_data import base_dir; print(base_dir.parent)'`

## Licence

This work is dual-licensed under Apache 2.0 and CC-BY-SA 4.0.
All data files in the directory ([`esmvaltool_sample_data/data/`](esmvaltool_sample_data/data/)) are derived from CMIP6,
and licenced under CC-BY-SA 4.0. The rest of the contents of this work, if
not specified otherwise, is licenced under Apache 2.0. The terms of the
Apache 2.0 licence are available in the LICENCE file, and the terms of the
CC-BY-SA 4.0 licence in the [`esmvaltool_sample_data/data/LICENCE`](esmvaltool_sample_data/data/LICENCE) file.

## How to contribute

Suggestions/improvements/edits are most welcome. Please read the [contribution guidelines](CONTRIBUTING.md) before creating an issue or a pull request.
