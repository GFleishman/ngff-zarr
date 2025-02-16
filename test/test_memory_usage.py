import dask.array
import numpy as np
import zarr

from ngff_zarr import memory_usage, NgffImage, to_ngff_image, to_multiscales, to_ngff_zarr, from_ngff_zarr

def test_memory_usage():
    arr = np.random.randint(0, 255, size=(4,4,4), dtype=np.uint8)
    arr = dask.array.from_array(arr, chunks=2)
    image = to_ngff_image(arr)
    multiscales = to_multiscales(image, scale_factors=[], chunks=2)
    store = zarr.storage.MemoryStore()
    to_ngff_zarr(store, multiscales)
    multiscales = from_ngff_zarr(store)

    image = multiscales.images[0]
    arr = image.data
    assert arr.nbytes == 64
    usage = memory_usage(image)
    assert usage == 64
    usage = memory_usage(image, {'z'})
    assert usage == 32

    arr1 = arr + 1
    assert arr1.nbytes == 64
    image.data = arr1
    usage = memory_usage(image)
    assert usage == 64
    usage = memory_usage(image, {'z'})
    assert usage == 32
