from .action_interface import ActionInterface
from ..driver.driver_interface import DriverInterface
from ..files.read_files_interface import ReadFilesInterface
from ..files.write_files_interface import WriteFilesInterface
from ..email.send_email_interface import SendEmailInterface
from dotenv import load_dotenv
import inject , os , subprocess , time



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
        Executes the update procedure for the current machine.
        Reads the current machine URL, performs the update operation, and if the
        update is successful, updates the current position of url and the number of
        total updates.
        Environment variables are reloaded to ensure that the updated configuration
        values are used. Finally, the current URL position is being increased in order
        to update the next URL.

        :Parameters: None
        :Returns: None
        '''
        
        current_url = self.read_files.read_url_from_current_pos()
        updated = self.driver.update_machine(current_url)

        if(updated == 1):
            current_pos = self.read_files.read_url_current_pos()
            self.write_files.write_update_number_of_machine(current_pos)
            self.write_files.write_total_updates()
            load_dotenv(override=True)
            print(f'{self.read_files.read_total_updates()}/{os.getenv('total_required_updates')} machines updated.')
        
        elif(updated == -1):
            self.send_email.send_email_captcha_failed_to_solve()
            self.open_teamviewer()
            
        self.write_files.write_url_current_pos()
        
        
        
    
    
    
    def check_login(self) -> None:
        '''
        Checks the login status and handles login failure scenarios.
        Executes the login process and evaluates the returned status flag.
        If a CAPTCHA challenge cannot be solved or the login attempt fails,
        a notification email is sent and TeamViewer is opened for remote access.

        :Parameters: None
        :Returns: None
        '''
        
        flag = self.driver.login()
            
        if(flag == 2):
            self.send_email.send_email_captcha_failed_to_solve_in_login()
            self.open_teamviewer()
            
        elif(flag == 3):
            self.send_email.send_email_unable_to_login()
            self.open_teamviewer()
            

    
    def latest_version_available(self) -> bool:
        '''
        Read the 'new_version_update_flag' filename and if it contains '1', it
        means a new version has already been installed (many files have been replaced)
        and send an email to inform the new installation of the new app's version.
        Finally, reset the flag from the file.
        
        :Parameters: None
        :Returns: bool: True if the file 'new_version_update_flag.txt' contains the value
                        '1' (that means a new version is ready to be updated), otherwise 
                        False if the text file contains the value '0'. 
        '''
        
        if(self.read_files.read_new_version_update_flag()):
            self.write_files.write_new_version_update_flag(0)
            self.send_email.send_email_new_version_updated()
            return True
        
        return False
    
    
    

    def is_teamviewer_gui_enable(self) -> bool:
        '''
        Check if GUI of TeamViewer in the system is enabled.
        
        :Parameters: None
        :Returns: bool: True if the TeamViewer GUI is enabled, otherwise False.
        '''
        result = subprocess.run(['pgrep' , '-af' , 'teamviewer'] , stdout=subprocess.PIPE , stderr=subprocess.DEVNULL , text=True)

        if result.returncode != 0:
            return False

        for line in result.stdout.splitlines():
            if('teamviewerd' not in line):
                return True

        return False




    def is_teamviewer_daemon_active(self) -> bool:
        '''
        Check if DAEMON of TeamViewer in the system is enabled.
        
        :Parameters: None
        :Returns: bool: True if the TeamViewer DAEMON is enabled, otherwise False.
        '''
        return subprocess.run(['systemctl' , 'is-active' , '--quiet' , 'teamviewerd']).returncode == 0



    
    def open_teamviewer(self) -> None:
        '''
        Starts the TeamViewer service and application if not already running.
        If a TeamViewer connection is already active, an informational email is sent
        and no further action is taken. Otherwise, the TeamViewer service is started,
        the TeamViewer application is launched and a notification email is sent.
        In case of failure, an error is logged and a failure notification email is sent.

        :Parameters: None
        :Returns: None
        '''
        
        try:
            if(self.is_teamviewer_daemon_active() and self.is_teamviewer_gui_enable()):
                print('TeamViewer remote access is already enabled.')
                self.send_email.send_email_teamviewer_connection_already_opened()
                return
            
            print('Launching TeamViewer...')
            subprocess.run(['sudo' , 'systemctl' , 'start' , 'teamviewerd'] , check=False)
            subprocess.Popen(['teamviewer'] , stdout=subprocess.DEVNULL , stderr=subprocess.DEVNULL)
            print('TeamViewer launched.')
            self.send_email.send_email_teamviewer_connected()
            
        except Exception as e:
            print(f'An error occured while trying to open teamviewer: {str(e)}')
            self.write_files.write_total_errors()
            self.send_email.send_email_failed_to_open_teamviewer()
            
            
            
    def close_teamviewer(self) -> None:
        '''
        Stops the TeamViewer application and service if currently running.
        If no active TeamViewer connection is detected, an informational email is sent
        and no further action is taken. Otherwise, the TeamViewer application process
        is terminated, the TeamViewer service is stopped and a notification email is sent.
        In case of failure, an error is logged and a failure notification email is sent.

        :Parameters: None
        :Returns: None
        '''
        
        try:
            if(not self.is_teamviewer_daemon_active() and not self.is_teamviewer_gui_enable()):
                print('TeamViewer remote access is already disabled.')
                self.send_email.send_email_teamviewer_connection_already_closed()
                return
            
            print('Closing TeamViewer...')
            subprocess.run(['pkill' , 'teamviewer'] , check=False , stdout=subprocess.DEVNULL , stderr=subprocess.DEVNULL)
            subprocess.run(['sudo' , 'systemctl' , 'stop' , 'teamviewerd'] , check=False)
            print('TeamViewer closed.')
            self.send_email.send_email_teamviewer_disconnected()

        except Exception as e:
            print(f'An error occured while trying to close teamviewer: {str(e)}')
            self.write_files.write_total_errors()
            self.send_email.send_email_failed_to_close_teamviewer()