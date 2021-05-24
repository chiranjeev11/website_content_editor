import os
import secrets
from PIL import Image
from io import BytesIO
import base64
from app import app

def save_picture(form_picture):

	form_picture = form_picture.split(",")[1]
	form_picture = BytesIO( base64.b64decode(form_picture) )

	random_hex = secrets.token_hex(8)

	f_ext = '.png'

	picture_fn = random_hex + f_ext

	picture_path = os.path.join(app.root_path, 'static/crop_images', picture_fn)

	output_size = (125, 125)

	img = Image.open(form_picture)

	img.thumbnail(output_size)

	img.save(picture_path)

	return picture_fn