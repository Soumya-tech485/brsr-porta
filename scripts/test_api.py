import httpx

# 1. Login to get token
resp = httpx.post("http://127.0.0.1:8000/auth/login", json={"email": "admin@meil.com", "password": "password123"})
if resp.status_code != 200:
    print("Login failed:", resp.status_code, resp.text)
    exit(1)

token = resp.json()["access_token"]
print("Got token.")

# 2. Fetch dashboard
resp = httpx.get("http://127.0.0.1:8000/admin/dashboard?period_id=1", headers={"Authorization": f"Bearer {token}"})
print("Dashboard status:", resp.status_code)
if resp.status_code != 200:
    print("Dashboard error:", resp.text)
else:
    print("Dashboard data:", resp.json())
