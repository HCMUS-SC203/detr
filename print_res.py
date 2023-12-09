from PIL import Image

def get_image_resolution(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        print(f"Image Resolution: {width} x {height} pixels")

# Replace 'your_image_path.jpg' with the path to your image file
image_path = 'your_image_path.jpg'
get_image_resolution(image_path)