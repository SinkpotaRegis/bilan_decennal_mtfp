from app import create_app
from app.models.database import db
from sqlalchemy import text

app = create_app()
ctx = app.app_context()
ctx.push()

result = db.session.execute(text("PRAGMA table_info(kpis)"))
print("=== COLONNES DE LA TABLE KPIS ===")
for col in result:
    print(f"  - {col[1]}")

exit()