# migrate_db.py
import sqlite3
import os

db_path = 'instance/bilan_decennal.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

colonnes_a_ajouter = [
    ('is_active', 'BOOLEAN DEFAULT 1'),
    ('direction', 'VARCHAR(100)'),
    ('last_login', 'DATETIME'),
    ('created_by', 'INTEGER')
]

for col, col_type in colonnes_a_ajouter:
    try:
        cursor.execute(f'ALTER TABLE users ADD COLUMN {col} {col_type}')
        print(f'✅ Colonne {col} ajoutée')
    except Exception as e:
        if 'duplicate column' in str(e).lower():
            print(f'ℹ️ Colonne {col} existe déjà')
        else:
            print(f'❌ Erreur pour {col}: {e}')

conn.commit()
conn.close()
print('🎉 Migration terminée !')    