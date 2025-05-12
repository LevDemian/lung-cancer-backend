import os
from PIL import Image

image_dir = "../data/train/images"
mask_dir = "../data/train/masks"

os.makedirs(mask_dir, exist_ok=True)

for filename in os.listdir(image_dir):
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    filepath = os.path.join(image_dir, filename)

    # Считаем, что "aca" = опухоль, "n" = норма
    name_lower = filename.lower()
    if "aca" in name_lower:
        # Белая маска для опухоли
        mask = Image.new("L", (512, 512), color=255)
    elif "n" in name_lower:
        # Чёрная маска для нормы
        mask = Image.new("L", (512, 512), color=0)
    else:
        print(f"Пропущено: {filename}")
        continue

    mask.save(os.path.join(mask_dir, filename))

print("✅ Маски успешно созданы.")
