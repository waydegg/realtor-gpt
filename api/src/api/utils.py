from typing import Dict


def filter_null_params(params: Dict):
    return {k: v for k, v in params.items() if v is not None}
