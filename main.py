import pandas as pd
import psycopg2

# Настройки подключения к базе данных
db_config = {
    'dbname': 'postgres',  # Имя вашей базы данных
    'user': 'postgres',  # Ваше имя пользователя
    'password': 'postgres_oa',  # Ваш пароль
    'host': '10.159.8.163',  # Хост (например, localhost)
    'port': '5432'  # Порт (по умолчанию 5432)
}

# Создание подключения к базе данных
try:
    connection = psycopg2.connect(**db_config)
    print("Подключение к базе данных успешно установлено.")

    # SQL-запрос для извлечения данных
    query = "SELECT * FROM smp_razbor"  # Замените на ваш SQL-запрос

    # Загрузка данных в DataFrame
    df = pd.read_sql_query(query, connection)
    print("Данные успешно загружены в DataFrame.")

    # Вывод первых 5 строк DataFrame
    print(df.head())
    print(df.columns)

except Exception as e:
    print(f"Ошибка при подключении к базе данных: {e}")

finally:
    # Закрытие подключения
    if connection:
        connection.close()
        print("Подключение к базе данных закрыто.")
