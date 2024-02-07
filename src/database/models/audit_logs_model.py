from sqlalchemy import Column, String, JSON, DateTime, Integer, BIGINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from entities.auditd_log import AuditLog

Base = declarative_base()


class AuditLogsModel(Base):
    __tablename__ = 'audit_logs'

    id = Column(VARCHAR(36), primary_key=True)
    type = Column(VARCHAR(255), index=True)
    msg = Column(VARCHAR(255))
    pid = Column(Integer)
    ses = Column(BIGINT)
    uid = Column(Integer)
    res = Column(VARCHAR(255))
    target = Column(VARCHAR(255))
    subj = Column(VARCHAR(255))
    fd = Column(Integer)
    syscall = Column(VARCHAR(255))
    auid = Column(BIGINT, index=True)
    comm = Column(VARCHAR(255), index=True)
    exe = Column(VARCHAR(255), index=True)
    path = Column(VARCHAR(255), index=True)
    name = Column(VARCHAR(255), index=True)
    key = Column(VARCHAR(255), index=True)
    msg_audit_datetime = Column(DateTime, index=True)
    msg_audit_unique_id = Column(Integer, index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    def to_entity(self) -> AuditLog:
        return AuditLog(
            type=self.type,
            msg=self.msg,
            pid=self.pid,
            ses=self.ses,
            uid=self.uid,
            res=self.res,
            target=self.target,
            subj=self.subj,
            fd=self.fd,
            syscall=self.syscall,
            auid=self.auid,
            comm=self.comm,
            exe=self.exe,
            path=self.path,
            name=self.name,
            key=self.key,
            msg_audit_datetime=self.msg_audit_datetime,
            msg_audit_unique_id=self.msg_audit_unique_id
        )
