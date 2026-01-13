from .read_files_interface import ReadFilesInterface
from .filenames import *
import datetime



class ReadFiles(ReadFilesInterface):
    def can_app_run_at_current_time(self) -> bool:
        start_time = self.read_start_time()
        end_time = self.read_end_time()
        now = datetime.datetime.now().time()

        return now >= start_time and now < end_time



    def general_read_int(self , filename: str) -> int:
        try:
            with open(filename , 'r') as f:
                return int(f.read().strip())

        except FileNotFoundError:
            raise ValueError(f'File {filename} not found.')
        
        except ValueError:
            raise ValueError(f'File {filename} does not contain a valid integer.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')
        


    def read_number_of_urls(self) -> int:
        try:
            with open(urls_filename , 'r') as f:
                return len(f.readlines())

        except FileNotFoundError:
            raise ValueError(f'File {urls_filename} not found.')
        
        except ValueError:
            raise ValueError(f'File {urls_filename} does not contain a valid integer.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')
    


    def read_app_version(self) -> str:
        try:
            with open(app_version_filename , 'r') as f:
                return f.read().strip()

        except FileNotFoundError:
            raise ValueError(f'File {urls_filename} not found.')
        
        except ValueError:
            raise ValueError(f'File {urls_filename} does not contain a valid string.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')



    def read_url_current_pos(self) -> int:
        return self.general_read_int(url_current_pos_filename)
    

    def read_url_from_current_pos(self) -> str:
        try:
            with open(url_current_pos_filename , 'r') as f:
                current_pos = int(f.read())

            with open(urls_filename , 'r') as f:
                lines = f.readlines()
                if(current_pos > len(lines) or current_pos < 1):
                    raise ValueError('An error occured in function \'read_url_from_current_pos\'. Current position of element and number of url links does not match.')
                
                return lines[current_pos - 1]
        
        except FileNotFoundError:
            raise ValueError(f'File {url_current_pos_filename} not found.')
        
        except ValueError:
            raise ValueError(f'File {url_current_pos_filename} does not contain a valid integer.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')



    def read_delay_per_update(self) -> float:
        return self.general_read_int(delay_per_update_filename)
    

    def read_total_updates(self) -> int:
        return self.general_read_int(total_updates_filename)
    

    def read_total_errors(self) -> int:
        return self.general_read_int(total_errors_filename)
    

    def read_number_of_removed_machines(self) -> int:
        return self.general_read_int(number_of_removed_machines_filename)
    

    def read_number_of_inserted_machines(self) -> int:
        return self.general_read_int(number_of_inserted_machines_filename)
    

    def read_every_url(self) -> list[str]:
        try:
            with open(urls_filename , 'r') as f:
                return list(line.strip('\n') for line in f.readlines())

        except FileNotFoundError:
            raise ValueError(f'File {urls_filename} not found.')
        
        except ValueError:
            raise ValueError(f'File {urls_filename} does not contain a valid integer.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')


    def read_update_number_of_machine(self) -> list[int]:
        try:
            with open(updates_per_machine_filename , 'r') as f1 , open(urls_filename , 'r') as f2:
                lines = [line.strip('\n') for line in f1.readlines()]
                url_lines = f2.readlines()
            
            if(len(lines) != len(url_lines)):
                raise ValueError(f'Number of lines in \'{updates_per_machine_filename}\' and \'{urls_filename}\' does not match.')
    
            return lines

        except FileNotFoundError:
            raise ValueError(f'File {updates_per_machine_filename} not found.')
        
        except ValueError:
            raise ValueError(f'File {updates_per_machine_filename} does not contain valid values.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')


    
    def read_number_of_github_updates(self) -> int:
        return self.general_read_int(number_of_github_updates_filename)
    

    def read_datetime_general(self , filename: str) -> datetime.datetime | None:
        try:
            with open(filename , 'r') as f:
                value = f.read().strip()
                    
            return datetime.datetime.strptime(value , '%b %d, %Y - %H:%M:%S') if value else None

        except FileNotFoundError:
            raise ValueError(f'File {filename} not found.')
        
        except ValueError:
            raise ValueError(f'File {filename} does not contain a valid datetime value.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')


    
    def read_time_general(self , filename: str) -> datetime.time:
        try:        
            with open(filename , 'r') as f:
                return datetime.datetime.strptime(f.read().strip() , '%H:%M:%S').time()

        except FileNotFoundError:
            raise ValueError(f'File {filename} not found.')
        
        except ValueError:
            raise ValueError(f'File {filename} does not contain a valid time value.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')
        
        

    def read_error_datetime(self) -> datetime.datetime | None:
        return self.read_datetime_general(internet_error_datetime_filename)
        

    def check_errors_occurred_10(self) -> bool:
        return self.read_total_errors() != 0 and self.general_read_int(total_errors_filename) % 10 == 0
        
    
    def read_progress_number(self) -> int:
        return self.general_read_int(progress_number_filename)
    

    def read_start_time(self) -> datetime.datetime:
        return self.read_time_general(start_time_filename)
    

    def read_end_time(self) -> datetime.datetime:
        return self.read_time_general(end_time_filename)
    
    
    def read_email_dates(self) -> list[str]:
        try:
            with open(read_email_dates_filename , 'r') as f:
                lines = [line.strip('\n') for line in f.readlines()]
                
            return lines
        
        except FileNotFoundError:
            raise ValueError(f'File {url_current_pos_filename} not found.')
        
        except ValueError:
            raise ValueError(f'File {url_current_pos_filename} does not contain a valid integer.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')
        
        
        
    def read_app_started(self) -> bool:
        return self.general_read_int(app_started_filename)
    
    
    
    def read_app_ended(self) -> bool:
        return self.general_read_int(app_ended_filename)
        
        
    
    def read_number_of_captcha_challenges(self) -> int:
        return self.general_read_int(number_of_captcha_challenges_filename)
    
    
    
    def read_check_email_every_20_minutes(self) -> datetime.time:
        return self.read_time_general(check_email_every_20_minutes_filename)
    
    
    
    def read_daily_report_sent(self) -> int:
        return self.general_read_int(daily_report_sent_filename)