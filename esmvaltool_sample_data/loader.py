from pathlib import Path

import cf_units
import iris

base_dir = Path(__file__).parent


def strip_attributes(cube):
    """Remove attributes that cause issues with merging and concatenation."""
    for attr in ['creation_date', 'tracking_id', 'history']:
        if attr in cube.attributes:
            cube.attributes.pop(attr)


def simplify_time(cube):
    coord = cube.coord('time')
    coord.convert_units(
        cf_units.Unit('days since 1850-1-1 00:00:00',
                      calendar=coord.units.calendar))


def load_cubes_from_input_dirs(input_dirs):
    """Loads all *.nc files from each input dir into a cube."""
    for input_dir in input_dirs:
        files = input_dir.glob('*.nc')
        cubes = iris.load(str(file) for file in files)
        for cube in cubes:
            strip_attributes(cube)
            simplify_time(cube)

        cubes = cubes.concatenate()
        cube = cubes[0]

        yield cube


def load_timeseries_cubes():
    """
    Data: ta / Amon / historical / r1i1p1f1, any grid, 1850 - onwards.
    All dimensions reduced to a few steps except for the time dimension
    Some other variable / ocean, probably a different frequency,
       similar number of timesteps, other dimensions reduced.
    """

    timeseries_dir = base_dir / 'data' / 'timeseries'

    data_dirs = [
        'CMIP6.CMIP.CAMS.CAMS-CSM1-0.historical.r1i1p1f1.Amon.ta.gn.v20190708',
        'CMIP6.CMIP.CCCR-IITM.IITM-ESM.historical.r1i1p1f1.Amon.ta.gn.v20191226',
        'CMIP6.CMIP.CSIRO-ARCCSS.ACCESS-CM2.historical.r1i1p1f1.Amon.ta.gn.v20191108',
        'CMIP6.CMIP.E3SM-Project.E3SM-1-1.historical.r1i1p1f1.Amon.ta.gr.v20191211',
        'CMIP6.CMIP.HAMMOZ-Consortium.MPI-ESM-1-2-HAM.historical.r1i1p1f1.Amon.ta.gn.v20190627',
        'CMIP6.CMIP.INM.INM-CM4-8.historical.r1i1p1f1.Amon.ta.gr1.v20190605',
        'CMIP6.CMIP.INM.INM-CM5-0.historical.r1i1p1f1.Amon.ta.gr1.v20190610',
        'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.historical.r1i1p1f1.Amon.ta.gr.v20180803',
        'CMIP6.CMIP.MPI-M.MPI-ESM1-2-HR.historical.r1i1p1f1.Amon.ta.gn.v20190710',
        'CMIP6.CMIP.MPI-M.MPI-ESM1-2-LR.historical.r1i1p1f1.Amon.ta.gn.v20190710',
        'CMIP6.CMIP.NOAA-GFDL.GFDL-CM4.historical.r1i1p1f1.Amon.ta.gr1.v20180701',
        'CMIP6.CMIP.NOAA-GFDL.GFDL-ESM4.historical.r1i1p1f1.Amon.ta.gr1.v20190726',

        # BUG: next dataset is problematic
        # raises ValueError: Cube 'air_temperature' must contain
        #     a single 1D y coordinate.
        # 'CMIP6.CMIP.FIO-QLNM.FIO-ESM-2-0.historical.r1i1p1f1.Amon.ta.gn.v20191204',
    ]

    input_dirs = [timeseries_dir / data_dir for data_dir in data_dirs]

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
