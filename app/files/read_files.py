from .read_files_interface import ReadFilesInterface
from .filenames import *
from ..messages.numbers import number
from datetime import datetime , time



class ReadFiles(ReadFilesInterface):
    def general_read_int(self , filename: str) -> int:
        '''
        Reads an integer value from the specified file.

        :Parameters: filename (str): Path to the file containing an integer value.
        :Returns: int
        '''
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
        '''
        Reads and returns the total number of stored URLs.

        :Parameters: None
        :Returns: int
        '''
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
        '''
        Reads and returns the current application version.

        :Parameters: None
        :Returns: str
        '''
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
        '''
        Reads the current URL position index.

        :Parameters: None
        :Returns: int
        '''
        return self.general_read_int(url_current_pos_filename)
    

    def read_url_from_current_pos(self) -> str:
        '''
        Reads and returns the URL corresponding to the current position index.

        :Parameters: None
        :Returns: str
        '''
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
        '''
        Reads the configured delay between updates.

        :Parameters: None
        :Returns: float
        '''
        return self.general_read_int(delay_per_update_filename)
    

    def read_total_updates(self) -> int:
        '''
        Reads the total number of successful updates.

        :Parameters: None
        :Returns: int
        '''
        return self.general_read_int(total_updates_filename)
    

    def read_total_errors(self) -> int:
        '''
        Reads the total number of recorded errors.

        :Parameters: None
        :Returns: int
        '''
        return self.general_read_int(total_errors_filename)
    

    def read_number_of_removed_machines(self) -> int:
        '''
        Reads the total number of removed machines.

        :Parameters: None
        :Returns: int
        '''
        return self.general_read_int(number_of_removed_machines_filename)
    

    def read_number_of_inserted_machines(self) -> int:
        '''
        Reads the total number of inserted machines.

        :Parameters: None
        :Returns: int
        '''
        return self.general_read_int(number_of_inserted_machines_filename)
    

    def read_every_url(self) -> list[str]:
        '''
        Reads and returns all stored machine URLs.

        :Parameters: None
        :Returns: list[str]
        '''
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
        '''
        Reads the update count per machine and validates consistency with URLs.

        :Parameters: None
        :Returns: list[int]
        '''
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
        '''
        Reads the number of GitHub update operations performed.

        :Parameters: None
        :Returns: int
        '''
        return self.general_read_int(number_of_github_updates_filename)
    

    
    def read_time_general(self , filename: str) -> time | None:
        '''
        Reads a time value from the specified file.

        :Parameters: filename (str): Path to the file containing a time value.
        :Returns: time | None
        '''
        try:        
            with open(filename , 'r') as f:
                content = f.read().strip()
                
                if(not content):
                    return None
                
                return datetime.strptime(content , '%H:%M:%S').time()

        except FileNotFoundError:
            raise ValueError(f'File {filename} not found.')
        
        except ValueError:
            raise ValueError(f'File {filename} does not contain a valid time value.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')
        
        

    def read_error_time(self) -> time | None:
        '''
        Reads the most recent application error time.

        :Parameters: None
        :Returns: time | None
        '''
        return self.read_time_general(last_error_time_filename)
        

    def read_last_internet_error_time(self) -> time | None:
        '''
        Reads the most recent internet error time.

        :Parameters: None
        :Returns: time | None
        '''
        return self.read_time_general(last_internet_error_time_filename)
    
    
    def read_internet_errors(self) -> int:
        '''
        Reads the total number of internet-related errors.

        :Parameters: None
        :Returns: int
        '''
        return self.general_read_int(internet_errors_filename)
    
    
    def check_errors_occurred_10(self) -> bool:
        '''
        Checks whether the total error count is a multiple of 10.

        :Parameters: None
        :Returns: bool
        '''
        return self.read_total_errors() != 0 and self.general_read_int(total_errors_filename) % 10 == 0
    

    def read_start_time(self) -> time | None:
        '''
        Reads the application start time.

        :Parameters: None
        :Returns: time | None
        '''
        return self.read_time_general(start_time_filename)
    

    def read_end_time(self) -> time | None:
        '''
        Reads the application end time.

        :Parameters: None
        :Returns: time | None
        '''
        return self.read_time_general(end_time_filename)
    
    
    def read_email_uids(self) -> list[bytes]:
        '''
        Reads all processed email uids.

        :Parameters: None
        :Returns: list[bytes]
        '''
        try:
            with open(read_email_uids_filename , 'rb') as f:
                lines = [line.strip(b'\n') for line in f.readlines()]
                
            return lines
        
        except FileNotFoundError:
            raise ValueError(f'File {url_current_pos_filename} not found.')
        
        except ValueError:
            raise ValueError(f'File {url_current_pos_filename} does not contain a valid byte.')
            
        except Exception as e:
            raise ValueError(f'An error occured: {str(e)}')
        
        
        
    def read_app_started(self) -> bool:
        '''
        Reads the application started flag.

        :Parameters: None
        :Returns: bool
        '''
        return self.general_read_int(app_started_filename)
    
    
    
    def read_app_ended(self) -> bool:
        '''
        Reads the application ended flag.

        :Parameters: None
        :Returns: bool
        '''
        return self.general_read_int(app_ended_filename)
        
        
    
    def read_number_of_captcha_challenges(self) -> int:
        '''
        Reads the total number of CAPTCHA challenges encountered.

        :Parameters: None
        :Returns: int
        '''
        return self.general_read_int(number_of_captcha_challenges_filename)
    
    
    
    def read_check_email_every_20_minutes(self) -> time | None:
        '''
        Reads the timestamp of the last email check interval.

        :Parameters: None
        :Returns: time | None
        '''
        return self.read_time_general(check_email_every_20_minutes_filename)
    
    
    
    def read_daily_report_sent(self) -> int:
        '''
        Reads whether the daily report has been sent.

        :Parameters: None
        :Returns: int
        '''
        return self.general_read_int(daily_report_sent_filename)
    
    
    
    def read_new_version_update_flag(self) -> bool:
        '''
        Reads the flag indicating a pending new version update.

        :Parameters: None
        :Returns: bool
        '''
        return self.general_read_int(new_version_update_flag_filename)
    
    
    
    def retrieve_all_machines(self) -> str:
        '''
        Builds a HTML list containing all machine URLs.

        :Parameters: None
        :Returns: str: A HTML string listing all machines with numbering.
        '''
        
        urls_list = self.read_every_url()
        number_list = number(1 , len(urls_list) , None)
        returned_list = []
        
        for i in range(len(urls_list)):
            returned_list.append(urls_list[i])
        
        return f'''
                <tr>
                    <td width="100%" style="padding:0; margin:0;">
                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#ffffff; padding:5px; border-radius:16px;">
                            {' '.join(f'''
                                <tr>
                                <td style="width:25px; text-align:left; vertical-align:top;">{number_list[i]}</td>
                                <td style="width:40px; text-align:left; vertical-align:top; padding-right:8px;">{returned_list[i]}</td>
                                </tr>
                                <tr>
                                    {'<br>' if i < len(number_list)-1  else ''}
                                </tr>
                              '''
                              for i in range(len(number_list)))
                            }
                        </table>
                    </td>
                </tr>
                '''