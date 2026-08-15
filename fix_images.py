import os
from PIL import Image

DATASET_PATH = "dataset"

print("🔧 Fixing images...\n")

for person in os.listdir(DATASET_PATH):
    person_path = os.path.join(DATASET_PATH, person)

    if not os.path.isdir(person_path):
        continue

    print(f"📂 Fixing: {person}")

    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)

        try:
            img = Image.open(img_path)

            # Convert to RGB (removes alpha, fixes format)
            img = img.convert("RGB")

            # Save clean image
            img.save(img_path, "JPEG")

        except Exception as e:
            print(f"❌ Failed: {img_name} → {e}")

print("\n✅ All images fixed!")