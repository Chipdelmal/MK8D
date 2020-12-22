
from colour import Color

def generateColorSwatch(
    baseColor, levels,
    alphaOffset=(.1, .9), lumaOffset=(.1, 1),
):
    colorsList = [None] * levels
    for i in range(levels):
        c = Color(baseColor)
        baseLum = lumaOffset[1] - c.get_luminance()
        lumLevel = (baseLum - ((lumaOffset[1]-baseLum)/levels * i))
        c.set_luminance(lumLevel)
        rgb = c.get_rgb()
        alphaLevel = alphaOffset[0] + ((alphaOffset[1]-alphaOffset[0]) * i/levels)
        colorsList[i] = (rgb[0], rgb[1], rgb[2], alphaLevel)
    return colorsList