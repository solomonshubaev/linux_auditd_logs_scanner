import datetime
import logging
import traceback
from dataclasses import dataclass
from pathlib import Path

from database.db_methods.raw_data_db_methods import RawDataDbMethods
from entities.audit_log_manager import AuditLogManager
from entities.auditd_log import AuditLog
from utils.auditd_parser import AuditParser
from utils.datetime_utils import DatetimeUtils


@dataclass
class Analyser:
    file_path: str = '/var/log/audit/audit.log'  # todo: env var
    audit_log_manager = AuditLogManager()

    def start_analysing(self) -> None:
        logging.info(f'Starting analysis software. {self.file_path=}')
        start_time: datetime = DatetimeUtils.datetime_now()
        total_line_numbers: int = 0
        analysing: bool = True  # todo: we can check the config file and know exactly how many log files to expect
        file_index: int = 0
        try:
            while analysing:  # todo: if will be time I can do it in parallel (threads) But then need to do right writing
                file_path: str = self.file_path if file_index == 0 else (self.file_path + '.' + str(file_index))
                if Path(file_path).is_file():
                    scanned_lines: int = self._read_file(file_path)
                    logging.info(f'Scanned: {scanned_lines} lines in file index: {file_index}.\n'
                                 f'File name: {file_path}')
                    total_line_numbers += scanned_lines
                    file_index += 1
                else:
                    analysing = False
        except Exception as e:
            logging.fatal(f'Exception: {type(e)=}, {str(e)}')
            logging.fatal(traceback.format_exc())
        finally:
            logging.info(f'done. {total_line_numbers=}, total_time: {DatetimeUtils.datetime_now() - start_time}, '
                         f'routes (total files scanned): {file_index}')

    def _read_file(self, file_path: str, ) -> int:
        try:
            with open(file_path, 'r') as log_file:
                file_lines: int = 0
                for line_num, audit_log_str in enumerate(log_file):
                    # print(f'{audit_log_str}\n')
                    file_lines = line_num
                    audit_log_dict: dict = AuditParser.parse_audit_to_dict(audit_log_str)
                    audit_log: AuditLog = AuditLog.from_dict(audit_log_dict)
                    self.audit_log_manager.add_audit_log_to_dict(audit_log)

                    if line_num % 1000 == 0:
                        print(f'{line_num=}')
                        self.audit_log_manager.add_logs_from_dict_to_db_in_bulk()
        except Exception as e:
            logging.error(f'Exception during reading: {type(e)=}, {str(e)}. Continue to next log...')
        finally:
            return file_lines + 1
