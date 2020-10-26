import os
from pathlib import Path

import iris
import xarray as xr
import yaml
from pyesgf.logon import LogonManager
from pyesgf.search import SearchConnection

IGNORE_FACET_CHECK = True


def logon(hostname, username, password):
    lm = LogonManager()
    if not lm.is_logged_on():
        lm.logon(
            hostname=hostname,
            username=username,
            password=password,
            interactive=False,
            bootstrap=True,
        )
    print("Logged", "on" if lm.is_logged_on() else "off")


def search(connection, preferred_hosts, ignore_hosts, dataset):
    print("Searching")
    ctx = connection.new_context(**dataset)
    print("Found", ctx.hit_count, "items")

    # Find available datasets
    datasets = {}
    for result in ctx.search(ignore_facet_check=IGNORE_FACET_CHECK):
        dataset_name, host = result.dataset_id.split('|')
        print("Found", dataset_name, "on", host)
        if dataset_name not in datasets:
            datasets[dataset_name] = {}
        datasets[dataset_name][host] = result

    # Select host and find files on host
    files = {}
    for dataset_name, results in datasets.items():
        print(
            "Finding files for dataset",
            dataset_name,
            "available on hosts",
            sorted(results.keys()),
        )
        for host in preferred_hosts:
            if host in results:
                result = results[host]
                break
        else:
            results = {
                k: v
                for k, v in results.items() if k not in ignore_hosts
            }
            if not results:
                continue
            host = next(iter(results))
            result = results[host]
        # Not sure if this is reliable: sometimes no files are found on the
        # selected host.
        if dataset_name not in files:
            files[dataset_name] = []
        for file in result.file_context().search(
                variable=dataset['variable'],
                ignore_facet_check=IGNORE_FACET_CHECK):
            print(file.opendap_url)
            files[dataset_name].append(file.opendap_url)
        if not files[dataset_name]:
            print("Warning: no files found for", dataset_name, "on", host)
    return files


def save_xarray(data_url, target):

    ds = xr.open_dataset(data_url, chunks={'time': 120})
    print(ds)

    ds = ds.isel(time=slice(0, 1))
    ds = ds.sel(lat=slice(-50, 50), lon=slice(0, 50))

    ds.to_netcdf(target)


def save_iris(data_url, target):
    print("Saving sample of", data_url, "to", target)
    cube = iris.load_cube(data_url)
    print(cube)
    cube = cube[:, :2, :2, :2]

    iris.save(cube, target=target)


def save(dataset_name, files):
    for filename in files:
        dirpath = Path(__file__).parent / 'data' / 'timeseries' / dataset_name
        dirpath.mkdir(parents=True, exist_ok=True)
        target = dirpath / os.path.basename(filename)
        if not target.exists():
            save_iris(filename, target=str(target))


if __name__ == '__main__':

    dataset_cmip5 = {
        'variable': 'ta',
        'project': 'CMIP5',
        'experiment': 'historical',
        #'model': 'MPI-ESM-LR',
        'ensemble': 'r1i1p1',
        'cmor_table': 'Amon',
        'from_timestamp': "1850-01-01T00:00:00Z",
        'to_timestamp': "1900-01-01T00:00:00Z",
    }

    dataset_cmip6 = {
        'variable': 'ta',
        'project': 'CMIP6',
        'activity_id': 'CMIP',
        'experiment_id': 'historical',
        #'source_id': 'NorESM2-MM',
        'variant_label': 'r1i1p1f1',
        #'grid_label': 'gn',
        'table_id': 'Amon',
        'from_timestamp': "1850-01-01T00:00:00Z",
        'to_timestamp': "1900-01-01T00:00:00Z",
    }

    cfg_file = Path(__file__).parent.parent / "config.yml"
    with cfg_file.open() as file:
        cfg = yaml.safe_load(file)

    logon(**cfg["logon"])
    connection = SearchConnection(**cfg["search_connection"])
    files = search(connection, cfg['preferred_hosts'], cfg['ignore_hosts'],
                   dataset_cmip6)

    for dataset_name in files:
        save(dataset_name, files[dataset_name])
