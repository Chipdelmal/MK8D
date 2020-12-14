
from colour import Color

def generateColorSwatch(baseColor, levels, alphaOffset=.1, lumaOffset=.1):
    colorsList = [None] * levels
    for i in range(levels):
        c = Color(baseColor)
        baseLum = 1 - c.get_luminance()
        lumLevel = (baseLum - ((1-baseLum)/levels * i))
        c.set_luminance(lumLevel)
        rgb = c.get_rgb()
        alphaLevel = alphaOffset + ((1-alphaOffset) * i/levels)
        colorsList[i] = (rgb[0], rgb[1], rgb[2], alphaLevel)
    return colorsList