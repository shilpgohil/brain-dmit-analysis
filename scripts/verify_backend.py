import sys
sys.path.insert(0, 'backend')
for name, mod in [("sessions", "api.routes.sessions"), ("analysis", "api.routes.analysis"), ("main", "api.main")]:
    try:
        import importlib
        importlib.import_module(mod)
        print(f"OK {name}")
    except Exception as e:
        print(f"ERR {name}: {e}")
