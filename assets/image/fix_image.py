from PIL import Image

imgbg = Image.open("assets/image/background.png")
imgbg.save("assets/image/background.png", icc_profile=None)

imgmusicC = Image.open("assets/image/music-close.png")
imgmusicC.save("assets/image/music-close.png", icc_profile=None)

imgMusicO = Image.open("assets/image/music-open.png")
imgMusicO.save("assets/image/music-open.png", icc_profile=None)