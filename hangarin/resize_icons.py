from PIL import Image
img = Image.open('static/img/logo.png')
img.resize((192, 192)).save('static/img/icon-192.png')
img.resize((512, 512)).save('static/img/icon-512.png')
print('Done!')