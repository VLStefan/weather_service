from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Type

def _prepare_obj(
    record: Dict[str, Any], data_model: Type[BaseModel]
) -> Optional[Dict[str, Any]]:
    return data_model.parse_obj(record).dict() if record else None


def _prepare_list(
    query_result: List[Dict[str, Any]], data_model: Type[BaseModel],
) -> List[Optional[Dict[str, Any]]]:
    return [_prepare_obj(record, data_model) for record in query_result] if query_result else query_result
