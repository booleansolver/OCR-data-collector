import math
import os

from PIL import Image
from PIL import ImageFont, ImageDraw

import errors
import qr


class Generate:
    def __init__(
            self,
            label: str,
            box_size: tuple = (60, 60),
            form_size: tuple = (10, 3),
            form_dimensions: tuple = None,
            UID: str = None,
            comment: str = None,
            font_path: str = 'Arial',
            background: tuple = (255, 255, 255, 255),
            comment_colour: tuple = (0, 0, 0)
    ):

        UID = str(UID) if UID else None

        if form_dimensions:
            if box_size:
                # Here the user has provided a desired form size and a desired box size.
                form_size = (
                    math.floor(form_dimensions[0] / box_size[0]),
                    math.floor(form_dimensions[0] / box_size[0])
                )
            if form_size:
                box_size = (
                    math.floor(form_dimensions[0] / form_size[0]),
                    math.floor(form_dimensions[0] / form_size[0])
                )

        form_dimensions = (box_size[0] * form_size[0], box_size[1] * form_size[1])

        if 100 < box_size[0] < 50 or 100 < box_size[1] < 50:
            raise errors.ArgumentError(
                'Box size values must be at least 50, and less than 100 - please adjust your values'
            )

        if 10 < form_size[0] < 3 or 1 > form_size[1] > 99:
            raise errors.ArgumentError(
                'Form must be at least 1x3, and no greater than 9,99 - please adjust your values'
            )
        if UID:
            if len(UID) > 4:
                raise errors.ArgumentError(
                    "UID's are limited to 4 characters, 0-9 and a-z and A-Z"
                )
        qr_image, qrdata = qr.generate_qr_code(label, form_size, UID)
        path = os.path.dirname(os.path.abspath(__file__))

        f1 = Image.open(path + '/Fiducials/1.png')
        f2 = Image.open(path + '/Fiducials/2.png')
        f3 = Image.open(path + '/Fiducials/3.png')
        f4 = Image.open(path + '/Fiducials/4.png')
        try:
            font = ImageFont.truetype(font_path, size=20)
            head = ImageFont.truetype(font_path, size=44)
        except:
            font = ImageFont.load_default()
            head = ImageFont.load_default()
            print(f'{font_path} font not found on system... resorted to default')

        if comment:

            for idx, line in enumerate(comment.split('\n')):
                text_size = font.getsize(line)
                if text_size[0] > form_dimensions[0]:
                    raise errors.ArgumentError(
                        f'Comment line {idx} is too long. Width of form is {form_dimensions[0]}, and width of line is {text_size[0]}. Split the comment into more lines.'
                    )
            imgsize = (
                form_dimensions[0] + 100, form_dimensions[1] + ((comment.count('\n') + 1) * font.getsize('hg')[1]) + 10)
        else:
            imgsize = (form_dimensions[0] + 100, form_dimensions[1])
        image = Image.new('RGBA', imgsize, background)

        image.paste(f1, (0, 0))
        image.paste(qr_image, (0, 50))
        image.paste(f4, (0, box_size[1] * form_size[1] - 50))
        image.paste(f2, (form_dimensions[0] + 50, 0))
        image.paste(f3, (form_dimensions[0] + 50, box_size[1] * form_size[1] - 50))
        draw = ImageDraw.Draw(image)
        if comment:
            for idx, line in enumerate(comment.split('\n')):
                draw.text((10, form_dimensions[1] + idx * font.getsize('hg')[1]), line, comment_colour, font=font)

        for i in range(50, form_dimensions[0] + box_size[0] + 2, box_size[0]):
            draw.line((i, 0, i, form_dimensions[1] - 1), (0, 0, 0), 1)

        for i in range(0, form_dimensions[1], box_size[1]):
            draw.line((50, i, form_dimensions[0] + 50, i), (0, 0, 0), 1)
        draw.line((50, form_dimensions[1] - 1, form_dimensions[0] + 50, form_dimensions[1] - 1), (0, 0, 0), 1)
        w, h = head.getsize(label)
        draw.text((form_dimensions[0] + 50 + (50 - w) / 2, 50 + ((50 - h) / 2)), label, comment_colour, font=head)
        self.image = image
        self.label = label
        self.size = imgsize

    def save_image(self, filename, abs=False):
        if not abs:
            path = os.path.dirname(os.path.abspath(__file__))
            if filename[0] == '/':
                filename = path + filename
            else:
                filename = path + '/' + filename
        self.image.save(filename)

    def show_image(self):
        self.image.show()


class Group:
    def __init__(
            self,
            form: list,
            page_id=None,
            font_path: str = 'Arial',
            title: str = '',
            title_colour: tuple = (0, 0, 0)
    ):
        if page_id:
            page_id = str(page_id)
        formcount = len(form)
        check = ''.join([i.label for i in form])
        path = os.path.dirname(os.path.abspath(__file__))
        data = f"{page_id},{check},{formcount}"
        f1 = Image.open(path + '/Fiducials/5.png')
        f2 = Image.open(path + '/Fiducials/6.png')
        f3 = Image.open(path + '/Fiducials/7.png')
        f4 = Image.open(path + '/Fiducials/8.png')
        height = 220
        width = 0
        for i in form:
            height += i.size[1] + 20
            width = max(width, i.size[0])
        try:
            head = ImageFont.truetype(font_path, size=44)
        except:
            head = ImageFont.load_default()
            print(f'{font_path} font not found on system... resorted to default')

        image = Image.new('RGBA', (width + 200, height), (255, 255, 255, 255))
        image.paste(f1, (0, 0))
        image.paste(f2, (width + 100, 0))
        image.paste(f3, (width + 100, height - 100))
        image.paste(f4, (0, height - 100))

        code = qr.pagebarcode(data)
        w = int((width + 200 - code.size[0]) / 2)
        image.paste(code, (w, height - 100))
        draw = ImageDraw.Draw(image)
        draw.text((int((width + 200 - head.getsize(title)[0]) / 2), 10), title, title_colour, font=head)
        currenth = 120
        for item in form:
            w, h = item.size
            padw = int((width + 200 - w) / 2)
            image.paste(item.image, (padw, currenth))
            currenth += h + 20
        self.image = image

    def save_image(self, filename, abs=False):
        if not abs:
            path = os.path.dirname(os.path.abspath(__file__))
            if filename[0] == '/':
                filename = path + filename
            else:
                filename = path + '/' + filename
        self.image.save(filename)

    def show_image(self):
        self.image.show()
