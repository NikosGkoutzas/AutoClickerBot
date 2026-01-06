from .run_interface import RunInterface
from ..calculations.calculations_interface import CalculationInterface
from ..internet.internet_interface import InternetInterface
from ..action.action_interface import ActionInterface
from ..files.read_files_interface import ReadFilesInterface
from ..files.write_files_interface import WriteFilesInterface
from ..email.send_email_interface import SendEmailInterface
from ..driver.driver_interface import DriverInterface
from ..email.read_email_interface import ReadEmailInterface
import inject , time


class Run(RunInterface):
    #@inject.autoparams()
    def __init__(self ,
                 calculations_interface: CalculationInterface ,
                 internet_interface: InternetInterface ,
                 action_interface: ActionInterface ,
                 read_files_interface: ReadFilesInterface ,
                 write_files_interface: WriteFilesInterface ,
                 send_email_interface: SendEmailInterface ,
                 driver_interface: DriverInterface ,
                 read_email_interface: ReadEmailInterface
                 ):
        
        self.calculation = calculations_interface
        self.internet = internet_interface
        self.action = action_interface
        self.read_files = read_files_interface
        self.write_files = write_files_interface
        self.send_email = send_email_interface
        self.driver = driver_interface
        self.read_email = read_email_interface
        
        
        
    def run(self):
        self.driver.open_url('https://www.car.gr/login/')
        self.driver.accept_cookies()
        time.sleep(12) # wait for the captcha to pop up
        self.action.check_login()
        
        while(True):
            if(not self.calculation.app_in_time()):
                if(self.read_files.read_app_ended() == 0):
                    
                    self.write_files.write_app_ended()
                    if(self.internet.check_and_wait_for_internet_connection()):
                        self.send_email.send_email_daily_report()
                        self.write_files.write_daily_report_sent()
                    
            
            else:
                '''result = self.driver.is_captcha_active_before_login_credentials()
                if(result == 3):
                    self.send_email.send_email_unable_to_login()
                    
                elif(result == 2):
                    self.send_email.send_email_captcha_problem()'''
                    
                #if(self.calculation.check_emails()):
                self.read_email.fetch_last_emails()
                
                if(not self.calculation.updates_completed()):
                    if(self.internet.check_and_wait_for_internet_connection()):
                        if(self.read_files.read_app_started() == 0):
                            self.write_files.reset_all_files() # reset all files here, because if daily report is going to be sent
                                                               # but internet connection has a problem and a few minutes later
                                                               # restored, all data will be reset and we will gonna send these data
                                                               # which are the wrong today's data. Also, if daily report was not sent,
                                                               # this is going to be sent the next day, before 'launch' email and then
                                                               # all data will be reset.
                            #self.send_email.send_email_launch()
                            self.write_files.write_app_started()
                            
                        self.action.update_machine_procedure()
                        delay = self.calculation.delay_between_updates()
                        self.write_files.write_delay_per_update(delay)
                        time.sleep(10)
                        
                else:
                    self.calculation.updates_completed_earlier_wait()
                                                
                        # 8a stamataei se opoiadhpote katastash einai me mia metablhth apo8hkeumenh se arxeio kai molis steilw email kai
                        # to lusw xeirokinhta, tote h metzblhth allazei kai sunexizei kapws. 8elei skepsh.