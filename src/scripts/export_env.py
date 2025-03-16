import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def export_env():
    ENV_FILE = os.path.join(BASE_DIR, '.env')
    print(f"ENV FILE PATH:\t{ENV_FILE}")
    with open(ENV_FILE) as file:
        for line in file:
            # print(f"LINE:\t{line}")
            if line.startswith('##') or line.startswith("#"):
                # print("Comment Line.")
                continue
            elif not line.startswith("##"):
                key, value = line.replace('"', "").replace("'", "").strip().split(" = ", 1)
                print(f"{key}:\t{value}")
                os.environ[key] = value
            elif line.startswith("") or line.startswith(" ") or line.startswith("\n") or line.startswith("\t"):
                # print("Blank Line.")
                continue
    
    for key in os.environ:
        print(f"{key}:\t{os.getenv(key)}")

if __name__=="__main__":
    export_env()