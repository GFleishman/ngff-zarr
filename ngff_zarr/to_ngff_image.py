from typing import Union, Optional, Sequence, Hashable, Mapping, Dict, Tuple, Any, List
from collections.abc import MutableMapping

from numpy.typing import ArrayLike
from zarr.core import Array as ZarrArray
from dask.array.core import Array as DaskArray
import dask

from .methods._support import _spatial_dims
from .ngff_image import NgffImage
from .zarr_metadata import Units


def to_ngff_image(
    data: Union[ArrayLike, MutableMapping, str, ZarrArray],
    dims: Optional[Sequence[Union["t", "z", "y", "x", "c"]]] = None,
    scale: Optional[Union[Mapping[Hashable, float]]] = None,
    translation: Optional[Union[Mapping[Hashable, float]]] = None,
    name: str = "image",
    axes_units: Optional[Mapping[str, Units]] = None,
) -> NgffImage:
    """
    Create an image with pixel array and metadata to following the OME-NGFF data model.

    data: ArrayLike, ZarrArray, MutableMapping, str
        Multi-dimensional array that provides the image pixel values. It can be a numpy.ndarray
         or another type that behaves like a numpy.ndarray, i.e. an ArrayLike.
         If a ZarrArray, MutableMapping, or str, it will be loaded into Dask lazily
         as a zarr Array.

    dims: sequence of hashable, optional
        Tuple specifying the data dimensions.
        Values should drawn from: {'t', 'z', 'y', 'x', 'c'} for time, third spatial direction
        second spatial direction, first spatial dimension, and channel or
        component, respectively spatial dimension, and time, respectively.

    scale: dict of floats, optional
        Pixel spacing for the spatial dims

    translation: dict of floats, optional
        Origin or offset of the center of the first pixel.

    name: str, optional
        Name of the resulting image

    axes_units: dict of str, optional
        Units to associate with the axes. Should be drawn from UDUNITS-2, enumerated at
        https://ngff.openmicroscopy.org/latest/#axes-md


    Returns
    -------

    image: NgffImage
        Representation of an image (pixel data + metadata) for a single scale of an NGFF-OME-Zarr multiscale dataset
    """

    ndim = data.ndim
    if dims is None:
        if ndim < 4:
            dims = ("z", "y", "x")[-ndim:]
        elif ndim < 5:
            dims = ("z", "y", "x", "c")
        elif ndim < 6:
            dims = ("t", "z", "y", "x", "c")
        else:
            raise ValueError("Unsupported dimension: " + str(ndim))
    else:
        _supported_dims = {"c", "x", "y", "z", "t"}
        if not set(dims).issubset(_supported_dims):
            raise ValueError("dims not valid")

    if scale is None:
        scale = {dim: 1.0 for dim in dims if dim in _spatial_dims}

    if translation is None:
        translation = {dim: 0.0 for dim in dims if dim in _spatial_dims}

    if not isinstance(data, DaskArray):
        if isinstance(data, (ZarrArray, str, MutableMapping)):
            data = dask.array.from_zarr(data)
        else:
            data = dask.array.from_array(data)

    ngff_image = NgffImage(
        data=data,
        dims=dims,
        scale=scale,
        translation=translation,
        name=name,
        axes_units=axes_units,
    )

    return ngff_image
