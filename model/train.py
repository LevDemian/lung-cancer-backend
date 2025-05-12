import os
import torch
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
from unet_model import UNet
from dataset_preparation import DummyLungDataset

# Папки с изображениями и масками
image_dir = "../data/train/images"
mask_dir = "../data/train/masks"

# Преобразования изображений
transform = transforms.Compose([
    transforms.Resize((512, 512)),
    transforms.ToTensor()
])

# Датасет и загрузчик
dataset = DummyLungDataset(image_dir, mask_dir, transform=transform)
loader = DataLoader(dataset, batch_size=2, shuffle=True)

# Модель, функция потерь, оптимизатор
model = UNet(in_channels=3)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Обучение
for epoch in range(3):  # 3 эпохи для начала
    model.train()
    total_loss = 0
    for images, masks in loader:
        preds = model(images)
        loss = criterion(preds, masks)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Эпоха {epoch+1}, Потери: {total_loss:.4f}")

# Сохраняем модель
torch.save(model.state_dict(), "../model/model.pth")
print("✅ Модель сохранена как model.pth")
