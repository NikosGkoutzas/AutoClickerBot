from .reset_files_interface import ResetFilesInterface
from .write_files_interface import WriteFilesInterface
from .filenames import *
import inject


class ResetFiles(ResetFilesInterface):
    @inject.autoparams()
    def __init__(self , write_files_interface: WriteFilesInterface):
        self.write_files = write_files_interface
        
        
    def reset_all_files(self):
        try:
            self.write_files.write_number_in_file(progress_number_filename , 0)
            self.write_files.write_number_in_file(internet_error_datetime_filename , '')
            self.write_files.write_number_in_file(number_of_captcha_challenges_filename , 0)
            self.write_files.write_number_in_file(number_of_github_updates_filename , 0)
            self.write_files.write_number_in_file(number_of_inserted_machines_filename , 0)
            self.write_files.write_number_in_file(number_of_removed_machines_filename , 0)
            self.write_files.write_number_in_file(total_errors_filename , 0)
            self.write_files.write_number_in_file(total_updates_filename , 0)
            self.write_files.write_number_in_file(url_current_pos_filename , 1)
            self.write_files.write_number_in_file(daily_report_sent_filename , 1)
            self.write_files.write_check_email_every_20_minutes('06:30:00')
            self.write_files.write_number_in_file(app_started_filename , 0)
            self.write_files.write_number_in_file(app_ended_filename , 0)
            self.write_files.write_number_in_file(delay_per_update_filename , 5)
            self.write_files.reset_all_updates_per_machine()
            
        except Exception as e:
            print(f'An error occured while trying to reset all files: {str(e)}')
            self.write_files.write_total_errors()