from .reset_files_interface import ResetFilesInterface
from .write_files_interface import WriteFilesInterface
from .read_files_interface import ReadFilesInterface
from .filenames import *
import inject


class ResetFiles(ResetFilesInterface):
    @inject.autoparams()
    def __init__(self ,
                 write_files_interface: WriteFilesInterface ,
                 read_files_interface: ReadFilesInterface):
        
        self.read_files = read_files_interface
        self.write_files = write_files_interface
        
        
    def reset_all_files(self) -> None:
        '''
        Resets all files.
        
        :Parameters: None
        :Returns: None
        '''
        try:
            self.write_files.write_number_in_file(number_of_captcha_challenges_filename , 0)
            self.write_files.write_number_in_file(number_of_github_updates_filename , 0)
            self.write_files.write_number_in_file(number_of_inserted_machines_filename , 0)
            self.write_files.write_number_in_file(number_of_removed_machines_filename , 0)
            self.write_files.write_number_in_file(total_errors_filename , 0)
            self.write_files.write_number_in_file(total_updates_filename , 0)
            self.write_files.write_number_in_file(url_current_pos_filename , 1)
            self.write_files.write_number_in_file(daily_report_sent_filename , 1)
            self.write_files.write_number_in_file(internet_errors_filename , 0)
            self.write_files.write_number_in_file(last_internet_error_time_filename , '')
            self.write_files.write_number_in_file(last_error_time_filename , '')
            self.write_files.write_check_email_every_20_minutes(self._reset_check_email_every_20_minutes_filename())
            self.write_files.write_number_in_file(app_started_filename , 0)
            self.write_files.write_number_in_file(app_ended_filename , 0)
            self.write_files.write_number_in_file(delay_per_update_filename , 5)
            self.write_files.write_number_in_file(new_version_update_flag_filename , 0)
            self.reset_all_updates_per_machine()
            
        except Exception as e:
            print(f'An error occured while trying to reset all files: {str(e)}')
            self.write_files.write_total_errors()
            
            
            
            
            

    def reset_all_updates_per_machine(self) -> None:
        '''
        Resets all machine numbers of updates.
        
        :Parameters: None
        :Returns: None
        '''
        try:
            with open(updates_per_machine_filename , 'r') as f:
                lines = f.readlines()
                
            with open(updates_per_machine_filename , 'w') as f:
                for i in range(len(lines)):
                    if(i != len(lines) - 1):
                        f.write('0\n')
                    else:
                        f.write('0')
                
        except FileNotFoundError:
            raise ValueError(f'File \'{updates_per_machine_filename}\' not found.')
        
        except ValueError:
            raise ValueError(f'File \'{updates_per_machine_filename}\' does not contain valid integers.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')
        
        
        
    
    def reset_total_updates(self) -> None:
        '''
        Resets total updates number.
        
        :Parameters: None
        :Returns: None
        '''
        self.write_files.write_number_in_file(total_updates_filename , 0)




    def reset_app_started(self) -> None:
        '''
        Resets app_started file.
        
        :Parameters: None
        :Returns: None
        '''
        self.write_files.write_number_in_file(app_started_filename , 0)
        
        
    
    def reset_app_ended(self) -> None:
        '''
        Resets ended_started file.
        
        :Parameters: None
        :Returns: None
        '''
        self.write_files.write_number_in_file(app_ended_filename , 0)
        
        
        
    def _reset_check_email_every_20_minutes_filename(self) -> str:
        start_time = str(self.read_files.read_start_time())
        start_time_split = start_time.split(':')
        start_time_hour = str(int(start_time_split[0]) - 1)
        start_time_hour = '0' + start_time_hour if(len(str(int(start_time_split[0]) - 1)) == 1) else start_time_hour
        start_time_min = '30'
        start_time_sec = start_time_split[2]
        return start_time_hour + ':' + start_time_min + ':' + start_time_sec