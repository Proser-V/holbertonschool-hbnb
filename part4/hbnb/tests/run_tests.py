"""
This module launch automated tests.
"""


import subprocess

print("🔁 Initialising test DB with admin...")
try:
    subprocess.run("sqlite3 ../instance/testDB.db '.read init_admin.sql'",
                   shell=True, check=True)
    print("✅ Admin inserted into DB")
except subprocess.CalledProcessError as e:
    print(f"❌ Failed to insert admin: {e}")
    exit(1)

test_files = [
    "test_users_req.py",
    "test_amenities_req.py",
    "test_places_req.py"
]

for file in test_files:
    try:
        print(f"\n🚀 Running {file}")
        subprocess.run(["python3", file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ {file} failed with return code {e.returncode}")
