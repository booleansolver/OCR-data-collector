"""
John Montgomery 29/03/21 - NEA 2022
"""
from generate import Generate, Group

form_a = Generate(
    'a',
    box_size=(80, 80),
    form_size=(5, 5),
    UID=2133,
    comment='Please write in pencil',
    font_path='Arial',
    background=(255, 255, 255, 255),
    comment_colour=(20, 20, 20)
)
form_b = Generate('b')
form_group = Group(
    [form_a,form_b],
    page_id=1234,
    font_path='Arial',
    title = 'OCR Data Collection',
    title_colour=(50,50,50)
)
form_group.show_image()