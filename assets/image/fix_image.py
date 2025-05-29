from PIL import Image

bird1 = Image.open("birds/glitch-bird.png")
bird2 = Image.open("birds/blue-bird.png")
bird3 = Image.open("birds/green-bird.png")
bird4 = Image.open("birds/yellow-bird.png")
bird5 = Image.open("birds/navy-bird.png")

bird1.save("birds/glitch-bird.png", icc_profile=None)
bird2.save("birds/blue-bird.png", icc_profile=None)
bird3.save("birds/green-bird.png", icc_profile=None)
bird4.save("birds/yellow-bird.png", icc_profile=None)
bird5.save("birds/navy-bird.png", icc_profile=None)