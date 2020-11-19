# Sample data for use with the ESMValTool

This repository will contain samples of real data for use with the ESMValTool for demonstration purposes and automated testing.
The goal is to keep the repository size small (~ 100 MB), so it can be easily downloaded.

## Usage

TODO

## Updating the test data

Create and activate conda environment with the required dependencies
```bash
conda env create -f environment.yml -n esmvaltool_test_data
conda activate esmvaltool_test_data
```

Copy `config.yml.template` to `config.yml` and customize, at least add your
ESGF username and password.
Create an account on [https://esgf-data.dkrz.de/user/add/](https://esgf-data.dkrz.de/user/add/) if you do not have one.

Run
```bash
python download_sample_data.py
```
to download a sample of the test data.

## Licence

This work is dual-licensed under Apache 2.0 and CC-BY-SA 4.0.
The data (`esmvaltool_sample_data/data/`) are derived from CMIP6,
and licenced under CC-BY-SA 4.0. The rest of the contents of this work, if
not specified otherwise, is licenced under Apache 2.0. The terms of the
Apache 2.0 licence are available in the LICENCE file, and the terms of the
CC-BY-SA 4.0 licence in the `esmvaltool_sample_data/data/LICENCE` file.

## How to contribute

Suggestions/improvements/edits are most welcome. Please read the [contribution guidelines](CONTRIBUTING.md) before creating an issue or a pull request.
