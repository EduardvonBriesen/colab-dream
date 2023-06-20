import os
from datetime import datetime

folder_name = "dream"

# Get current date and time
now = datetime.now()
date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

# Set parent directory path
parent_path = '/home/ubuntu/stable-diffusion-webui/outputs/img2img-images'

# Check if "dream" folder exists and hasn't been renamed yet
if os.path.isdir(os.path.join(parent_path, folder_name)):

    # Get list of existing folder names
    folder_names = [name for name in os.listdir(parent_path) if os.path.isdir(os.path.join(parent_path, name))]

    # Determine next highest number
    highest_num = 0
    for name in folder_names:
        if name.startswith(f"{folder_name}_") and name[6:][:3].isdigit() and int(name[6:][:3]) > highest_num:
            highest_num = int(name[6:][:3])
    next_num = highest_num + 1

    # Construct new folder name
    new_folder_name = f"{folder_name}_{next_num:03d}_{date_time}"

    # Rename folder
    os.rename(os.path.join(parent_path, folder_name), os.path.join(parent_path, new_folder_name))

    new_folder_path = os.path.join(parent_path, folder_name)

    os.makedirs(new_folder_path)