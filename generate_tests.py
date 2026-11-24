import argparse
import requests
import sys

def generate_scenarios(num_scenarios):
    # Промпт для модели
    prompt = f"""
    Ты — опытный QA-инженер. Напиши ровно {num_scenarios} тестовых сценариев для формы регистрации.
    Поля формы: 
    1. Ввод имени пользователя (логин).
    2. Ввод пароля.
    3. Поле ввода подтверждения пароля.
    4. Кнопка «Зарегистрировать».

    Обязательно включи как позитивные сценарии (успешная регистрация), так и негативные (несовпадение паролей, пустые поля, слишком короткий пароль и т.д.).
    Оформи результат в формате Markdown. Используй заголовки (## Сценарий 1...) и списки шагов.
    Не пиши ничего лишнего, только Markdown с тест-кейсами.
    """

    # Адрес локального сервера Ollama
    url = "http://localhost:11434/api/generate"
    
    # Настройки запроса
    data = {
        "model": "qwen3.5:4b",  # Имя вашей скачанной модели
        "prompt": prompt,
        "stream": False         # Ждем ответ целиком
    }

    print(f"Генерирую {num_scenarios} сценариев. Пожалуйста, подождите, модели нужно время...")
    
    try:
        # Отправляем запрос к Ollama
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        # Извлекаем текст ответа
        result = response.json()["response"]
        return result
        
    except requests.exceptions.ConnectionError:
        print("ОШИБКА: Не удается подключиться к Ollama. Убедитесь, что приложение запущено.")
        sys.exit(1)

if __name__ == "__main__":
    # Настраиваем прием аргументов из командной строки
    parser = argparse.ArgumentParser(description="Генератор тест-кейсов с помощью нейросети")
    parser.add_argument("--count", type=int, default=5, help="Количество генерируемых сценариев")
    args = parser.parse_args()

    # Вызываем функцию генерации
    markdown_content = generate_scenarios(args.count)

    # Сохраняем в файл
    filename = "test_scenarios.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print(f"✅ Готово! Сценарии сохранены в файл: {filename}")