from enum import Enum

class Methods(Enum):
    ITK_BIN_SHRINK = "itk_bin_shrink"
    ITK_GAUSSIAN = "itk_gaussian"
    # ITK_LABEL_GAUSSIAN = "itk_label_gaussian"
    DASK_IMAGE_GAUSSIAN = "dask_image_gaussian"
    DASK_IMAGE_MODE = "dask_image_mode"
    DASK_IMAGE_NEAREST = "dask_image_nearest"
