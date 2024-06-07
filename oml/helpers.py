from dataclasses import dataclass, field, asdict, fields
from typing import Optional, Dict, Any, List
from oml.model_metadata import ModelMetadata
from oras.provider import Registry
from oml.provider import OMLRegistry
import os

def write_content_to_file(filename: str, content_fn):
    try:
        with open(filename, 'x') as f:
            content = content_fn()
            f.write(content)
    except FileExistsError:
        raise RuntimeError(f"File '{filename}' already exists. Aborting TODO: demonstrator.")


def push(
    target: str,
    path: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    author: Optional[str] = None,
    model_format_name: Optional[str] = None,
    model_format_version: Optional[str] = None,
    **kwargs
):
    dataclass_fields = {f.name for f in fields(ModelMetadata)} # avoid anything specified in kwargs which would collide
    custom_properties = {k: v for k, v in kwargs.items() if k not in dataclass_fields}
    model_metadata = ModelMetadata(
        name=name,
        description=description,
        author=author,
        customProperties=custom_properties,
        model_format_name=model_format_name,
        model_format_version=model_format_version
    )
    write_content_to_file("model_metadata.oml.json", lambda: model_metadata.to_json())
    write_content_to_file("model_metadata.oml.yaml", lambda: model_metadata.to_yaml())
    files = [
        f"{path}:application/x-artifact",
        "model_metadata.oml.json:application/x-config",
        "model_metadata.oml.yaml:application/x-config",
    ]
    registry = Registry(insecure=True)
    registry.push(
        target=target,
        files=files,
        manifest_config="model_metadata.oml.json:application/x-config"
    )
    os.remove("model_metadata.oml.json")
    os.remove("model_metadata.oml.yaml")
    return None


def pull(
    target: str,
    outdir: str,
    media_types: List[str]
):
    registry = OMLRegistry(insecure=True)
    registry.download_layers(target, outdir, media_types)


def get_config(
    target: str
) -> str:
    registry = OMLRegistry(insecure=True)
    return f'{{"reference":"{target}", "config": {registry.get_config(target)} }}' # this assumes OCI Manifest.Config later is JSON (per std spec)


def crawl(
    targets: List[str]
) -> str:
    configs = map(get_config, targets)
    joined = "[" + ", ".join(configs) + "]"
    return joined
