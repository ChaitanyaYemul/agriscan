
from pathlib import Path
import random
import shutil

BASE_DIR = Path(__file__).resolve().parent

SOURCE_DIR = BASE_DIR / "data" / "processed" / "standardized"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "split"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

random.seed(42)

if not SOURCE_DIR.exists():
    print("ERROR: Standardized dataset folder not found!")
    raise SystemExit(1)

if abs(TRAIN_RATIO + VAL_RATIO + TEST_RATIO - 1.0) > 0.001:
    print("ERROR: Split ratios must add up to 1.")
    raise SystemExit(1)

class_folders = sorted(
    folder for folder in SOURCE_DIR.iterdir()
    if folder.is_dir()
)

if not class_folders:
    print("ERROR: No class folders found!")
    raise SystemExit(1)

print("Creating train/validation/test split...")

for class_folder in class_folders:
    images = sorted(
        file for file in class_folder.iterdir()
        if file.is_file()
        and file.suffix.lower() in IMAGE_EXTENSIONS
    )

    random.shuffle(images)

    total = len(images)
    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    split_groups = {
        "train": images[:train_end],
        "val": images[train_end:val_end],
        "test": images[val_end:]
    }

    for split_name, split_images in split_groups.items():
        destination = OUTPUT_DIR / split_name / class_folder.name
        destination.mkdir(parents=True, exist_ok=True)

        for image_path in split_images:
            shutil.copy2(image_path, destination / image_path.name)

    print(
        f"{class_folder.name}: "
        f"train={len(split_groups['train'])}, "
        f"val={len(split_groups['val'])}, "
        f"test={len(split_groups['test'])}"
    )

print("\nDataset splitting complete!")
print("Output folder:", OUTPUT_DIR)
print("Splits: train, val, test")



print("\nFinal Dataset Split Verification")
print("=" * 35)

grand_total = 0

for split_name in ["train", "val", "test"]:
    split_path = OUTPUT_DIR / split_name
    split_total = 0

    for class_folder in split_path.iterdir():
        if class_folder.is_dir():
            split_total += sum(
                1 for file in class_folder.iterdir()
                if file.is_file()
                and file.suffix.lower() in IMAGE_EXTENSIONS
            )

    grand_total += split_total
    print(f"{split_name}: {split_total} images")

print("-" * 35)
print("Total images:", grand_total)

if grand_total == 20638:
    print("SUCCESS: All 20,638 images are accounted for!")
else:
    print("CHECK NEEDED: Expected 20,638 images.")
