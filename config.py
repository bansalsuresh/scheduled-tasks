from pathlib import Path


class Config:
    _config = None

    @staticmethod
    def read_config():
        if Config._config is not None:
            return Config._config

        config = {}
        config_path = Path(__file__).with_name("config.cfg")

        for line in config_path.read_text().splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

        Config._config = config
        return Config._config
