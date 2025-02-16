from ngff_zarr import cli_input_to_ngff_image, ConversionBackend

from ._data import test_data_dir, input_images

def test_cli_input_to_ngff_image_itk(input_images):
    input = [test_data_dir / "input" / "cthead1.png",]
    image = cli_input_to_ngff_image(ConversionBackend.ITK, input)
    assert image.dims == ('y', 'x')

def test_cli_input_to_ngff_image_itk_glob(input_images):
    input = [test_data_dir / "input" / "lung_series" / "*.png",]
    image = cli_input_to_ngff_image(ConversionBackend.ITK, input)
    assert image.dims == ('z', 'y', 'x')

def test_cli_input_to_ngff_image_itk_list(input_images):
    input = [
            test_data_dir / "input" / "lung_series" / "LIDC2-025.png",
            test_data_dir / "input" / "lung_series" / "LIDC2-026.png",
            test_data_dir / "input" / "lung_series" / "LIDC2-027.png",
            ]
    image = cli_input_to_ngff_image(ConversionBackend.ITK, input)
    assert image.dims == ('z', 'y', 'x')

def test_cli_input_to_ngff_image_tifffile(input_images):
    input = [
            test_data_dir / "input" / "bat-cochlea-volume.tif",
            ]
    image = cli_input_to_ngff_image(ConversionBackend.TIFFFILE, input)
    assert image.dims == ('z', 'y', 'x')

def test_cli_input_to_ngff_image_imageio(input_images):
    input = [test_data_dir / "input" / "cthead1.png",]
    image = cli_input_to_ngff_image(ConversionBackend.IMAGEIO, input)
    assert image.dims == ('y', 'x')
