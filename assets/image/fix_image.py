from PIL import Image

login = Image.open("login.png")
signup = Image.open("signup.png")
account = Image.open("account.png")

login.save("login.png", icc_profile=None)
signup.save("signup.png", icc_profile=None)
account.save("account.png", icc_profile=None)

print("done")