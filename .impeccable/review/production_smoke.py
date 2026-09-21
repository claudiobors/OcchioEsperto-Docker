from pathlib import Path
import sys
from fastapi.testclient import TestClient
root = Path.cwd()
sys.path.insert(0, str(root / 'backend'))
from app.main import app
client = TestClient(app)
routes = ['/', '/analisi', '/pricing', '/login', '/register', '/dashboard', '/terms', '/privacy', '/api/health']
assets = list((root / 'backend/static/assets').glob('*')) + list((root / 'backend/static/fonts').glob('*.ttf')) + list((root / 'backend/static/images').glob('*.webp'))
for route in routes:
    response = client.get(route)
    assert response.status_code == 200, (route, response.status_code)
    print('OK', route)
for asset in assets:
    route = '/static/' + asset.relative_to(root / 'backend/static').as_posix()
    response = client.get(route)
    assert response.status_code == 200 and len(response.content) == asset.stat().st_size, route
    assert 'text/html' not in response.headers.get('content-type', ''), route
    print('OK', route)
print('Production routes and assets verified; no account, database lifespan or payment mutation.')
