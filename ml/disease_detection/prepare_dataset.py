
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "raw"
PLANTVILLAGE_DIR = DATA_DIR / "PlantVillage"
SUMMARY_FILE = BASE_DIR / "data" / "dataset_summary.txt"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

print("AgriScan - PlantVillage Dataset Inventory")
print("=" * 45)

if not PLANTVILLAGE_DIR.exists():
    print("PlantVillage folder not found:", PLANTVILLAGE_DIR)

else:
    class_folders = sorted(
        folder for folder in PLANTVILLAGE_DIR.iterdir()
        if folder.is_dir()
    )

    total_images = 0
    total_readable = 0
    total_unreadable = 0
    summary_lines = [
        "AgriScan - PlantVillage Dataset Summary",
        "=" * 45,
        ""
    ]

    for folder in class_folders:
        image_files = [
            file for file in folder.iterdir()
            if file.is_file()
            and file.suffix.lower() in IMAGE_EXTENSIONS
        ]

        readable = 0
        unreadable = 0

        for image_path in image_files:
            try:
                with Image.open(image_path) as image:
                    image.verify()
                readable += 1
            except Exception:
                unreadable += 1

        total_images += len(image_files)
        total_readable += readable
        total_unreadable += unreadable

        line = (
            f"{folder.name}: {len(image_files)} images, "
            f"{readable} readable, {unreadable} unreadable"
        )

        print(line)
        summary_lines.append(line)

    summary_lines.extend([
        "",
        f"Total classes: {len(class_folders)}",
        f"Total images: {total_images}",
        f"Readable images: {total_readable}",
        f"Unreadable images: {total_unreadable}"
    ])

    SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_FILE.write_text(
        "\n".join(summary_lines),
        encoding="utf-8"
    )

    print("\n" + "=" * 45)
    print("Total classes:", len(class_folders))
    print("Total images:", total_images)
    print("Readable images:", total_readable)
    print("Unreadable images:", total_unreadable)
    print("\nSummary saved to:")
    print(SUMMARY_FILE)

    
import json

MAPPING_FILE = BASE_DIR / "class_mapping.json"

if PLANTVILLAGE_DIR.exists() and MAPPING_FILE.exists():
    with open(MAPPING_FILE, "r", encoding="utf-8") as file:
        class_mapping = json.load(file)

    actual_classes = {
        folder.name
        for folder in PLANTVILLAGE_DIR.iterdir()
        if folder.is_dir()
    }

    mapped_classes = set(class_mapping.keys())

    missing = actual_classes - mapped_classes
    extra = mapped_classes - actual_classes

    print("\nClass Mapping Verification")
    print("=" * 30)
    print("Dataset classes:", len(actual_classes))
    print("Mapped classes:", len(mapped_classes))
    print("Missing mappings:", missing or "None")
    print("Extra mappings:", extra or "None")

    if not missing and not extra:
        print("SUCCESS: All class names match!")
    else:
        print("Please check the class_mapping.json file.")


import shutil

PROCESSED_DIR = BASE_DIR / "data" / "processed" / "standardized"

if PLANTVILLAGE_DIR.exists() and MAPPING_FILE.exists():
    with open(MAPPING_FILE, "r", encoding="utf-8") as file:
        class_mapping = json.load(file)

    print("\nCreating standardized dataset...")

    for original_name, clean_name in class_mapping.items():
        source_folder = PLANTVILLAGE_DIR / original_name
        destination_folder = PROCESSED_DIR / clean_name
        destination_folder.mkdir(parents=True, exist_ok=True)

        copied = 0

        for image_path in source_folder.iterdir():
            if (
                image_path.is_file()
                and image_path.suffix.lower() in IMAGE_EXTENSIONS
            ):
                destination_path = destination_folder / image_path.name

                if not destination_path.exists():
                    shutil.copy2(image_path, destination_path)
                    copied += 1

        print(f"{clean_name}: copied {copied} images")

    print("\nStandardized dataset saved to:")
    print(PROCESSED_DIR)


    
print("\nVerifying standardized dataset...")

verified_total = 0
verified_classes = 0

for folder in sorted(PROCESSED_DIR.iterdir()):
    if folder.is_dir():
        count = sum(
            1 for file in folder.iterdir()
            if file.is_file()
            and file.suffix.lower() in IMAGE_EXTENSIONS
        )
        print(f"{folder.name}: {count} images")
        verified_total += count
        verified_classes += 1

print("\nStandardized classes:", verified_classes)
print("Standardized images:", verified_total)

if verified_classes == 15 and verified_total == 20638:
    print("SUCCESS: All images were copied!")
else:
    print("CHECK NEEDED: The counts do not match.")

