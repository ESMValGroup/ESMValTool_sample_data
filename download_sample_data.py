"""Download sample data from ESGF.

This script uses two configuration files:

1) A configuration file called config.yml in the root of the repostitory
   that contains account details for logging in to ESGF.
   Copy config.yml.template to config.yml and add your own account details to
   get started.

2) A configuration file called datasets.yml in esmvaltool_sample_data that
   defines the datasets to download.
"""
import datetime
import warnings
from pathlib import Path

import iris
import yaml
from pyesgf.logon import LogonManager
from pyesgf.search import SearchConnection


def get_time(filename):
    """Read the start and end date from a string.

    Parameters
    ----------
    filename : str
        A filename ending with a date, e.g. _20010101-20011231.nc.

    Returns
    -------
    (datetetime.datetime, datetime.datetime)
        A tuple containing the start and end date of the file.
    """
    times = Path(filename).stem.split('_')[-1].split('-')
    fmt = {
        6: "%Y%m",
        8: "%Y%m%d",
    }
    times = (datetime.datetime.strptime(t, fmt[len(t)]) for t in times)

    return tuple(times)


def select_by_time(filename, from_timestamp, to_timestamp):
    """Select file if it contains data in the requested timerange.

    Parameters
    ----------
    filename : str
        A filename ending with a date, e.g. _20010101-20011231.nc.
    from_timestamp : str or None
        The required start date, formatted as "2000-01-01T00:00:00Z".
    to_timestamp : str or None
        The required end date, formatted as "2000-01-01T00:00:00Z".
    """
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
    """Select a suitable host from a list of hosts.

    Parameters
    ----------
    hosts : :obj:`list` of :obj:`str`
        List of all available hosts.
    preferred_hosts : :obj:`list` of :obj:`str`
        List of preferred hosts.
    ignore_hosts : :obj:`list` of :obj:`str`
        List of hosts to ignore.

    Returns
    -------
    str or None
        The name of the most suitable host or None of all available hosts are
        in `ignore_hosts`.

    Notes
    -----
        Not sure if this is reliable: sometimes no files are found on the
        selected host.
    """
    hosts = [h for h in hosts if h not in ignore_hosts]
    if not hosts:
        return None

    for host in preferred_hosts:
        if host in hosts:
            return host

    return hosts[0]


def search(connection, preferred_hosts, ignore_hosts, facets):
    """Search for files on ESGF.

    Parameters
    ----------
    connection : pyesgf.search.SearchConnection
        Search connection
    preferred_hosts : :obj:`list` of :obj:`str`
        List of preferred hosts.
    ignore_hosts : :obj:`list` of :obj:`str`
        List of hosts to ignore.
    facets : :obj:`dict` of :obj:`str`
        Facets to constrain the search.

    Returns
    -------
    :obj:`dict` of :obj:`list` of :obj:`str`
        A dict with dataset names as keys and a list of filenames
        (OPeNDAP URLs) as values.
    """
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


def save_sample(in_file, out_file):
    """Load data and save a sample.

    Selects:
      - the first 2 pressure levels
      - latitudes between 88 and 90 degrees north
      - longitudes between 0 and 2 degrees east

    Only works with data with 1 dimensional latitude/longitude coordinates.

    Parameters
    ----------
    in_file : str
        Path to the input file.
    out_file : str
        Path to the output file.
    """
    print("Saving sample of", in_file, "to", out_file)
    with warnings.catch_warnings():
        warnings.filterwarnings(
            'ignore',
            message="Missing CF-netCDF measure variable .*",
            category=UserWarning,
            module='iris',
        )
        cube = iris.load_cube(in_file)
    print(cube)

    # select bottom two vertical levels
    cube = cube[:, :2]
    # select horizontal region
    try:
        latitude = iris.coords.CoordExtent('latitude', 88, 90)
        lat_size = cube[0, 0].intersection(
            latitude,
            ignore_bounds=True,
        ).shape[0]
        if lat_size < 2:
            lat_size = 2
    except IndexError:
        lat_size = 2
    try:
        longitude = iris.coords.CoordExtent('longitude', 0, 2)
        lon_size = cube[0, 0].intersection(
            longitude,
            ignore_bounds=True,
        ).shape[1]
        if lon_size < 2:
            lon_size = 2
    except IndexError:
        lon_size = 2
    cube = cube[:, :, -lat_size:, :lon_size]
    print("Shape of sample:", cube.shape)

    # Remove unsupported attribute, see
    # https://github.com/Unidata/netcdf4-python/issues/1020
    cube.attributes.pop('_NCProperties', None)

    iris.save(cube, target=out_file)


def sample_files(plot_type, dataset_name, files):
    """Sample files from ESGF.

    Parameters
    ----------
    plot_type : str
        The type of plot that can be made with the sampled data.
    dataset_name : str
        Name of the dataset to sample.
    files : :obj:`list` of :obj:`str`
        A list of filenames that comprise the dataset.
    """
    project_dir = Path(__file__).parent
    data_dir = project_dir / 'esmvaltool_sample_data' / 'data' / plot_type
    data_path = data_dir.joinpath(*dataset_name.split('.'))
    data_path.mkdir(parents=True, exist_ok=True)

    for filename in files:
        out_file = data_path / Path(filename).name
        if out_file.exists():
            print("File exists, skipping:", out_file)
        else:
            save_sample(filename, str(out_file))


def main():
    """Download sample data from ESGF.

    This will first find all available datasets on ESGF that match the facets
    in datasets.yml and subsequently find all available files on a single host.

    The resulting list of files is then sampled and stored locally in the
    directory 'data' using a commonly used directory structure.
    """
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
