#!/bin/env python
import sqlite3
import csv

# Konfiguracja
DB_NAME = 'nomos.db'
PREDICATES_CSV = 'predicates.csv'
QUESTIONS_CSV = 'questions.csv'

def create_database():
    """Tworzy bazę danych i tabele."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tworzenie tabel
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS predicates (
            predicate_id VARCHAR(50) PRIMARY KEY,
            category VARCHAR(100),
            logic_expression TEXT NOT NULL,
            short_answer TEXT
        );

        CREATE TABLE IF NOT EXISTS questions (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            intent TEXT
        );

        CREATE TABLE IF NOT EXISTS question_predicate_mapping (
            question_id INTEGER,
            predicate_id VARCHAR(50),
            PRIMARY KEY (question_id, predicate_id),
            FOREIGN KEY (question_id) REFERENCES questions (question_id),
            FOREIGN KEY (predicate_id) REFERENCES predicates (predicate_id)
        );
    ''')
    conn.commit()
    conn.close()

def load_data():
    """Ładuje dane z plików CSV do bazy."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Ładowanie predykatów
    try:
        with open(PREDICATES_CSV, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row)
                cursor.execute('''
                    INSERT OR IGNORE INTO predicates (predicate_id, category, logic_expression, short_answer)
                    VALUES (?, ?, ?, ?)
                ''', (row['predicate_id'].strip(), row['category'].strip(), row['logic_expression'].strip(), row['short_answer'].strip()))
        print("Załadowano predykaty.")
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {PREDICATES_CSV}.")

    # 2. Ładowanie pytań i mapowania
    try:
        with open(QUESTIONS_CSV, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row)
                # Wstawienie pytania do tabeli 'questions'
                cursor.execute('''
                    INSERT INTO questions (question_text, intent)
                    VALUES (?, ?)
                ''', (row['question_text'].strip(), row['intent'].strip()))
                
                # Pobranie ID nowo wstawionego pytania
                question_id = cursor.lastrowid
                
                # Przetwarzanie predykatów (rozdzielenie po przecinku i usunięcie spacji)
                predicates_raw = row['mapped_predicates']
                predicate_list = [p.strip() for p in predicates_raw.split(',') if p.strip()]
                
                # Wstawienie relacji do tabeli mapującej
                for pred_id in predicate_list:
                    cursor.execute('''
                        INSERT OR IGNORE INTO question_predicate_mapping (question_id, predicate_id)
                        VALUES (?, ?)
                    ''', (question_id, pred_id))
        print("Załadowano pytania i utworzono relacje.")
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {QUESTIONS_CSV}.")

    conn.commit()
    conn.close()
    print("Zasilanie bazy zakończone sukcesem.")

if __name__ == '__main__':
#    create_database()
    load_data()
