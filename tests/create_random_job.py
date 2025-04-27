import os
import random
import string
import shutil


def generate_random_id(length=6) -> str:
    """
    Generates a random ID composed of numbers and lowercase letters.
    """
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=length))


def select_random_image(images_dir: str) -> str:
    """
    Selects a random image file from the given directory.
    Assumes images are named in the format img0xy.jpg where 01 <= xy <= 86.
    """
    valid_numbers = [f"{i:02d}" for i in range(1, 87)]
    valid_files = [f"img0{num}.jpg" for num in valid_numbers]

    existing_files = [f for f in os.listdir(images_dir) if f in valid_files]

    if not existing_files:
        raise FileNotFoundError("❌ No valid images found in the Images directory.")

    return random.choice(existing_files)


def create_job_with_image(base_dir: str, images_dir: str):
    """
    Creates a job_<random_id> folder and copies a random image into it as uploaded.jpg.
    """
    random_id = generate_random_id()
    job_folder_name = f"job_{random_id}"
    job_folder_path = os.path.join(base_dir, job_folder_name)

    os.makedirs(job_folder_path, exist_ok=False)
    print(f"✅ Created job folder: {job_folder_path}")

    selected_image = select_random_image(images_dir)
    src_image_path = os.path.join(images_dir, selected_image)
    dest_image_path = os.path.join(job_folder_path, "uploaded.jpg")

    shutil.copyfile(src_image_path, dest_image_path)
    print(f"✅ Copied {selected_image} as uploaded.jpg into {job_folder_path}")


if __name__ == "__main__":
    BASE_DIR = "../shared"  # Change if needed
    IMAGES_DIR = "../images"  # Directory containing img___.jpg files

    create_job_with_image(BASE_DIR, IMAGES_DIR)