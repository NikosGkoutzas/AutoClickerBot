from .write_files_interface import WriteFilesInterface
from .read_files_interface import ReadFilesInterface
from .filenames import *
from datetime import datetime
import inject



class WriteFiles(WriteFilesInterface):
    @inject.autoparams()
    def __init__(self , read_files_interface: ReadFilesInterface):
        self.read_files = read_files_interface


    def compute_delay_between_updates(self) -> None:
        try:
            total_required_updates = int(os.getenv('total_required_updates'))
            current_time = datetime.now().replace(microsecond=0)
            end_time_from_file = str(self.read_files.read_end_time())
            end_time_hour = int(end_time_from_file.split(':')[0])
            end_time_minute = int(end_time_from_file.split(':')[1])
            end_time = datetime.now().replace(hour=end_time_hour , minute=end_time_minute , second=0 , microsecond=0)

            minutes_difference = end_time - current_time
            return round((minutes_difference.total_seconds() / 60) / total_required_updates , 1)          

        except Exception as e:
            raise ValueError(f'An error occured computing delay between updates: {str(e)}')
        



    def general_write_int(self , filename: str , number: int) -> None:
        try:
            with open(filename , 'w') as f:
                f.write(str(number + 1))

        except FileNotFoundError:
            raise ValueError(f'File \'{filename}\' not found.')
        
        except ValueError:
            raise ValueError(f'File \'{filename}\' does not contain a valid integer.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')
        


    def write_url_current_pos(self) -> None:
        current_pos = self.read_files.read_url_current_pos()
        total_number_of_urls = self.read_files.read_number_of_urls()

        try:
            with open(url_current_pos_filename , 'w') as f:
                if(current_pos < total_number_of_urls):
                    f.write(str(current_pos + 1))
                else:
                    f.write(str(1))

        except FileNotFoundError:
            raise ValueError(f'File \'{url_current_pos_filename}\' not found.')
        
        except ValueError:
            raise ValueError(f'File \'{url_current_pos_filename}\' does not contain a valid integer.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')
        

    def write_app_version(self , semantic_versioning: str) -> None:
        '''
        PATCH: bug fix (0.0.1 -> 0.0.2)
        MINOR: add features (0.0.1 -> 0.1.0) ~> eliminate patch
        MAJOR: change function_name, arguments(add,remove), remove features (1.4.7 → 2.0.0) ~> eliminate patch & minor
        '''
        version = self.read_files.read_app_version()
        
        try:
            with open(app_version_filename , 'w') as f:
                patch = int(version.split('.')[2])
                minor = int(version.split('.')[1])
                major = int(version.split('.')[0])
                
                if(semantic_versioning not in ['patch' , 'minor' , 'major']):
                    raise ValueError('Semantic versioning must be \'patch\', \'minor\' or \'major\' in function \'write_app_version\'.')                
                
                if(semantic_versioning == 'major'):
                    minor = 0
                    patch = 0
                    major += 1
                elif(semantic_versioning == 'minor'):
                    patch = 0
                    minor += 1
                else:
                    patch += 1
                
                new_version = str(major) + '.' + str(minor) + '.' + str(patch)
                f.write(new_version)
                
        except FileNotFoundError:
            raise ValueError(f'File \'{url_current_pos_filename}\' not found.')
        
        except ValueError:
            raise ValueError(f'File \'{url_current_pos_filename}\' does not contain a valid string.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')
        
        

    def write_delay_per_update(self , delay: float) -> None:
        try:
            with open(delay_per_update_filename , 'w') as f:
                #delay = 5 if delay < 5 else delay # min delay is 5 minutes
                f.write(str(delay))

        except FileNotFoundError:
            raise ValueError(f'File \'{delay_per_update_filename}\' not found.')
        
        except ValueError:
            raise ValueError(f'File \'{delay_per_update_filename}\' does not contain a valid integer.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')


    def write_total_updates(self) -> None:
        number = self.read_files.read_total_updates()
        self.general_write_int(total_updates_filename , number)


    def write_total_errors(self) -> None:
        number = self.read_files.read_total_errors()
        self.general_write_int(total_errors_filename , number)


    def write_number_of_removed_machines(self) -> None:
        number = self.read_files.read_number_of_removed_machines()
        self.general_write_int(number_of_removed_machines_filename , number)


    def write_number_of_inserted_machines(self) -> None:
        number = self.read_files.read_number_of_inserted_machines()
        self.general_write_int(number_of_inserted_machines_filename , number)


    def write_update_number_of_machine(self , line: int) -> None:
        with open(updates_per_machine_filename , 'r') as f1 , open(urls_filename , 'r') as f2:
            lines = f1.readlines()
            url_lines = f2.readlines()
        
        if(len(lines) != len(url_lines)):
            raise ValueError(f'Number of lines in \'{updates_per_machine_filename}\' and \'{urls_filename}\' does not match.')
        
        if(line < 1 or line > len(lines)):
            raise ValueError(f'Invalid position selected from file \'{updates_per_machine_filename}\'.')
        
        current_update_number_of_machine = int(lines[line - 1])
        new_line = '\n' if(line < len(lines)) else ''
        lines[line - 1] = str(current_update_number_of_machine + 1) + new_line

        with open(updates_per_machine_filename , 'w') as f:
            f.writelines(lines)



    def write_number_of_github_updates(self) -> None:
        number = self.read_files.read_number_of_github_updates()
        self.general_write_int(number_of_github_updates_filename , number)
    
    
    def write_time_general(self , filename: str , dt: str) -> None:
        try:
            with open(filename , 'w') as f:
                f.write(dt)

        except FileNotFoundError:
            raise ValueError(f'File \'{filename}\' not found.')
        
        except ValueError:
            raise ValueError(f'File \'{filename}\' does not contain a valid time value.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')


    def write_internet_error_date(self , dt: str) -> None:
        self.write_time_general(internet_error_datetime_filename , dt)


    def write_progress_number(self) -> None:
        number = self.read_files.read_progress_number()
        self.general_write_int(progress_number_filename , number)


    def add_machine(self , url_link: str) -> None:
        # add url link to the bottom of 'urls.txt' file
        # add a new line with '0' updates to the bottom of 'updates_per_machine' file
        try:                
            is_empty_f1  = False
            is_empty_f2 = False
            
            with open(urls_filename , 'r') as f1 , open(updates_per_machine_filename , 'r') as f2:
                if(f1.read(1) == ''):
                    is_empty_f1 = True
                
                if(f2.read(1) == ''):
                    is_empty_f2 = True
                    
            with open(urls_filename , 'a') as f1 , open(updates_per_machine_filename , 'a') as f2:
                f1.write('\n' + url_link if not is_empty_f1 else url_link)
                f2.write('\n' + str(0) if not is_empty_f2 else str(0))
                

        except FileNotFoundError:
            raise ValueError(f'File \'{urls_filename}\' or \'{updates_per_machine_filename} not found.')
        
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')


    def remove_machine(self , url_link: str) -> None:
        try:
            with open(urls_filename , 'r') as f1 , open(updates_per_machine_filename , 'r') as f2:
                f1_lines = f1.read().splitlines()
                f2_lines = f2.read().splitlines()
                
                if(url_link in f1_lines):
                    line_of_url_link = f1_lines.index(url_link)
                    f1_lines.pop(line_of_url_link)
                    f2_lines.pop(line_of_url_link)
                else:
                    print(f'File \'{urls_filename}\' does not contain \'{url_link}\' url link.')
            
            with open(urls_filename , 'w') as f1 , open(updates_per_machine_filename , 'w') as f2:
                f1.write('\n'.join(f1_lines))
                f2.write('\n'.join(f2_lines))

        except FileNotFoundError:
            raise ValueError(f'File \'{urls_filename}\' or \'{updates_per_machine_filename} not found.')
       
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')
        
        
        
    def write_email_dates(self , dt: str) -> None:
        try:
            is_empty = False
            
            with open(read_email_dates_filename , 'r') as f:
                if(f.read(1) == ''):
                    is_empty = True
                    
            with open(read_email_dates_filename , 'a') as f:
                f.write('\n' + dt if not is_empty else dt)
                
        except FileNotFoundError:
            raise ValueError(f'File \'{read_email_dates_filename}\' not found.')
        
        except ValueError:
            raise ValueError(f'File \'{read_email_dates_filename}\' does not contain a valid time value.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')
        
    
    
    
    def write_number_in_file(self , filename , number) -> None:
        try:
            with open(filename , 'w') as f:
                f.write(str(number))
                
        except FileNotFoundError:
            raise ValueError(f'File \'{filename}\' not found.')
        
        except ValueError:
            raise ValueError(f'File \'{filename}\' does not contain a valid integer.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')
        
        
        
        
    def write_app_started(self) -> None:
        self.write_number_in_file(app_started_filename , 1)
        
        app_ended_number = self.read_files.read_app_ended()
        if(app_ended_number != 0):
            self.write_number_in_file(app_ended_filename , 0)
        
        
        
        
    def write_app_ended(self) -> None:
        number = self.read_files.read_app_ended()
        self.general_write_int(app_ended_filename , number)
        
        app_started_number = self.read_files.read_app_started()
        if(app_started_number != 0):
            self.write_number_in_file(app_started_filename , 0)
        
    
        
        
    def write_number_of_captcha_challenge(self) -> None:
        number = self.read_files.read_number_of_captcha_challenges()
        self.general_write_int(number_of_captcha_challenges_filename , number)
        
        
        
    def write_check_email_every_20_minutes(self , time_: str) -> None:
        self.write_time_general(check_email_every_20_minutes_filename , time_)
        
        
    
    def reset_all_updates_per_machine(self) -> None:
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
        
        
        
    def reset_all_files(self) -> None:
        try:
            self.write_number_in_file(progress_number_filename , 0)
            self.write_number_in_file(internet_error_datetime_filename , '')
            self.write_number_in_file(number_of_captcha_challenges_filename , 0)
            self.write_number_in_file(number_of_github_updates_filename , 0)
            self.write_number_in_file(number_of_inserted_machines_filename , 0)
            self.write_number_in_file(number_of_removed_machines_filename , 0)
            self.write_number_in_file(total_errors_filename , 0)
            self.write_number_in_file(total_updates_filename , 0)
            self.write_number_in_file(url_current_pos_filename , 1)
            self.write_number_in_file(daily_report_sent_filename , 1)
            self.write_check_email_every_20_minutes('06:30:00')
            self.reset_all_updates_per_machine()
            
        except Exception as e:
            print(f'An error occured while trying to reset some files: {str(e)}')
            self.write_files.write_total_errors()
        
        
    
    
    def update_credentials_from_env(self , new_username: str | None , new_password: str | None) -> None:
        try:
            with open(env_filename , 'r') as f:
                lines = f.readlines()
                
            with open(env_filename , 'w') as f:
                for i in range(len(lines)): # first 2 lines are the credentials
                    if(i == 0 and 'site_username' in lines[i]):
                        if(new_username is not None):
                            lines[i] = f"site_username='{new_username}'\n"
                            
                    elif(i == 1 and 'site_password' in lines[i]):
                        if(new_password is not None):
                            lines[i] = f"site_password='{new_password}'\n"
                    
                f.writelines(lines)
                    
                
        except FileNotFoundError:
            raise ValueError(f'File \'{env_filename}\' not found.')
        
        except ValueError:
            raise ValueError(f'File \'{env_filename}\' does not contain valid strings.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')
        
        
        
        
        
    def write_daily_report_sent(self) -> None:
        self.write_number_in_file(daily_report_sent_filename , 1)