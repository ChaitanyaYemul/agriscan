
# AgriScan Disease Detection Dataset

## Dataset source
PlantVillage dataset.

## Dataset overview
- Crops: Tomato, Potato, and Bell Pepper
- Total classes: 15
- Total images: 20,638
- Unreadable images detected during initial inspection: 0

## Dataset split

| Split | Image count | Approximate percentage |
|---|---:|---:|
| Train | 14,440 | 69.97% |
| Validation | 3,089 | 14.97% |
| Test | 3,109 | 15.06% |
| Total | 20,638 | 100% |

## Dataset folders
- `data/raw/PlantVillage/`: Original dataset
- `data/processed/standardized/`: Standardized class folders
- `data/processed/split/train/`: Training images
- `data/processed/split/val/`: Validation images
- `data/processed/split/test/`: Testing images

## Supporting files
- `class_mapping.json`: Original-to-standardized class names
- `classes.json`: Model class labels
- `prepare_dataset.py`: Dataset inspection and preparation
- `split_dataset.py`: Train/validation/test splitting

## Notes
- All 15 original class folders matched the class mapping.
- The split verification confirmed that all 20,638 images are accounted for.
- Some classes have fewer images than others. Class imbalance should be considered during model training.
- PlantVillage images alone do not establish performance on real-world field photographs.
