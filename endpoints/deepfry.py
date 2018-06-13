from io import BytesIO
from random import randint

from flask import send_file
from PIL import Image, ImageEnhance

from utils import http, noisegen
from utils.endpoint import Endpoint


class DeepFry(Endpoint):
    def generate(self, avatars, text, usernames):
        avatar = Image.open(http.get_image(avatars[0])).resize((400, 400)).convert('RGBA')
        joy = Image.open('assets/deepfry/joy.png').resize((100, 100)).rotate(randint(-30, 30)).convert('RGBA')
        hand = Image.open('assets/deepfry/ok-hand.png').resize((100, 100)).rotate(randint(-30, 30)).convert('RGBA')
        hundred = Image.open('assets/deepfry/100.png').resize((100, 100)).rotate(randint(-30, 30)).convert('RGBA')
        fire = Image.open('assets/deepfry/fire.png').resize((100, 100)).rotate(randint(-30, 30)).convert('RGBA')

        avatar.paste(joy, (randint(20, 75), randint(20, 45)), joy)
        avatar.paste(hand, (randint(20, 75), randint(150, 300)), hand)
        avatar.paste(hundred, (randint(150, 300), randint(20, 45)), hundred)
        avatar.paste(fire, (randint(150, 300), randint(150, 300)), fire)

        noise = avatar.convert('RGB')
        noise = noisegen.add_noise(noise, 25)
        noise = ImageEnhance.Contrast(noise).enhance(randint(5, 20))
        noise = ImageEnhance.Sharpness(noise).enhance(17.5)
        noise = ImageEnhance.Color(noise).enhance(randint(-15, 15))

        b = BytesIO()
        noise.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return DeepFry()
