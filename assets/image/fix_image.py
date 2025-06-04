from PIL import Image


eye = Image.open("eye.png")
eye.save("eye.png", icc_profile=None)

print("done")