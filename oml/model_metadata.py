from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
import json
import yaml

@dataclass
class ModelMetadata:
    name: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    customProperties: Optional[Dict[str, Any]] = field(default_factory=dict)
    uri: Optional[str] = None
    model_format_name: Optional[str] = None
    model_format_version: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=4)

    @staticmethod
    def from_json(json_str: str) -> 'ModelMetadata':
        data = json.loads(json_str)
        return ModelMetadata(**data)

    def to_yaml(self) -> str:
        return yaml.dump(asdict(self), default_flow_style=False)

    @staticmethod
    def from_yaml(yaml_str: str) -> 'ModelMetadata':
        data = yaml.safe_load(yaml_str)
        return ModelMetadata(**data)
