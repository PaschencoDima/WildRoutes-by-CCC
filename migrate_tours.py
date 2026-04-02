import sqlite3


def migrate_tours():
    conn = sqlite3.connect('db/blogs.sqlite')
    cursor = conn.cursor()

    # Получаем список существующих колонок
    cursor.execute("PRAGMA table_info(tours)")
    columns = [col[1] for col in cursor.fetchall()]

    # Добавляем недостающие колонки
    new_columns = {
        'images': 'TEXT',
        'organizer_type': 'TEXT DEFAULT "company"',
        'company_name': 'TEXT',
        'company_description': 'TEXT',
        'company_phone': 'TEXT',
        'company_email': 'TEXT',
        'company_website': 'TEXT'
    }

    for col_name, col_type in new_columns.items():
        if col_name not in columns:
            try:
                cursor.execute(f"ALTER TABLE tours ADD COLUMN {col_name} {col_type}")
                print(f"✓ Добавлена колонка: {col_name}")
            except sqlite3.OperationalError as e:
                print(f"✗ Ошибка при добавлении {col_name}: {e}")

    # Обновляем существующие записи: устанавливаем organizer_type = 'company' для туров без гида
    cursor.execute("UPDATE tours SET organizer_type = 'company' WHERE guide_id IS NULL AND organizer_type IS NULL")
    cursor.execute("UPDATE tours SET organizer_type = 'guide' WHERE guide_id IS NOT NULL AND organizer_type IS NULL")

    # Устанавливаем company_name по умолчанию
    cursor.execute(
        "UPDATE tours SET company_name = 'WildRoutes' WHERE company_name IS NULL AND organizer_type = 'company'")

    conn.commit()
    conn.close()
    print("Миграция завершена!")


if __name__ == "__main__":
    migrate_tours()