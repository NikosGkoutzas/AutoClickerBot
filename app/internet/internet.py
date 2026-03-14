from .internet_interface import InternetInterface
from ..email.send_email_interface import SendEmailInterface
from ..files.read_files_interface import ReadFilesInterface
from ..files.write_files_interface import WriteFilesInterface
from datetime import datetime
import socket
import inject


class Internet(InternetInterface):
    @inject.autoparams()
    def __init__(self,
                 send_email_interface: SendEmailInterface,
                 read_files_interface: ReadFilesInterface,
                 write_files_interface: WriteFilesInterface):

        self.send_email = send_email_interface
        self.read_files = read_files_interface
        self.write_files = write_files_interface

    def check_for_internet_connection(self) -> bool:
        '''
        Checks internet connectivity by attempting socket connections to known DNS servers.
        If connectivity is restored after an outage, a notification email is sent.
        If all checks fail, internet error counters and timestamps are updated.

        :Parameters: None
        :Returns: bool
        '''
        servers = [("1.1.1.1", 53), ("8.8.8.8", 53)]

        for server in servers:
            try:
                socket.create_connection(server, timeout=2)
                occured = self.read_files.read_last_internet_error_time()

                if (occured):
                    restored = str(datetime.now().replace(
                        microsecond=0).strftime('%H:%M:%S'))
                    self.write_files.write_last_internet_error_time('')
                    self.send_email.send_email_no_internet_connection(occured.strftime('%H:%M:%S'),
                                                                      restored)
                return True

            except Exception as e:
                print(
                    f'An error occured while checking internet connection status: {str(e)}')
                continue

        self.write_files.write_total_errors()
        self.write_files.write_internet_errors()
        internet_error_date = self.read_files.read_last_internet_error_time()

        if (not internet_error_date):
            self.write_files.write_last_internet_error_time(
                str(datetime.now().replace(microsecond=0).strftime('%H:%M:%S')))
        return False
