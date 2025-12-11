import cloudinary.uploader

def upload_image_in_cloudinary_and_get_url(image_file):
    url_link = cloudinary.uploader.upload(image_file)
    return url_link