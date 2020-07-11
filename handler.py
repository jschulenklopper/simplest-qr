import json
import pyqrcode
import png
import base64
import os


## Normal HTTP requests.

# Create QR code for `/qr/new?data=some-data`
def http_create_qr(event, context):
    data = ""

    # Test whether data is passed in query string...
    if event['queryStringParameters'] and event['queryStringParameters']['data']:
        data = event['queryStringParameters']['data']
    else:
        return { "body": "Not found", "statusCode": 404 }

    image_in_base64 = core_create_qrcode(data)

    return { "body": image_in_base64,
             "headers": { "Content-Type": "image/png" },
             "isBase64Encoded": True,
             "statusCode": 200 }


# Generate QR code as PNG image and encode it as base64 string.
def core_create_qrcode(text):

    # Generate QR code image.
    # TODO Once service is deployed on own, short domain, try to restrict QR code version to 4.
    # That should be sufficient for 32 bytes in binary mode with error correction set to Q.
    mode = 'binary'
    error_correction = 'M'
    img = pyqrcode.create(text, error = error_correction, mode = mode)

    # Set unit size to 4 pixels and margin to 2 units (a bit smaller than default 4).
    return img.png_as_base64_str(scale = 4, quiet_zone = 2)

