import iris
import pytest

from esmvaltool_sample_data import load_timeseries_cubes


@pytest.mark.parametrize("mip_table", [
    'amon',
    'day',
])
def test_load_timeseries_cubes(mip_table):
    """Load data and check if the types are OK."""
    cubes = load_timeseries_cubes(mip_table)
    assert isinstance(cubes, list)
    assert all(isinstance(cube, iris.cube.Cube) for cube in cubes)


def test_load_timeseries_cubes_invalid():
    """Test for fail on wrong input parameter."""
    with pytest.raises(ValueError):
        load_timeseries_cubes("FAIL")
