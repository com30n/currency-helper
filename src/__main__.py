from uvicorn import run

from src.utils.config import get_config_path, load_config


def main() -> None:
    config_path = get_config_path()
    config = load_config(config_path)

    run(
        "src.server:get_app",
        host=config["app"]["host"],
        port=config["app"]["port"],
        workers=config["app"]["workers"],
        reload=config["app"].get("dev", False),
    )


if __name__ == "__main__":
    main()
