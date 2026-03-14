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
import inject
import time


class Run(RunInterface):
    @inject.autoparams()
    def __init__(self,
                 calculations_interface: CalculationInterface,
                 internet_interface: InternetInterface,
                 action_interface: ActionInterface,
                 read_files_interface: ReadFilesInterface,
                 write_files_interface: WriteFilesInterface,
                 send_email_interface: SendEmailInterface,
                 driver_interface: DriverInterface,
                 read_email_interface: ReadEmailInterface,
                 reset_files_interface: ResetFilesInterface,
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

    def run(self) -> None:
        '''
        Runs the main application loop.
        Handles application startup, login, scheduled updates,
        email notifications, internet checks, and daily workflow
        until the process completes or waits for the next cycle.

        :Parameters: None
        :Returns: None
        '''

        self.chrome_boot.boot()
        self.driver.start_driver()
        print('System launched!')
        self.action.check_login()

        while (True):
            if (not self.calculation.app_in_time()):
                if (self.read_files.read_app_ended() == 0):
                    self.write_files.write_app_ended()
                    self.reset_files.reset_app_started()

                    if (self.internet.check_for_internet_connection()):
                        self.send_email.send_email_daily_report()
                        self.reset_files.reset_all_files()

                    else:
                        self.write_files.write_daily_report_sent(0)
                        self.reset_files.reset_total_updates()

                    self.calculation.sleep_till_next_day()

            else:
                if (self.calculation.check_emails()):
                    self.read_email.fetch_last_emails()

                if (not self.calculation.updates_completed()):
                    if (self.internet.check_for_internet_connection()):
                        if (self.read_files.read_daily_report_sent() == 0):
                            self.send_email.send_email_daily_report()
                            self.write_files.write_daily_report_sent(1)

                        if (self.read_files.read_app_started() == 0):
                            '''
                            Reset all files here to avoid sending incorrect daily data.
                            If the daily report is scheduled to be sent but the internet
                            connection fails and is restored a few minutes later partial
                            data may be sent.
                            Additionally, if the daily report is not sent on the intended day,
                            it will be sent the next day before the 'launch' email.
                            After the report is sent, all data will be reset.
                            '''
                            self.reset_files.reset_all_files()
                            self.send_email.send_email_launch()
                            self.write_files.write_app_started()
                            self.reset_files.reset_app_ended()

                        self.action.update_machine_procedure()
                        delay = self.calculation.delay_between_updates()
                        self.write_files.write_delay_per_update(delay)

                        if (self.read_files.check_errors_occurred_10()):
                            self.send_email.send_email_every_10_errors_occured(
                                self.read_files.read_total_errors())

                        time.sleep(delay)

                    else:
                        time.sleep(5)

                else:
                    self.calculation.updates_completed_earlier_wait()
