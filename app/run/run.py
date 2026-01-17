from .run_interface import RunInterface
from ..calculations.calculations_interface import CalculationInterface
from ..internet.internet_interface import InternetInterface
from ..action.action_interface import ActionInterface
from ..files.read_files_interface import ReadFilesInterface
from ..files.write_files_interface import WriteFilesInterface
from ..files.reset_files_interface import ResetFilesInterface
from ..email.send_email_interface import SendEmailInterface
from ..driver.driver_interface import DriverInterface
from ..email.read_email_interface import ReadEmailInterface
from ..browser_launcher.chrome_boot_interface import ChromeBootInterface
import inject , time


class Run(RunInterface):
    @inject.autoparams()
    def __init__(self ,
                 calculations_interface: CalculationInterface ,
                 internet_interface: InternetInterface ,
                 action_interface: ActionInterface ,
                 read_files_interface: ReadFilesInterface ,
                 write_files_interface: WriteFilesInterface ,
                 send_email_interface: SendEmailInterface ,
                 driver_interface: DriverInterface ,
                 read_email_interface: ReadEmailInterface ,
                 reset_files_interface: ResetFilesInterface ,
                 chrome_boot_interface: ChromeBootInterface
                 ):
        
        self.calculation = calculations_interface
        self.internet = internet_interface
        self.action = action_interface
        self.read_files = read_files_interface
        self.write_files = write_files_interface
        self.send_email = send_email_interface
        self.driver = driver_interface
        self.read_email = read_email_interface
        self.reset_files = reset_files_interface
        self.chrome_boot = chrome_boot_interface
        
        
        
    def run(self):
        self.action.check_for_latest_version()
        self.reset_files.reset_all_files()
        self.chrome_boot.boot()
        self.driver.start_driver()
        self.driver.open_url('https://www.car.gr/login/')
        #wait_for_captcha = 60 # sec.
        #print(f'Wait {wait_for_captcha} seconds to allow captcha detection...')
        #time.sleep(wait_for_captcha)
        print('Launch.')
        self.driver.accept_cookies()
        self.action.check_login()
        
        while(True):
            if(not self.calculation.app_in_time()):
                if(self.read_files.read_app_ended() == 0):
                    self.write_files.write_app_ended()
                    if(self.internet.check_for_internet_connection()):
                        self.send_email.send_email_daily_report()
                        self.write_files.write_daily_report_sent()
                        self.calculation.sleep_till_next_day()
                    
            
            else:
                #if(self.calculation.check_emails()):
                self.read_email.fetch_last_emails()
                    
                if(not self.calculation.updates_completed()):
                    if(self.internet.check_for_internet_connection()):
                        if(self.read_files.read_daily_report_sent() == 0):
                            self.send_email.send_email_daily_report()
                            self.write_files.write_daily_report_sent()
                            
                        if(self.read_files.read_app_started() == 0):
                            self.write_files.reset_all_files() # reset all files here, because if daily report is going to be sent
                                                               # but internet connection has a problem and a few minutes later
                                                               # restored, all data will be reset and we will gonna send these data
                                                               # which are the wrong today's data. Also, if daily report was not sent,
                                                               # this is going to be sent the next day, before 'launch' email and then
                                                               # all data will be reset.
                            self.send_email.send_email_launch()
                            self.write_files.write_app_started()
                            
                        self.action.update_machine_procedure()
                        delay = self.calculation.delay_between_updates()
                        self.write_files.write_delay_per_update(delay)
                        time.sleep(delay)
                        
                    else:
                        time.sleep(5)
                        
                else:
                    self.calculation.updates_completed_earlier_wait()