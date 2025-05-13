import os

from dotenv import load_dotenv

ENVS = ["dev", "test", "prod"]


def setup_env(argv):
    if len(argv) == 1:
        # No environment passed → default to 'dev'
        env = "dev"
        print("No environment specified. Defaulting to 'dev' environment.")
    elif len(argv) == 2 and argv[1] in ENVS:
        env = argv[1]
    else:
        raise ValueError(
            f"Invalid or missing environment. Allowed values: {ENVS}. "
            "Example: python run_etl.py dev"
        )

    cleanup_previous_env()
    os.environ["ENV"] = env

    # Throw an error or load the appropriate .env file
    if env is None:
        raise KeyError("ENV variable not set")

    env_file = ".env" if env == "prod" else f".env.{env}"
    print(f"Loading environment variables from: {env_file}")

    load_dotenv(env_file, override=True)


def cleanup_previous_env():
    # Clear relevant environment variables
    keys_to_clear = [
        "WEATHER_API_KEY",
        "STOCK_API_KEY",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
        "DB_HOST",
        "DB_PORT",
    ]
    for key in keys_to_clear:
        if key in os.environ:
            del os.environ[key]
