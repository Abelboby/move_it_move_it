from PIL import Image

# Open your PNG
img = Image.open('icon.png')
# Convert and save as ICO
img.save('icon.ico', format='ICO') 