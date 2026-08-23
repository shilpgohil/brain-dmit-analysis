import sys
sys.path.insert(0, 'backend')
from api.main import app
print('App imports OK')
from api.db.connection import get_conn
conn = get_conn()
tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print('Tables:', sorted(tables))
