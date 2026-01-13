from .internet_interface import InternetInterface
from ..email.send_email_interface import SendEmailInterface
from ..files.read_files_interface import ReadFilesInterface
from ..files.write_files_interface import WriteFilesInterface
from datetime import datetime
import socket , inject


class Internet(InternetInterface):
    @inject.autoparams()
    def __init__(self , send_email_interface: SendEmailInterface , read_files_interface: ReadFilesInterface , write_files_interface: WriteFilesInterface):
        self.send_email = send_email_interface
        self.read_files = read_files_interface
        self.write_files = write_files_interface
        
        
    def check_for_internet_connection(self) -> bool:
        servers = [("1.1.1.1", 53) , ("8.8.8.8", 53)]

        for server in servers:
            try:
                socket.create_connection(server, timeout=2)
                occured = self.read_files.read_error_datetime()

                if(occured):
                    restored = str(datetime.now().replace(microsecond=0).strftime('%b %d, %Y - %H:%M:%S'))
                    self.write_files.write_internet_error_date('') # clear
                    self.send_email.send_email_no_internet_connection(occured.strftime('%b %d, %Y - %H:%M:%S') , restored)
                print('YES')
                return True
            
            except Exception as e:
                print(f'An error occured while checking internet connection status: {str(e)}')
                continue
        
        self.write_files.write_total_errors()
        internet_error_date = self.read_files.read_error_datetime()
        if(not internet_error_date):
            self.write_files.write_internet_error_date(str(datetime.now().replace(microsecond=0).strftime('%b %d, %Y - %H:%M:%S')))
        print('NO')
        return False
