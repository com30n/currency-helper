from uvicorn import run

from server import get_app
from src.utils.config import get_config_path, load_config


def main() -> None:
    config_path = get_config_path()
    config = load_config(config_path)

    app = get_app(config)

    run(
        app,
        host=config["app"]["host"],
        port=config["app"]["port"],
    )


if __name__ == "__main__":
    main()
