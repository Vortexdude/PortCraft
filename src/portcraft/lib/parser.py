from pathlib import Path


def _file_parser(filename, base_path=None) -> str:
    if not base_path:
        slug = Path("./") / filename
    else:
        if isinstance(base_path, Path):
            slug = base_path / filename
        else:
            raise Exception(f"'{base_path}' is not Path like object")

    return slug.resolve()
