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
        '''
        Executes the machine update process using the URL from the current
        position that is stored in a file. If the update is successful,
        updates the current position and total number of the updates.
        '''
        
        current_url = self.read_files.read_url_from_current_pos()
        updated = self.driver.update_machine(current_url)

        if(updated):
            current_pos = self.read_files.read_url_current_pos()
            self.write_files.write_update_number_of_machine(current_pos)
            self.write_files.write_total_updates()
            
        self.write_files.write_url_current_pos()
        
        
        
    
    
    
    def check_login(self) -> None:
        '''
        On system startup, checks whether a captcha is present.
        If detected, the system attempts to solve it and upon success,
        enters the user credentials.

        The captcha challenge appears again, the system is trying to
        solve it and a status code is returned.
        Finallym an appropriate email notification is sent.

        Returned values from login function:
        2: Failed to solve captcha
        3: Invalid login credentials after three attempts (email sent)
        '''
        
        flag = self.driver.login()
            
        if(flag == 2):
            self.send_email.send_email_captcha_failed_to_solve()
            
        elif(flag == 3):
            self.send_email.send_email_unable_to_login()
            

    
    def latest_version_available(self) -> bool:
        '''
        Read the 'new_version_update_flag' filename and if it contains '1', it
        means a new version has already been installed (many files have been replaced)
        and send an email to inform the new installation of the new app's version.
        Finally, reset the flag from the file. 
        '''
        
        if(self.read_files.read_new_version_update_flag()):
            self.write_files.write_new_version_update_flag(0)
            self.send_email.send_email_new_version_updated()
            return True
        
        return False