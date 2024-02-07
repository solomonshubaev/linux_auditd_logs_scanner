from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

from dataclasses_json import DataClassJsonMixin

from utils.datetime_utils import DatetimeUtils


@dataclass
class AuditLog(DataClassJsonMixin):
    type: Optional[str] = None
    msg: Optional[str] = None
    pid: Optional[int] = None
    ses: Optional[int] = None
    uid: Optional[int] = None
    res: Optional[str] = None
    target: Optional[str] = None
    subj: Optional[str] = None
    fd: Optional[int] = None
    syscall: Optional[str] = None
    auid: Optional[int] = None
    comm: Optional[str] = None
    exe: Optional[str] = None
    path: Optional[str] = None
    name: Optional[str] = None
    key: Optional[str] = None
    msg_audit_datetime: Optional[datetime] = None
    msg_audit_unique_id: Optional[int] = None

    def __post_init__(self):
        self.pid = int(self.pid) if self.pid else None
        self.ses = int(self.ses) if self.ses else None
        self.uid = int(self.uid) if self.uid else None
        self.auid = int(self.auid) if self.auid else None
        self.fd = int(self.fd) if self.fd else None
        self.msg_audit_datetime, self.msg_audit_unique_id = self._extract_audit()

    def is_same_as(self, other_audit_log: 'AuditLog') -> bool:
        self_attributes: dict = vars(self)
        other_attributes: dict = vars(other_audit_log)
        return ((len(self_attributes) == len(other_attributes)) and
                any(self_attributes[attr] == other_attributes[attr] for attr in self_attributes if attr not in ['id']))

    def _extract_audit(self) -> Tuple[Optional[datetime], Optional[int]]:
        start_index = self.msg.find('(')
        end_index = self.msg.find(')')
        if start_index == end_index:
            return None, None
        timestamp, unique_id = self.msg[start_index + 1:end_index].split(':')
        return DatetimeUtils.str_timestamp_to_datetime(timestamp), int(unique_id)
