from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1] #cover-image.png by 1 it take the extension
    print(ext)
    valid_extension = ['.png','.jpeg','.jpg']
    if not ext.lower() in valid_extension:
        raise ValidationError('Unsupported file extension. Allowed extensions :'+str(valid_extension))
