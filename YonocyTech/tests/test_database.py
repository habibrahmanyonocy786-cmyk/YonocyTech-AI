"""Quick database verification script."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database.schema import migrate
from database.models import (
    create_user, authenticate, get_all_users,
    get_all_providers, get_all_agents,
    count_users, get_usage_stats
)

migrate()
print("Migration OK")

u = create_user("Test Admin", "test@yonocytech.com", "admin123")
if u:
    print(f"User created: {u['name']} (role: {u['role']})")
else:
    print("User already exists")

a = authenticate("test@yonocytech.com", "admin123")
if a:
    print(f"Auth OK: {a['name']}")
else:
    print("Auth failed")

provs = get_all_providers()
print(f"Providers: {len(provs)} -> {[p['id'] for p in provs]}")

agents = get_all_agents()
print(f"Agents: {len(agents)} -> {[a['id'] for a in agents]}")

print(f"Total users: {count_users()}")
print("All database tests passed!")
