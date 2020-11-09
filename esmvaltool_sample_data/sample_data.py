import datetime
import os
import warnings
from pathlib import Path

import iris
import yaml
from pyesgf.logon import LogonManager
from pyesgf.search import SearchConnection


def get_time(filename):
    """Read the start and end date from a string.

    Example: any string ending with _20010101-20011231.nc.
    """
    t1, t2 = Path(filename).stem.split('_')[-1].split('-')
    fmt = {6: "%Y%m", 8: "%Y%m%d"}
    t1 = datetime.datetime.strptime(t1, fmt[len(t1)])
    t2 = datetime.datetime.strptime(t2, fmt[len(t2)])

    return t1, t2


def select_by_time(filename, from_timestamp, to_timestamp):
    """Select file if it contains data in the requested timerange."""
    if from_timestamp is None and to_timestamp is None:
        return True

    start, end = get_time(filename)

    if from_timestamp is not None:
        from_date = datetime.datetime.fromisoformat(from_timestamp.rstrip('Z'))
        if to_timestamp is None:
            return end > from_date

    if to_timestamp is not None:
        to_date = datetime.datetime.fromisoformat(to_timestamp.rstrip('Z'))
        if from_timestamp is None:
            return start < to_date

    return start < to_date and end > from_date


def select_host(hosts, preferred_hosts, ignore_hosts):
    """Select a suitable host from a list of hosts."""
    # Not sure if this is reliable: sometimes no files are found on
    # the selected host.
    hosts = [h for h in hosts if h not in ignore_hosts]
    if not hosts:
        return None

    for host in preferred_hosts:
        if host in hosts:
            return host

    return hosts[0]


def search(connection, preferred_hosts, ignore_hosts, facets):
    print("Searching ...")
    ctx = connection.new_context(**facets, latest=True)
    print("Found", ctx.hit_count, "datasets (including copies)")

    # Find available datasets
    datasets = {}
    for dataset in ctx.search():
        dataset_name, host = dataset.dataset_id.split('|')
        if dataset_name not in datasets:
            datasets[dataset_name] = {}
        datasets[dataset_name][host] = dataset

    print("Found", len(datasets), "unique datasets")

    # Select host and find files on host
    files = {}
    for dataset_name in sorted(datasets):
        copies = datasets[dataset_name]
        print(
            "\nFinding files for dataset",
            dataset_name,
            "available on hosts",
            sorted(copies.keys()),
        )
        host = select_host(copies.keys(), preferred_hosts, ignore_hosts)
        if host is None:
            print("All hosts that have this datasets are ignored.")
            continue
        dataset = copies[host]

        if dataset_name not in files:
            files[dataset_name] = []
        dataset_files = dataset.file_context().search(
            variable=facets['variable'])
        if not dataset_files:
            print("Warning: no files found for", dataset_name, "on", host)

        for file in dataset_files:
            select = select_by_time(
                file.filename,
                facets.get('from_timestamp'),
                facets.get('to_timestamp'),
            )
            if select:
                print("Found", file.opendap_url)
                files[dataset_name].append(file.opendap_url)
        print(
            "Found",
            len(dataset_files),
            "files, of which",
            len(files[dataset_name]),
            "were within requested time range",
        )

    return files


def save_sample(data_url, target):
    print("Saving sample of", data_url, "to", target)
    with warnings.catch_warnings():
        warnings.filterwarnings(
            'ignore',
            message="Missing CF-netCDF measure variable .*",
            category=UserWarning,
            module='iris',
        )
        cube = iris.load_cube(data_url)
    print(cube)

    # select bottom two vertical levels
    cube = cube[:, :2]
    # select horizontal region
    exceptions = (
        IndexError,  # 0 points in requested range
        iris.exceptions.CoordinateMultiDimError,  # 2D lat/lon coord
        iris.exceptions.CoordinateNotFoundError,  # wrong lat/lon coord
    )
    try:
        latitude = iris.coords.CoordExtent('latitude', 88, 90)
        cube = cube.intersection(latitude, ignore_bounds=True)
    except exceptions:
        cube = cube[:, :, :2]
    try:
        longitude = iris.coords.CoordExtent('longitude', 0, 2)
        cube = cube.intersection(longitude, ignore_bounds=True)
    except exceptions:
        cube = cube[:, :, :, :2]
    print("Shape of sample:", cube.shape)

    # Remove unsupported attribute, see
    # https://github.com/Unidata/netcdf4-python/issues/1020
    cube.attributes.pop('_NCProperties', None)

    iris.save(cube, target=target)


def sample_files(plot_type, dataset_name, files):
    for filename in files:
        dirpath = (Path(__file__).parent / 'data' / plot_type /
                   dataset_name.replace('.', os.sep))
        dirpath.mkdir(parents=True, exist_ok=True)
        target = dirpath / Path(filename).name
        if target.exists():
            print("File exists, skipping:", target)
        else:
            save_sample(filename, target=str(target))


def main():

    cfg_file = Path(__file__).parent.parent / "config.yml"
    with cfg_file.open() as file:
        cfg = yaml.safe_load(file)

    facets_file = Path(__file__).parent / "datasets.yml"
    with facets_file.open() as file:
        cfg_data = yaml.safe_load(file)

    manager = LogonManager()
    if not manager.is_logged_on():
        manager.logon(**cfg['logon'])
    print("Logged", "on" if manager.is_logged_on() else "off")

    connection = SearchConnection(**cfg["search_connection"])

    for plot_type, facet_list in cfg_data['datasets'].items():
        print("Looking for data for plot type", plot_type)
        for dataset_facets in facet_list:
            print("Looking for data for dataset:")
            print("\n".join(f"{k}: {v}" for k, v in dataset_facets.items()))
            files = search(
                connection,
                cfg['preferred_hosts'],
                cfg['ignore_hosts'],
                dataset_facets,
            )
            for i, dataset_name in enumerate(files, start=1):
                print("Progress: sampling dataset", i, "of", len(files))
                if dataset_name in cfg_data['ignore']:
                    print("Skipping ignored dataset", dataset_name)
                else:
                    print("Sampling dataset", dataset_name)
                    sample_files(
                        plot_type,
                        dataset_name,
                        files[dataset_name],
                    )


if __name__ == '__main__':
    main()
