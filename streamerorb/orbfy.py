from PIL import Image
import numpy as np
from apng import APNG, PNG
from apnggif import apnggif
import os
import requests
from io import BytesIO
import os

def orbfy(image_path, output_dir, streamer, frame_count=20, img_size=300):
    if image_path.startswith("http"):
        response = requests.get(image_path)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
    else:
        img = Image.open(image_path).convert("RGBA")
    
    img = img.resize((img_size, img_size))
    img_np = np.array(img)
    animation = APNG()
    for frameIndex in range(frame_count):
        theta_offset = 2 * np.pi * frameIndex / frame_count
        new_frame_np = np.zeros((img_size, img_size, 4), dtype=np.uint8)
        for y_2d in range(img_size):
            for x_2d in range(img_size):
                xs = (x_2d - img_size // 2) / (img_size // 2)
                ys = (y_2d - img_size // 2) / (img_size // 2)
                rs = np.sqrt(xs**2 + ys**2)
                
                if rs <= 1:
                    phi = np.arcsin(ys)
                    theta = np.arctan2(xs, np.sqrt(1 - rs**2)) + theta_offset
                    u = (theta + np.pi) / (2 * np.pi)
                    v = (phi + np.pi / 2) / np.pi
                    xi = int(u * img_size) % img_size
                    yi = int(v * img_size) % img_size
                    new_frame_np[y_2d, x_2d] = img_np[yi, xi]
        # save current frame to png file
        frame = Image.fromarray(new_frame_np)
        frame.save(os.path.join(output_dir, f"frame_{frameIndex}.png"))
        # append frame to the animation
        framepng = PNG.open(os.path.join(output_dir, f"frame_{frameIndex}.png"))
        animation.append(framepng, delay=100)
        # delete the frame file
        os.remove(os.path.join(output_dir, f"frame_{frameIndex}.png"))
    # Save the animation to a file
    animation.save(os.path.join(output_dir, "animation.apng"))
    # Convert the APNG to a GIF
    apnggif(os.path.join(output_dir, "animation.apng"), os.path.join(output_dir, f"{streamer}ORB.gif"))
    # Delete the APNG
    os.remove(os.path.join(output_dir, "animation.apng"))
    return os.path.join(output_dir, f"{streamer}ORB.gif")
    # Delete the saved frames
    # for frame in range(frame_count):
    #     os.remove(os.path.join(output_dir, f"frame_{frame}.png"))