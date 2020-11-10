from pathlib import Path

import cf_units
import iris

base_dir = Path(__file__).parent

problematic = [
    # iris.exceptions.ConcatenateError: failed to concatenate into a single cube.
    'esmvaltool_sample_data/data/timeseries/CMIP6/CMIP/NCC/NorCPM1/historical/r1i1p1f1/Amon/ta/gn/v20190914',
    # UserWarning: Gracefully filling 'lat' dimension coordinate masked points
    'esmvaltool_sample_data/data/timeseries/CMIP6/CMIP/NCAR/CESM2-FV2/historical/r1i1p1f1/Amon/ta/gn/v20191120',
    'esmvaltool_sample_data/data/timeseries/CMIP6/CMIP/NCAR/CESM2-WACCM-FV2/historical/r1i1p1f1/Amon/ta/gn/v20191120',
]


def strip_attributes(cube: 'iris.Cube') -> None:
    """Remove attributes in-place that cause issues with merging and
    concatenation."""
    for attr in ['creation_date', 'tracking_id', 'history']:
        if attr in cube.attributes:
            cube.attributes.pop(attr)


def simplify_time(cube: 'iris.Cube') -> None:
    """Simplifies the time coordinate in-place."""
    coord = cube.coord('time')
    coord.convert_units(
        cf_units.Unit('days since 1850-1-1 00:00:00',
                      calendar=coord.units.calendar))


def load_cubes_from_input_dirs(input_dirs: list) -> 'iris.Cube':
    """Generator that loads all *.nc files from each input dir into a cube."""
    for input_dir in input_dirs:
        if str(input_dir) in problematic:
            # print('Skipping', input_dir)
            continue
        # print(input_dir)
        files = input_dir.glob('*.nc')
        cubes = iris.load(str(file) for file in files)
        for cube in cubes:
            strip_attributes(cube)
            simplify_time(cube)

        cube = cubes.concatenate_cube()

        yield cube


def load_timeseries_cubes(mip_table: str = 'Amon') -> list:
    """Returns a list of iris cubes with timeseries data.

    The data are: ta / Amon / historical / r1i1p1f1, any grid, 1950 - onwards.
    All dimensions were reduced to a few steps except for the time dimension.

    Parameters
    ----------
    mip_table: str
        select monthly (`Amon`) or daily (`day`) data.

    Returns
    -------
    list of iris.cube
    """

    timeseries_dir = base_dir / 'data' / 'timeseries'

    paths = timeseries_dir.glob(f'**/{mip_table}/**/*.nc')
    input_dirs = list(set(path.parent for path in paths))

    cubes = load_cubes_from_input_dirs(input_dirs)

    return list(cubes)


def load_map_cubes():
    """a 4D atmospheric variable, all dimensions reduced to a few steps except
    the horizontal dimension(s) same for an ocean variable."""
    raise NotImplementedError


def load_profile_cubes():
    """a 4D atmospheric variable, all dimensions reduced to a few steps except
    the vertical dimension(s) same for an ocean variable."""
    raise NotImplementedError


if __name__ == '__main__':
    ts = load_timeseries_cubes()
    breakpoint()
