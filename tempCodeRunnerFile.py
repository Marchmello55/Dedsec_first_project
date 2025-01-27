from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image, UnidentifiedImageError
import torch
from googletrans import Translator
import os
from concurrent.futures import ThreadPoolExecutor


# Загрузка процессора и модели BLIP
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")  # Улучшенная модель
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

# Ускорение: использование GPU, если доступно
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Функция для корректировки пути
def normalize_path(path):
    """Заменяет символы '\' на '/' в пути."""
    return path.replace("\\", "/")

# Функция для генерации описания
def generate_caption(image_path):
    try:
        # Загрузка и уменьшение изображения
        try:
            image = Image.open(image_path).convert("RGB")
            image = image.resize((512, 512))  # Уменьшение размера изображения
        except UnidentifiedImageError:
            raise RuntimeError(f"Формат файла {image_path} не поддерживается.")

        # Предобработка изображения
        inputs = processor(images=image, return_tensors="pt").to(device)

        # Генерация текста
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_length=50,  # Увеличенная длина описания
                num_beams=10,   # Больше лучей для улучшения результата
                repetition_penalty=1.2  # Устранение повторений
            )

        # Расшифровка токенов в текст
        caption = processor.decode(output[0], skip_special_tokens=True)

        # Убираем "There is"/"There are", если они есть
        if caption.lower().startswith("there is "):
            caption = caption[9:]
        elif caption.lower().startswith("there are "):
            caption = caption[10:]

        # Удаляем повторения в тексте
        words = caption.split()
        caption = " ".join(dict.fromkeys(words))  # Удаление повторяющихся слов

        return caption
    except Exception as e:
        raise RuntimeError(f"Ошибка при обработке изображения: {e}")

# Перевод текста на русский язык
def translate_to_russian(text):
    try:
        translator = Translator()
        translation = translator.translate(text, src="en", dest="ru")
        return translation.text.capitalize()
    except Exception as e:
        raise RuntimeError(f"Ошибка при переводе текста: {e}")

# Получение пути к изображению
def get_image_path(file_path):
    while True:
        image_path = file_path.strip()
        image_path = normalize_path(image_path)  # Нормализация пути
        if os.path.isfile(image_path):
            return image_path
        print("Ошибка: указанный путь не существует. Попробуйте снова.")

# Основной блок
def main(file_path):
    try:
        # Получаем путь к изображению
        image_path = get_image_path(file_path)

        # Генерация описания
        description = generate_caption(image_path)

        # Параллельный перевод
        with ThreadPoolExecutor() as executor:
            future = executor.submit(translate_to_russian, description)
            description_russian = future.result()

        return(description_russian)
    except Exception as e:
        print(f"Ошибка: {e}")

# Запуск программы

