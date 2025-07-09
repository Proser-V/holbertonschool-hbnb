import subprocess

test_files = [
    "test_users_req.py",
    "test_amenities_req.py",
    "test_places_req.py"
]

for file in test_files:
    try:
        subprocess.run(["python3", file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ {file} failed with return code {e.returncode}")
