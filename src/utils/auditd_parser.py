import json
import logging
from abc import ABC
from sre_constants import ANY
from typing import Dict, Tuple


class AuditParser(ABC):

    @staticmethod
    def parse_audit_to_dict(audit_log: str) -> dict:
        audit_dict: dict = {}
        audit_log = audit_log.replace(chr(29), ' ')
        audit_log = audit_log.replace('\n', '')
        for part in audit_log.split(' '):
            split_result: list[str] = part.split('=')
            if len(split_result) == 2:
                key, value = split_result
                audit_dict[key] = AuditParser.convert_to_original_value(value)
            # elif len(split_result) > 2:
            #     logging.warning(f"More than one '=' found in '{part}', skipping.")
            # else:
            #     logging.warning(f"No '=' found in '{part}', skipping.")
        return audit_dict

    @staticmethod
    def convert_to_original_value(value: str) -> ANY:
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            return value
