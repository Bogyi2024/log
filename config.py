import os

# Get environment variables from GitHub Actions
setting_content = os.environ.get("SETTING_CONTENT")
setting_content_2 = os.environ.get("SETTING_CONTENT_2")

# Ensure directory exists
os.makedirs("core/settings", exist_ok=True)

# Write general.cfg
if setting_content:
    with open("core/settings/general.cfg", "w", encoding="utf-8") as f:
        f.write(setting_content)
    print("--- general.cfg contents ---")
    print(setting_content)
    print("----------------------------")

# Write custom.cfg
if setting_content_2:
    with open("core/settings/custom.cfg", "w", encoding="utf-8") as f:
        f.write(setting_content_2)
    print("--- custom.cfg contents ---")
    print(setting_content_2)
    print("---------------------------")
