import uuid
from abc import ABC
from datetime import datetime

from database.database import session_decorator
from database.models.audit_logs_model import AuditLogsModel
from entities.auditd_log import AuditLog


class AuditLogsDbMethods(ABC):

    @staticmethod
    @session_decorator
    def insert_audit_logs_from_same_event(session, audit_logs: list[AuditLog]) -> None:
        audit_logs_models: list[AuditLogsModel] = [AuditLogsModel(id=str(uuid.uuid4()),
                                                                  type=audit_log.type,
                                                                  msg=audit_log.msg,
                                                                  pid=audit_log.pid,
                                                                  ses=audit_log.ses,
                                                                  uid=audit_log.uid,
                                                                  res=audit_log.res,
                                                                  target=audit_log.target,
                                                                  subj=audit_log.subj,
                                                                  fd=audit_log.fd,
                                                                  syscall=audit_log.syscall,
                                                                  auid=audit_log.auid,
                                                                  comm=audit_log.comm,
                                                                  exe=audit_log.exe,
                                                                  path=audit_log.path,
                                                                  name=audit_log.name,
                                                                  key=audit_log.key,
                                                                  msg_audit_datetime=audit_log.msg_audit_datetime,
                                                                  msg_audit_unique_id=audit_log.msg_audit_unique_id,
                                                                  created_at=datetime.now(),  # Current datetime
                                                                  updated_at=datetime.now()  # Current datetime
                                                                  )
                                                   for audit_log in audit_logs]
        session.bulk_save_objects(audit_logs_models)
        session.commit()

    @staticmethod
    @session_decorator
    def list_same_audit_logs(session, audit_log: AuditLog) -> list[AuditLog]:
        audit_logs_models: list[AuditLogsModel] = (session.query(AuditLogsModel)
                                                   .filter(AuditLogsModel.type == audit_log.type)
                                                   .filter(AuditLogsModel.key == audit_log.key)
                                                   .filter(AuditLogsModel.msg_audit_datetime == audit_log.msg_audit_datetime)
                                                   .filter(AuditLogsModel.msg_audit_unique_id == audit_log.msg_audit_unique_id)
                                                   .filter(AuditLogsModel.auid == audit_log.auid)
                                                   .filter(AuditLogsModel.comm == audit_log.comm)
                                                   .filter(AuditLogsModel.exe == audit_log.exe)
                                                   .filter(AuditLogsModel.name == audit_log.name)
                                                   .all())
        if len(audit_logs_models) > 0:
            print(f'There are {len(audit_logs_models)} same logs as \n {audit_log=}\n\n')
        return [audit_model.to_entity() for audit_model in audit_logs_models]
