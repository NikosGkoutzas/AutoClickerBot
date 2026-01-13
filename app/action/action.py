from .action_interface import ActionInterface
from ..driver.driver_interface import DriverInterface
from ..files.read_files_interface import ReadFilesInterface
from ..files.write_files_interface import WriteFilesInterface
from ..email.send_email_interface import SendEmailInterface
import inject



class Action(ActionInterface):
    @inject.autoparams()
    def __init__(self ,
                 driver_interface: DriverInterface ,
                 read_files_interface: ReadFilesInterface ,
                 write_files_interface: WriteFilesInterface ,
                 send_email_interface: SendEmailInterface
                ):        
        
        self.driver = driver_interface
        self.read_files = read_files_interface
        self.write_files = write_files_interface
        self.send_email = send_email_interface
        
        

    def update_machine_procedure(self) -> None:
        current_url = self.read_files.read_url_from_current_pos()
        updated = self.driver.update_machine(current_url)

        if(updated):
            current_pos = self.read_files.read_url_current_pos()
            self.write_files.write_update_number_of_machine(current_pos)
            self.write_files.write_total_updates()
            
        self.write_files.write_url_current_pos()
        
        
        
    
    
    
    '''
    0: captcha challenge solved after a few attempts
    1: captcha is inactive
    2: captcha challenge failed to solve
    3: wrong login credentials after 3 attempts. Email sent
    '''
    def check_login(self) -> None:
        flag = self.driver.login()

        if(flag == 3):
            self.send_email.send_email_unable_to_login()
            
        elif(flag == 2):
            self.send_email.send_email_captcha_failed_to_solve()