import logging
from dataclasses import dataclass, field
from typing import Dict

from database.db_methods.audit_logs_db_method import AuditLogsDbMethods
from entities.auditd_log import AuditLog


@dataclass
class AuditLogManager:
    _instance = None
    unique_id_to_audit_map: Dict[int, list[AuditLog]] = field(default_factory=lambda: {})

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def add_audit_log_to_dict(self, audit_log: AuditLog) -> None:
        # if audit_log.msg_audit_unique_id == 304034:
        #     return
        # else:
        #     print('****************************************** ', audit_log.msg_audit_unique_id)
        # todo: maybe hashmap can help here (check if have time), hashmap on several fields
        self.unique_id_to_audit_map[audit_log.msg_audit_unique_id] = self.unique_id_to_audit_map.get(
            audit_log.msg_audit_unique_id, [])
        if not self._is_audit_log_already_exist_in_db(audit_log):
            # RawDataDbMethods.insert_raw_date(audit_log.to_dict())  # todo: better todo in bulk if have time
            self.unique_id_to_audit_map[audit_log.msg_audit_unique_id].append(audit_log)
        else:
            logging.warning(f'audit already exist: {audit_log=}')

    def add_logs_from_dict_to_db_in_bulk(self):
        logging.info(f'Adding {len(self.unique_id_to_audit_map.keys())} audit log events')
        for key in self.unique_id_to_audit_map.keys():
            AuditLogsDbMethods.insert_audit_logs_from_same_event(self.unique_id_to_audit_map.get(key, []))
        logging.info(f'Inserted bulk of audit logs, emptying dict...')
        self.unique_id_to_audit_map = {}

    # def _is_audit_log_already_exist(self, audit_log_to_insert: AuditLog) -> bool:
    #     return any(audit.is_same_as(audit_log_to_insert)
    #                for audit in self.unique_id_to_audit_map.get(audit_log_to_insert.msg_audit_unique_id, []))

    @staticmethod
    def _is_audit_log_already_exist_in_db(audit_log_to_insert: AuditLog) -> bool:
        return any(audit_log_to_insert.is_same_as(audit)
                   for audit in AuditLogsDbMethods.list_same_audit_logs(audit_log_to_insert))
