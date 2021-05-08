"""
John Montgomery 29/03/21 - NEA 2022
"""

import code128
import pyqrcode
from PIL import Image


def generate_qr_code(
        label: str,
        formsize: tuple,
        uid
):
    """
    A helper to generate a QR code and store any needed data for the form
    :param label:
    :param boxsize:
    :param formsize:
    :param uid:
    :return:
    """

    data = f"{label},{formsize[0]},{formsize[1]},{uid}"

    qr = pyqrcode.create(data, error='M', version=1)

    return text2png(qr.text()), data


def text2png(value):
    length = len(value.split('\n')[0])
    value = value.replace('\n', '')
    mapdict = {'0': (255, 255, 255),
               '1': (0, 0, 0)}
    data = [mapdict[letter] for letter in value]
    img = Image.new('RGB', (length, len(value) // length), "white")
    img.putdata(data)
    img = img.resize((50, 50), resample=Image.NEAREST, box=(2, 2, 27, 27))
    return img


def pagebarcode(data):
    return code128.image(data, 100)
