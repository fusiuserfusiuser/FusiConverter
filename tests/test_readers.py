"""
Test readers created to enable loading files from napari via File -> Open File(s)
"""
# %% import libraries
import pytest
from pathlib import Path
import numpy as np

# %% Import functions to test

from src.fusiconverter.reader import read_mat

# %% Get paths to data files

session_date_id = '20251211-2'
load_data_dir = Path(__file__).parent.parent.parent / Path('data') / session_date_id
paths_mat = sorted([path for path in load_data_dir.glob('*/*.mat') if '_BM' not in path.stem and '_DP' not in path.stem and '_HQ' not in path.stem])

def test_mat_files_found():
    assert paths_mat, f'no .mat recordings found in {load_data_dir}'

@pytest.fixture(scope='module', params=paths_mat, ids=lambda p: p.name)
def read_mat_file(request):
    return read_mat(str(request.param), ask = False)


# %%
def test_read_mat(read_mat_file):
    assert len(read_mat_file) == 1 # napari wants it to be a list with a tuple inside, therefore length 1
    assert len(read_mat_file[0]) == 3 # the tuple inside the list should contain 3 elements

    image = read_mat_file[0][0]
    kwargs = read_mat_file[0][1]
    napari_layer_type = read_mat_file[0][2]

    assert len(image.shape) in [3,4] # the recorded data should have 3 spatial dimensions and sometimes a time dimension

    assert len(kwargs['scale']) == image.ndim
    assert kwargs['metadata']['spatial_axes'] == tuple(range(image.ndim - 3, image.ndim)) # spatial axes last
    assert not np.iscomplexobj(image)
    assert kwargs['metadata']['source_path'].endswith('.mat')
    assert 'name' in kwargs

    if 'affine' in kwargs:
        assert np.asarray(kwargs['affine']).shape == (image.ndim + 1, image.ndim + 1)

    assert napari_layer_type == 'image'

# %%
