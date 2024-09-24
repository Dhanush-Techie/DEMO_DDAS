from PIL import Image
import imagehash

# Open images
image1 = Image.open('pravin_photo.jpg')
image2 = Image.open('pravin_photo2.jpg')

# image1 = Image.open('image.png')
# image2 = Image.open('image2.jpeg')

# Compute perceptual hashes
hash1 = imagehash.phash(image1)
hash2 = imagehash.phash(image2)

# Compare the hashes
difference = hash1 - hash2

print(f"pHash of image1: {hash1}")
print(f"pHash of image2: {hash2}")
print(f"Hash difference (Hamming distance): {difference}")
