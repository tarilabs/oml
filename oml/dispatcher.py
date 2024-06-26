from dataclasses import dataclass, field, asdict, fields
from typing import Optional, Dict, Any, List
from oml.helpers import Helper
from collections import namedtuple

PushThenMRResult = namedtuple('PushThenMRResult', ['push_sha', 'mr_result'])

class Dispatcher:
    def __init__(self, helper: Helper, model_registry):
        self._helper = helper
        try:
            from model_registry import ModelRegistry
            if not isinstance(model_registry, ModelRegistry):
                msg = "this optional component requires Model Registry"
                raise ValueError(msg)
            self._model_registry = model_registry
        except:
            msg = "this optional component requires Model Registry"
            raise RuntimeError(msg)
        
    def push_then_model_registry(
            self,
            target: str,
            path: str,
            name: str,
            description: Optional[str] = None,
            author: Optional[str] = None,
            model_format_name: Optional[str] = None,
            model_format_version: Optional[str] = None,
            **kwargs
        ):
        params = {k: v for k, v in locals().items() if k != 'self'}
        push_result = self._helper.push(**params)
        push_sha = push_result.headers["Docker-Content-Digest"]
        print("push_sha is:", push_sha)
        mr_result = self._model_registry.register_model(
            name=name,
            uri=target,
            version=push_sha,
            metadata=kwargs,
            description=description,
            author=author,
            model_format_name=model_format_name,
            model_format_version=model_format_version
        )
        return PushThenMRResult(push_sha, mr_result)