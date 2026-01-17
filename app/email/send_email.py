from .send_email_interface import SendEmailInterface
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..files.read_files_interface import ReadFilesInterface
from ..messages.email_messages_interface import EmailMessagesInterface
from ..calculations.calculations_interface import CalculationInterface
from datetime import datetime
import smtplib , os , inject



class SendEmail(SendEmailInterface):
    @inject.autoparams()
    def __init__(self , 
                 read_files_interface: ReadFilesInterface , 
                 email_message_interface: EmailMessagesInterface , 
                 calculations_interface: CalculationInterface
                 ):
        
        self.read_files = read_files_interface
        self.email_message = email_message_interface
        self.calculations = calculations_interface
        
        
    def send_email_general(self , title: str , body_message: str , email_receiver: str) -> None:
        message = MIMEMultipart('alternative')
        message['subject'] = title
        email_sender = os.getenv('email_sender')
        message['From'] = email_sender
        message['To'] = email_receiver
        
        HTML_BODY = MIMEText(body_message, 'html')
        message.attach(HTML_BODY)
        server = smtplib.SMTP("smtp.gmail.com:587")    
        password = os.getenv('email_sender_password')
        server.starttls()
        server.login(email_sender , password)
        server.sendmail(email_sender , email_receiver , message.as_string())
        server.quit()


    def send_email_to_all_receivers(self , title: str , message: str) -> None:
        self.send_email_general(title=title , body_message=message , email_receiver=os.getenv('email_receiver_1'))
        #self.send_email_general(title=title , body_message=message , email_receiver=os.getenv('email_receiver_2'))


    def send_email_launch(self) -> None:
        self.send_email_to_all_receivers(self.email_message.launch_app_title_message() , self.email_message.launch_app_body_message())


    def send_email_no_internet_connection(self , occured: str , restored: str) -> None:
        self.send_email_to_all_receivers(self.email_message.no_internet_title_message() , self.email_message.no_internet_body_message(occured , restored))


    def send_email_daily_report(self) -> None:
        self.send_email_to_all_receivers(self.email_message.daily_report_title_message() , self.email_message.daily_report_body_message(total_updates_of_day=self.read_files.read_total_updates() ,
                                                                                                                                        total_issues=self.read_files.read_total_errors() ,
                                                                                                                                        total_machines=self.read_files.read_number_of_urls() ,
                                                                                                                                        inserted_machines=self.read_files.read_number_of_inserted_machines() ,
                                                                                                                                        removed_machines=self.read_files.read_number_of_removed_machines() ,
                                                                                                                                        updated_result=self.calculations.extract_update_results())
                                                                                                                                        )


    def send_email_new_version_updated(self) -> None:
        self.send_email_to_all_receivers(self.email_message.new_version_started_title_message() , self.email_message.new_version_started_body_message(self.read_files.read_app_version()))
    
    
    def send_email_link_inserted(self , list_added_links: list[str] , list_added_invalied_links: list[str]) -> None:
        self.send_email_to_all_receivers(self.email_message.machine_inserted_title_message(len(list_added_links) , list_added_invalied_links) , self.email_message.machine_inserted_body_message(list_added_links , list_added_invalied_links , self.read_files.read_number_of_urls()))


    def send_email_link_removed(self , list_removed_links: list[str] , list_removed_invalied_links: list[str]) -> None:
        self.send_email_to_all_receivers(self.email_message.machine_removed_title_message(len(list_removed_links) , list_removed_invalied_links) , self.email_message.machine_removed_body_message(list_removed_links , list_removed_invalied_links , self.read_files.read_number_of_urls()))


    def send_email_credentials_updated(self , cond_str: str) -> None:
        self.send_email_to_all_receivers(self.email_message.credentails_update_title_message(cond_str) , self.email_message.credentials_update_body_message(cond_str))


    def send_email_progress(self) -> None:
        self.send_email_to_all_receivers(self.email_message.progress_title_message() , self.email_message.progress_body_message(number_of_machines=self.read_files.read_number_of_urls() ,
                                                                                                                                current_updates=self.read_files.read_total_updates() ,
                                                                                                                                current_errors=self.read_files.read_total_errors() ,
                                                                                                                                most_recent_error=self.read_files.read_error_datetime() ,
                                                                                                                                added_machines=self.read_files.read_number_of_inserted_machines() ,
                                                                                                                                removed_machines=self.read_files.read_number_of_removed_machines() ,
                                                                                                                                captcha_challenges=self.read_files.read_number_of_captcha_challenges() ,
                                                                                                                                version=self.read_files.read_app_version())
                                                                                                                                )


    def send_email_new_version_failed_to_update(self) -> None:
        self.send_email_to_all_receivers(self.email_message.error_installing_new_version_title_message() , self.email_message.general_error_installing_new_version_body_message())
        
        
    def send_email_error_installing_new_version_missing_type(self) -> None:
        self.send_email_to_all_receivers(self.email_message.error_installing_new_version_title_message() , self.email_message.error_installing_new_version_body_message_missing_type())
        
        
    def send_email_all_links(self) -> None:
        self.send_email_to_all_receivers(self.email_message.see_all_available_links_title_message() , self.email_message.see_all_available_links_body_message(self.calculations.list_of_all_machines()))
        
        
    def send_email_unable_to_login(self) -> None:
        self.send_email_to_all_receivers(self.email_message.unable_to_login_title_message() , self.email_message.unable_to_login_body_message())
        
        
    def send_email_captcha_failed_to_solve(self) -> None:
        self.send_email_to_all_receivers(self.email_message.captcha_failed_to_solve_title_message() , self.email_message.captcha_failed_to_solve_body_message())
        
    
    def send_email_every_10_errors_occured(self , errors: int) -> None:
        self.send_email_to_all_receivers(self.email_message.notify_every_10_errors_title_message() , self.email_message.notify_every_10_errors_body_message(errors))
        
        
    def send_email_connect_via_teamviewer(self) -> None:
        self.send_email_to_all_receivers(self.email_message.connect_via_teamviewer_title_message() , self.email_message.connect_via_teamviewer_body_message())