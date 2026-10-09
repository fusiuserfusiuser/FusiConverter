"""Napari reader for Allen CCF NIfTI atlases.

Registered as a napari plugin (see `napari.yaml`) so that opening an atlas from
File -> Open File(s) scales it the same way `view_mat_in_napari.py` does, i.e.
in mm, on the same grid as the recording.
"""

import numpy as np
from pathlib import Path

from .utils import load_atlas_image, load_mat_image, prepare_image_for_layer
from .viewer_ops import load_transform_matrix, put_transform_matrix_in_layer_affine


def napari_get_reader(path):
    """return the reader itself, not the data."""
    path =  str(path).lower()
    if path.endswith(('.nii', '.nii.gz')):
        return read_atlas
    if path.endswith('.mat'):
        return read_mat
    return None

def _saved_alignment_affine(source_path, ndim, spatial_axes=(0, 1, 2)):
    """Affine from <source>.alignment.json (maps to Allen CCF mm), or None if there is no saved alignment."""
    alignment_path = Path(f'{source_path}.alignment.json')
    if not alignment_path.exists():
        return None
    alignment = load_transform_matrix(alignment_path)
    print(f'Applied saved alignment to {Path(source_path).name}')
    return put_transform_matrix_in_layer_affine(alignment['transform_matrix'], ndim, spatial_axes)

def read_mat(mat_path):
    image, voxel_size, _origin, image_name = load_mat_image(mat_path)

    image, scale, spatial_axes = prepare_image_for_layer(np.abs(image), voxel_size)
    kwargs = {
        'name': f'{image_name}_{Path(mat_path).stem}',
        'scale': scale,
        'metadata': {'source_path': str(mat_path), 'spatial_axes': spatial_axes},
    }
    affine = _saved_alignment_affine(mat_path, image.ndim, spatial_axes)
    if affine is not None:
        kwargs['affine'] = affine

    return [(image, kwargs, 'image')]

def read_atlas(atlas_path):
    image, scale = load_atlas_image(atlas_path)
    kwargs = {
        'name': Path(atlas_path).name.rsplit('.nii', 1)[0],
        'scale': scale,
        # make it so a recording sitting inside the atlas volume stays visible in 3D
        'blending': 'additive',
        'metadata': {'source_path': str(atlas_path)},
    }
    # the Allen atlas is the reference frame, so its own alignment file is ignored
    if Path(atlas_path).parent.name != 'Allen_CCF':
        affine = _saved_alignment_affine(atlas_path, image.ndim)
        if affine is not None:
            kwargs['affine'] = affine
    return [(image, kwargs, 'image')]  # napari expects a list of layers
