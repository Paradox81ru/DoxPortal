import os
import random

from PIL import Image, ImageDraw, ImageFont, ImageColor
from django.conf import settings


class Captcha:
    """ Каптча """
    def __init__(self,
                 trash_range=15,
                 code_range=5,
                 offset=50,
                 font_size=40,
                 base_size=(250, 50)):
        self._trash_range = trash_range
        self._code_range = code_range
        self._offset = offset
        self._font_size = font_size
        self._base_size = base_size
        self._letters = self._letters()
        self._font_path = self._font_path()

    @classmethod
    def _random_fill(cls, red=255, green=255, blue=255):
        """ Случайный цвет RGB """
        fill = (random.randrange(red),
                random.randrange(green),
                random.randrange(blue))
        return fill

    @classmethod
    def _random_font(cls, path='fonts', s1=12, s2=35, main=None):
        """ Случайный шрифт """
        if main is None:
            size = random.randrange(s1, s2)
        else:
            size = main
        font_files = os.listdir(path)
        r_font = os.path.join(path, random.choice(font_files))
        font = ImageFont.truetype(r_font, size)
        return font

    @classmethod
    def _random_coords(cls, coords=(250, 50)):
        """ Случайные координаты """
        coords = (random.randrange(0, coords[0]),
                  random.randrange(0, coords[1]))
        return coords

    @classmethod
    def _letters(cls):
        """ Создает и возвращает кортеж символов """
        letters = (
            'a', 'b', 'c', 'd', 'e', 'f',
            'g', 'h', 'j', 'k', 'm', 'n',
            'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z',
            '0', '1', '2', '3', '4', '5',
            '6', '7', '8', '9'
        )
        # или, лучше воспользуемся готовыми наборами:
        # letters = tuple(string.ascii_lowercase + string.digits)
        return letters

    @classmethod
    def _font_path(cls):
        """ Возвращает папку со шрифтами"""
        return os.path.join(settings.BASE_DIR, r'common/helpers/big/dox_captcha/fonts')

    # Не используется
    def _draw_trash_letters(self, img_drw):
        """ Рисует мусор из светных символов """
        for i in range(self._trash_range):
            img_drw.font = self._random_font(self._font_path)
            img_drw.text(self._random_coords(self._base_size), random.choice(self._letters), self._random_fill())

    def _draw_trash_lines(self, img_drw):
        """
        Рисуте мусор из прямых линий

        :type img_drw: ImageDraw.Draw
        :return:
        """
        img_drw.line(self._rand_line('h'), ImageColor.getrgb("Black"), 2)
        img_drw.line(self._rand_line('h'), ImageColor.getrgb("Black"), 2)
        img_drw.line(self._rand_line('v'), ImageColor.getrgb("Black"), 2)
        img_drw.line(self._rand_line('v'), ImageColor.getrgb("Black"), 2)

    def _rand_line(self, direction):
        """
        Возвращает случайные линии горизонтальные или вертикальные
        :param direction: направление линии 'h' или 'v'
        :return:
        """
        direction = direction.lower()
        if direction not in ('h', 'v'):
            raise ValueError("Координаты могут быть только 'h' или 'v'")
        if direction == 'h':
            max_size = self._base_size[1]
            cord1 = random.randint(1, max_size-2)
            cord2 = random.randint(1, max_size-2)
            line_coord = [0, cord1, 250, cord2]
        else:
            max_size = self._base_size[0]
            cord1 = random.randint(1, max_size-2)
            cord2 = random.randint(1, max_size-2)
            line_coord = [cord1, 0, cord2, 50]

        return line_coord

    def _draw_code_img(self, img_drw, code):
        """ Создает и возвращает изображение с кодом капчи"""
        x = 0
        offset = random.randrange(30, self._offset)
        for c in code:
            img_drw.text((x, 0), c, 'black', font=self._random_font(self._font_path, main=self._font_size))
            x += offset

    def captcha(self, destination):
        # Если установлен режим отладки и отключена капча,
        if settings.DEBUG and settings.NO_CAPTCHA:
            # то сделаем капчу равной "12345".
            code = list('12345')
        else:
            # Иначе генерируем случайный набор символов из списка символов в пределах.
            code = [random.choice(self._letters) for i in range(self._code_range)]

        img = Image.new("RGBA", self._base_size, 'white')
        img_drw = ImageDraw.Draw(img)
        # Создаем первое изображение с мусором — случайными символами
        self._draw_trash_lines(img_drw)
        self._draw_code_img(img_drw, code)

        # Сохраняем изображение
        img.save(destination, 'PNG')
        img.close()
        # И возвращаем строку
        return ''.join(code)


