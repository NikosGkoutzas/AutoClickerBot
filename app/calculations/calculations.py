from .calculations_interface import CalculationInterface
from ..driver.driver_interface import DriverInterface
from ..files.read_files_interface import ReadFilesInterface
from ..files.write_files_interface import WriteFilesInterface
from datetime import datetime
from ..messages.numbers import number
import os , time , inject



class Calculations(CalculationInterface):
    @inject.autoparams()
    def __init__(self , 
                 driver_interface: DriverInterface , 
                 read_files_interface: ReadFilesInterface , 
                 write_files_interface: WriteFilesInterface
                 ):
        
        self.driver = driver_interface
        self.read_files = read_files_interface
        self.write_files = write_files_interface




    def app_in_time(self) -> bool:
        end_time_from_file = str(self.read_files.read_end_time())
        end_time_hour = int(end_time_from_file.split(':')[0])
        end_time_minute = int(end_time_from_file.split(':')[1])

        start_time_from_file = str(self.read_files.read_start_time())
        start_time_hour = int(start_time_from_file.split(':')[0])
        start_time_minute = int(start_time_from_file.split(':')[1])

        end_time = datetime.now().replace(hour=end_time_hour , minute=end_time_minute , second=0 , microsecond=0)
        start_time = datetime.now().replace(hour=start_time_hour , minute=start_time_minute , second=0 , microsecond=0)
        current_time = datetime.now()

        return current_time >= start_time and current_time < end_time




    def updates_completed(self) -> bool:
        current_updates = self.read_files.read_total_updates()
        total_updates = int(os.getenv('total_required_updates'))
        return current_updates == total_updates




    def extract_update_results(self) -> str:
        urls_list = self.read_files.read_every_url()
        slug_list = []
        pretty_links = []

        for url in urls_list:
            inner_list = url.split('-')[1:]
            for i , words in enumerate(inner_list):
                if('www' in words or 'zitiste' in words):
                    inner_list = inner_list[:i]
                    break
            slug_list.append(' '.join(inner_list))

        for i in range(len(slug_list)):
            pretty_links.append(f'<a href="{urls_list[i]}" target="_blank">{slug_list[i]}</a><br>')

        updates_per_url = self.read_files.read_update_number_of_machine()
        number_list = number(1 , len(pretty_links) , None)

        summary = f'''
                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#ffffff; padding:15px; border-radius:16px;">
                        <tr>
                            <td style='width:50px; text-align:left; vertical-align:top;'>🔢</td>
                            <td style='width:160px; text-align:center; vertical-align:top;'>🔄</td>
                            <td style='width:150px; text-align:center;vertical-align:top;'>📎</td>
                        </tr>
                        <tr><br></tr>
                    
                        {' '.join(f'''
                                    <tr>
                                        <td style='width:50px; text-align:left; vertical-align:top;'>{number_list[i]}</td>
                                        <td style='width:160px; text-align:center; vertical-align:top;'><b>{updates_per_url[i]}</b></td>
                                        <td style='width:150px; text-align:center;vertical-align:top;'>{pretty_links[i]}</td>
                                    </tr>
                                    <tr>
                                        {'<br>' if i < len(pretty_links)-1  else ''}
                                    </tr>
                                 '''
                            for i in range(len(pretty_links)))
                        }
                    </table>
                    '''
        
        final_html = f'''
                        {summary}
                      '''
        
        return final_html






    def sleep_till_next_day(self) -> None:
        try:
            time.sleep(10*60) # wait 10 minutes, until 00:05
            start_time_from_file = str(self.read_files.read_start_time())
            start_time_hour = int(start_time_from_file.split(':')[0])
            current_time = datetime.now()
            time_of_sleep_minus_10_sec = datetime.now().replace(hour=start_time_hour - 1 , minute=59 , second=50 , microsecond=0)
            seconds_difference = (time_of_sleep_minus_10_sec - current_time).total_seconds()
            
            time.sleep(seconds_difference)

        except Exception as e:
            print(f'An error occured while trying to sleep till next day: {str(e)}')
            self.write_files.write_total_errors()
        

            
            
            
    
    def list_of_all_machines(self) -> str:
        urls_list = self.read_files.read_every_url()
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
            
            
            
            
    def compute_time_of_new_version_installation(self) -> datetime.time:
        import datetime
        return (datetime.datetime.now() + datetime.timedelta(minutes=7 , microseconds=0)).time().strftime('%H:%M:%S')
    
    
    
    
    
    def delay_between_updates(self) -> int:
        total_required_updates = int(os.getenv('total_required_updates')) 
        total_current_updates = self.read_files.read_total_updates()
        current_time = datetime.now().replace(microsecond=0)
        
        end_time_from_file = str(self.read_files.read_end_time())
        end_time_hour = int(end_time_from_file.split(':')[0])
        end_time_minutes = int(end_time_from_file.split(':')[1])
        end_time_seconds = int(end_time_from_file.split(':')[2])
        end_time = datetime.now().replace(hour=end_time_hour , minute=end_time_minutes , second=end_time_seconds , microsecond=0)

        if(total_required_updates - total_current_updates <= 0):
            return 1
        
        delay = (end_time - current_time).total_seconds() / (total_required_updates - total_current_updates) if(end_time > current_time) else 1
        return max(1 , delay)
    
    
    
    
    def check_emails(self) -> bool:
        dif_minutes = 20
        last_time_check_emails = self.read_files.read_check_email_every_20_minutes()
        current_time = datetime.now().time().replace(microsecond=0)
        current_time_minutes = current_time.hour * 60 + current_time.minute + current_time.second / 60
        last_time_check_emails_minutes = last_time_check_emails.hour * 60 + last_time_check_emails.minute + last_time_check_emails.second / 60

        result = current_time_minutes - last_time_check_emails_minutes >= dif_minutes

        if(result):
            self.write_files.write_check_email_every_20_minutes(current_time.strftime('%H:%M:%S'))
        
        return result
    
    
    
    def updates_completed_earlier_wait(self) -> None:
        current_time = datetime.now().time().replace(microsecond=0)
        current_time_in_seconds = current_time.hour * 3600 + current_time.minute * 60 + current_time.second
        end_time = datetime.now().replace(hour=23 , minute=54 , second=58 , microsecond=0)
        end_time_in_seconds = end_time.hour * 3600 + end_time.minute * 60 + end_time.second
        
        if(current_time_in_seconds < end_time_in_seconds):
            print(f'Updates were completed earlier than expected. Waiting until 23:55...')
            time.sleep(end_time_in_seconds - current_time_in_seconds)