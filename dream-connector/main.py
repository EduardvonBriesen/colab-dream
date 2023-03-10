import sys
from PIL import Image,ImageDraw

if __name__ == "__main__":

    args = sys.argv
    # ronny, take this 
    prompt = args[1]
    
   
   
  
    
    image = Image.new("RGB", (100, 100), (255, 0, 0))

    # Draw a blue rectangle in the center of the image
    draw = ImageDraw.Draw(image)
    draw.rectangle((40, 40, 60, 60), fill=(0, 0, 255))

    # Save the image as a PNG file
    image.save("output.png", "PNG")
  
