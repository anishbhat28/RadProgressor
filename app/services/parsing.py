import pydicom
from PIL import Image
import torch
import numpy as np
from typing import Union, Tuple
import io

def load_image(file_content: bytes, filename: str) -> Tuple[Image.Image, torch.Tensor]:
    if filename.lower().endswith('.dcm'):
        return load_dicom(file_content)
    else:
        return load_png_jpg(file_content)

def load_dicom(file_content: bytes) -> Tuple[Image.Image, torch.Tensor]:
    ds = pydicom.dcmread(io.BytesIO(file_content))
    pixel_array = ds.pixel_array
    
    if len(pixel_array.shape) == 3:
        pixel_array = pixel_array[:, :, 0]
    
    pixel_array = ((pixel_array - pixel_array.min()) / 
                   (pixel_array.max() - pixel_array.min()) * 255).astype(np.uint8)
    
    image = Image.fromarray(pixel_array, mode='L')
    tensor = torch.from_numpy(pixel_array).float() / 255.0
    
    return image, tensor

def load_png_jpg(file_content: bytes) -> Tuple[Image.Image, torch.Tensor]:
    image = Image.open(io.BytesIO(file_content))
    
    if image.mode != 'L':
        image = image.convert('L')
    
    tensor = torch.from_numpy(np.array(image)).float() / 255.0
    
    return image, tensor
