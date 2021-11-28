import datetime
from discord import Embed
from discord import Color

def generate_embed(title, description, image_link=""):
	return Embed(title=title, 
	color=Color.from_rgb(0, 255, 255), 
	description=description, 
	timestamp=datetime.datetime.utcnow()).set_footer(text='Jules Winnfield').set_image(url=image_link)