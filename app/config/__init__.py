from os.path import join
from configparser import ConfigParser

from . import models


def test_config() -> None:
    from app import BASE_DIR

    for section in models.__all__:
        filename = section.lower() + ".ini"

        tmp = ConfigParser()
        tmp.read(join(BASE_DIR, "config", filename), encoding="utf-8")

        if not tmp.has_section(section):
            reset = ConfigParser()
            reset.add_section(section)

            for field in getattr(getattr(models, section), "_fields"):
                reset.set(
                    section=section,
                    option=field,
                    value="#"
                )

            with open(join(BASE_DIR, "config", filename), mode="w", encoding="utf-8") as configInit:
                reset.write(configInit)


def get_config(model_name: str):
    from app import BASE_DIR

    if model_name not in models.__all__:
        raise KeyError("FailToLoadConfig: unregistered config model")

    filename = model_name.lower() + ".ini"

    config = ConfigParser()
    config.read(join(BASE_DIR, "config", filename), encoding="utf-8")

    import_result = []
    for field in getattr(getattr(models, model_name), "_fields"):
        import_result.append(
            config.get(
                section=model_name,
                option=field,
                fallback="#"
            )
        )

    return getattr(models, model_name)(*import_result)


def update_config(model_name: str, model: object) -> bool:
    from app import BASE_DIR

    if model_name not in models.__all__:
        raise KeyError("FailToLoadConfig: unregistered config model")

    filename = model_name.lower() + ".ini"

    config = ConfigParser()
    config.add_section(model_name)

    for field in getattr(getattr(models, model_name), "_fields"):
        config.set(
            section=model_name,
            option=field,
            value=getattr(model, field)
        )

    with open(join(BASE_DIR, "config", filename), mode="w", encoding="utf-8") as configUpdate:
        config.write(configUpdate)

    return True
