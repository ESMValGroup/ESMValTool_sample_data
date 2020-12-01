Contribution guidelines
=======================

Updating the test data
----------------------

Create and activate conda environment with the required dependencies
```bash
conda env create -f environment.yml -n esmvaltool_test_data
conda activate esmvaltool_test_data
```

Copy `config.yml.template` to `config.yml` and customize, at least add your
ESGF username and password.
Create an account on https://esgf-data.dkrz.de/user/add/ if you do not have one.

Run
```bash
python download_sample_data.py
```
to download a sample of the test data.
