from ngff_zarr import Methods, to_ngff_zarr, from_ngff_zarr, to_multiscales, to_ngff_image
from zarr.storage import MemoryStore

from ._data import input_images, store_new_multiscales, verify_against_baseline

from dask_image import imread



def test_gaussian_isotropic_scale_factors(input_images):
    dataset_name = "cthead1"
    image = input_images[dataset_name]
    baseline_name = "2_4/DASK_IMAGE_GAUSSIAN.zarr"
    multiscales = to_multiscales(image, [2, 4], method=Methods.DASK_IMAGE_GAUSSIAN)
    # store_new_multiscales(dataset_name, f'{baseline_name}', multiscales)
    verify_against_baseline(dataset_name, baseline_name, multiscales)


def test_from_ngff_zarr(input_images):
    dataset_name = "lung_series"
    data = imread.imread(input_images[dataset_name])
    image = to_ngff_image(data=data,
                          dims=('z', 'y', 'x'),
                          scale={'z': 2.5, 'y': 1.40625, 'x': 1.40625},
                          translation={'z': 332.5, 'y': 360., 'x': 0.0},
                          name='LIDC2')
    multiscales = to_multiscales(image)
    multiscales.scale_factors = None
    multiscales.method = None
    multiscales.chunks = None
    baseline_name = "from_ngff_zarr"
    # store_new_multiscales(dataset_name, baseline_name, multiscales)
    verify_against_baseline(dataset_name, baseline_name, multiscales)
    test_store =  MemoryStore(dimension_separator='/')
    to_ngff_zarr(test_store, multiscales)

    multiscales_back = from_ngff_zarr(test_store)
    # verify_against_baseline(dataset_name, baseline_name, multiscales_back)
