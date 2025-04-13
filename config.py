import argparse

# def update_env_var_in_dotenv(env_var: str, value: str, filepath: str = ".env") -> str:
#     """Update or add a new environment variable to the .env file"""

#     env_vars = {}
#     try:
#         with open(filepath, "r") as file:
#             for line in file:
#                 line = line.strip()
#                 if line and not line.startswith("#"):
#                     key, val = line.split("=", 1)
#                     env_vars[key] = val
#     except FileNotFoundError:
#         pass

#     env_vars[env_var] = value

#     with open(filepath, "w") as file:
#         for key, val in env_vars.items():
#             file.write(f"{key}={val}\n")

#     return value

def update_telegram_keys_in_dotenv(api_id: str, api_hash: str, filepath: str = ".env") -> None:
    """Update or add a new environment variable to the .env file"""

    env_vars = {}
    try:
        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    env_vars[key] = val
    except FileNotFoundError:
        pass

    env_vars["TELEGRAM_API_ID"] = api_id
    env_vars["TELEGRAM_API_HASH"] = api_hash

    with open(filepath, "w") as file:
        for key, val in env_vars.items():
            file.write(f"{key}={val}\n")

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-id",
        "--api_id",
        required=True,
        help="Enter your telegram API ID",
    )
    parser.add_argument(
        "-hash",
        "--api_hash",
        required=True,
        help="Enter your telegram API hash",
    )

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = setup_args()
    update_telegram_keys_in_dotenv(args.api_id, args.api_hash)