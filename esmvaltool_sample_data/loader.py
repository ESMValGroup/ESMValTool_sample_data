from pathlib import Path

import cube_helper

cube_helper.logger.muffle_logger()

base_dir = Path(__file__).parent


def load_timeseries_data():
    """
    ta / Amon / historical / r1i1p1f1, any grid, 1850 - onwards, all dimensions reduced to a few steps except for the time dimension
    some other variable / ocean, probably a different frequency, similar number of timesteps, other dimensions reduced
    """

    timeseries_dir = base_dir / 'data' / 'timeseries'

    data_dirs = [
        'CMIP6.CMIP.CAMS.CAMS-CSM1-0.historical.r1i1p1f1.Amon.ta.gn.v20190708',
        'CMIP6.CMIP.CCCR-IITM.IITM-ESM.historical.r1i1p1f1.Amon.ta.gn.v20191226',
        'CMIP6.CMIP.CSIRO-ARCCSS.ACCESS-CM2.historical.r1i1p1f1.Amon.ta.gn.v20191108',
        'CMIP6.CMIP.E3SM-Project.E3SM-1-1.historical.r1i1p1f1.Amon.ta.gr.v20191211',
        'CMIP6.CMIP.FIO-QLNM.FIO-ESM-2-0.historical.r1i1p1f1.Amon.ta.gn.v20191204',
        'CMIP6.CMIP.HAMMOZ-Consortium.MPI-ESM-1-2-HAM.historical.r1i1p1f1.Amon.ta.gn.v20190627',
        'CMIP6.CMIP.INM.INM-CM4-8.historical.r1i1p1f1.Amon.ta.gr1.v20190605',
        'CMIP6.CMIP.INM.INM-CM5-0.historical.r1i1p1f1.Amon.ta.gr1.v20190610',
        'CMIP6.CMIP.IPSL.IPSL-CM6A-LR.historical.r1i1p1f1.Amon.ta.gr.v20180803',
        'CMIP6.CMIP.MPI-M.MPI-ESM1-2-HR.historical.r1i1p1f1.Amon.ta.gn.v20190710',
        'CMIP6.CMIP.MPI-M.MPI-ESM1-2-LR.historical.r1i1p1f1.Amon.ta.gn.v20190710',
        'CMIP6.CMIP.NOAA-GFDL.GFDL-CM4.historical.r1i1p1f1.Amon.ta.gr1.v20180701',
        'CMIP6.CMIP.NOAA-GFDL.GFDL-ESM4.historical.r1i1p1f1.Amon.ta.gr1.v20190726',
    ]

    input_dirs = [timeseries_dir / data_dir for data_dir in data_dirs]

    cubelists = []

    for input_dir in input_dirs:
        print(input_dir)
        cubelist = cube_helper.load(str(input_dir), filetype='.nc')
        cubelists.append(cubelist)

    return cubelists


def load_map_data():
    """a 4D atmospheric variable, all dimensions reduced to a few steps except
    the horizontal dimension(s) same for an ocean variable."""
    raise NotImplementedError


def load_profile_data():
    """a 4D atmospheric variable, all dimensions reduced to a few steps except
    the horizontal dimension(s) same for an ocean variable."""
    raise NotImplementedError


if __name__ == '__main__':
    cube_helper.logger.reset_logger()
    ts = load_timeseries_data()
    breakpoint()
