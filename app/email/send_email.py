from .send_email_interface import SendEmailInterface
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..files.read_files_interface import ReadFilesInterface
from ..messages.email_messages_interface import EmailMessagesInterface
from ..calculations.calculations_interface import CalculationInterface
from dotenv import load_dotenv
import smtplib
import os
import inject


class SendEmail(SendEmailInterface):
    @inject.autoparams()
    def __init__(self,
                 read_files_interface: ReadFilesInterface,
                 email_message_interface: EmailMessagesInterface,
                 calculations_interface: CalculationInterface
                 ):

        self.read_files = read_files_interface
        self.email_message = email_message_interface
        self.calculations = calculations_interface

    def send_email_general(self, subject: str, body_message: str, email_receiver: str) -> None:
        '''
        Sends an HTML email using the configured SMTP email account.

        The function constructs an email message with the given subject and
        HTML body content, establishes a secure connection to the SMTP server,
        authenticates using credentials stored in environment variables, and
        sends the email to the specified recipient.

        :Parameters: subject (str): The subject line of the email.
                     body_message (str): The HTML-formatted body content of the email.
                     email_receiver (str): The recipient email address.
        :Returns: None
        '''
        message = MIMEMultipart('alternative')
        message['subject'] = subject
        load_dotenv(override=True)
        email_sender = os.getenv('email_sender')
        message['From'] = email_sender
        message['To'] = email_receiver

        HTML_BODY = MIMEText(body_message, 'html')
        message.attach(HTML_BODY)
        server = smtplib.SMTP("smtp.gmail.com:587")
        password = os.getenv('email_sender_password')
        server.starttls()
        server.login(email_sender, password)
        server.sendmail(email_sender, email_receiver, message.as_string())
        server.quit()

    def send_email_to_all_receivers(self, subject: str, message: str) -> None:
        '''
        Sends an email with the specified subject and message to all
        configured email recipients.

        :Parameters: subject (str): The subject line of the email.
                     message (str): The HTML-formatted body content of the email.
        :Returns: None
        '''
        load_dotenv(override=True)
        self.send_email_general(subject=subject,
                                body_message=message,
                                email_receiver=os.getenv('email_receiver_1'))
        # self.send_email_general(subject=subject,
        #                        body_message=message,
        #                        email_receiver=os.getenv('email_receiver_2'))

    def send_email_launch(self) -> None:
        '''
        Sends a notification email indicating that the application has started.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.launch_app_subject_message(),
                                         self.email_message.launch_app_body_message())

    def send_email_no_internet_connection(self, occured: str, restored: str) -> None:
        '''
        Sends a notification email about an internet connection outage and its restoration time.

        :Parameters: occured (str): The time the internet connection was lost.
                     restored (str): The time the internet connection was restored.
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.no_internet_subject_message(),
                                         self.email_message.no_internet_body_message(occured, restored))

    def send_email_daily_report(self) -> None:
        '''
        Sends a daily summary email with application statistics and results.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.daily_report_subject_message(), self.email_message.daily_report_body_message(total_updates_of_day=self.read_files.read_total_updates(),
                                                                                                                                         total_machines=self.read_files.read_number_of_urls(),
                                                                                                                                         general_issues=self.read_files.read_total_errors(),
                                                                                                                                         internet_issues=self.read_files.read_internet_errors(),
                                                                                                                                         captcha_challenges=self.read_files.read_number_of_captcha_challenges(),
                                                                                                                                         inserted_machines=self.read_files.read_number_of_inserted_machines(),
                                                                                                                                         removed_machines=self.read_files.read_number_of_removed_machines(),
                                                                                                                                         app_version=self.read_files.read_app_version(),
                                                                                                                                         updated_result=self.calculations.extract_update_results())
                                         )

    def send_email_new_version_updated(self) -> None:
        '''
        Sends a notification email indicating that a new application
        version has been successfully installed.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.new_version_started_subject_message(
        ), self.email_message.new_version_started_body_message(self.read_files.read_app_version()))

    def send_email_link_inserted(self, list_added_links: list[str], list_added_invalied_links: list[str]) -> None:
        '''
        Sends a notification email with the results of link insertion.

        :Parameters: list_added_links (list[str]): Successfully added links.
                     list_added_invalied_links (list[str]): Links that failed validation.
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.machine_inserted_subject_message(len(list_added_links), list_added_invalied_links),
                                         self.email_message.machine_inserted_body_message(list_added_links, list_added_invalied_links, self.read_files.read_number_of_urls()))

    def send_email_link_removed(self, list_removed_links: list[str], list_removed_invalied_links: list[str]) -> None:
        '''
        Sends a notification email with the results of link removal.

        :Parameters: list_removed_links (list[str]): Successfully removed links.
                     list_removed_invalied_links (list[str]): Links that failed validation.
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.machine_removed_subject_message(len(list_removed_links), list_removed_invalied_links),
                                         self.email_message.machine_removed_body_message(list_removed_links, list_removed_invalied_links, self.read_files.read_number_of_urls()))

    def send_email_credentials_updated(self, cond_str: str) -> None:
        '''
        Sends a notification email about the result of a credentials update request.

        :Parameters: cond_str (str): Message describing the outcome of the credentials update.
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.credentails_update_subject_message(cond_str),
                                         self.email_message.credentials_update_body_message(cond_str))

    def send_email_progress(self) -> None:
        '''
        Sends a progress report email with current application statistics.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.progress_subject_message(), self.email_message.progress_body_message(number_of_machines=self.read_files.read_number_of_urls(),
                                                                                                                                 current_updates=self.read_files.read_total_updates(),
                                                                                                                                 current_errors=self.read_files.read_total_errors(),
                                                                                                                                 internet_errors=self.read_files.read_internet_errors(),
                                                                                                                                 most_recent_error=str(
                                                                                                                                     self.read_files.read_error_time()),
                                                                                                                                 added_machines=self.read_files.read_number_of_inserted_machines(),
                                                                                                                                 removed_machines=self.read_files.read_number_of_removed_machines(),
                                                                                                                                 captcha_challenges=self.read_files.read_number_of_captcha_challenges(),
                                                                                                                                 version=self.read_files.read_app_version())
                                         )

    def send_email_new_version_failed_to_update(self) -> None:
        '''
        Sends a notification email indicating that the application
        failed to install the new version.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.error_installing_new_version_subject_message(),
                                         self.email_message.general_error_installing_new_version_body_message())

    def send_email_error_installing_new_version_missing_type(self) -> None:
        '''
        Sends a notification email indicating that the new version
        update type was missing or invalid.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.error_installing_new_version_subject_message(),
                                         self.email_message.error_installing_new_version_body_message_missing_type())

    def send_email_all_links(self) -> None:
        '''
        Sends a notification email containing all available machine links.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.see_all_available_links_subject_message(),
                                         self.email_message.see_all_available_links_body_message(self.read_files.retrieve_all_machines()))

    def send_email_unable_to_login(self) -> None:
        '''
        Sends a notification email indicating that the application
        was unable to log in.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.unable_to_login_subject_message(),
                                         self.email_message.unable_to_login_body_message())

    def send_email_login_error(self) -> None:
        '''
        Sends a notification email indicating that application is unabled to login due to unexpected error.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.login_error_subject_message(),
                                         self.email_message.login_error_body_message())

    def send_email_captcha_failed_to_be_solved_in_login(self) -> None:
        '''
        Sends a notification email indicating that a CAPTCHA
        challenge failed during login.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.captcha_failed_to_be_solved_subject_message(),
                                         self.email_message.captcha_failed_to_be_solved_in_login_body_message())

    def send_email_captcha_failed_to_be_solved(self) -> None:
        '''
        Sends a notification email indicating that a CAPTCHA
        challenge failed to be solved.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.captcha_failed_to_be_solved_subject_message(),
                                         self.email_message.captcha_failed_to_be_solved_body_message())

    def send_email_every_10_errors_occured(self, errors: int) -> None:
        '''
        Sends a notification email when every 10 errors have occurred.

        :Parameters: errors (int): The total number of errors detected.
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.notify_every_10_errors_subject_message(),
                                         self.email_message.notify_every_10_errors_body_message(errors))

    def send_email_teamviewer_connected(self) -> None:
        '''
        Sends a notification email indicating that TeamViewer
        remote access has been successfully enabled.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.teamviewer_connected_subject_message(),
                                         self.email_message.teamviewer_connected_body_message())

    def send_email_teamviewer_disconnected(self) -> None:
        '''
        Sends a notification email indicating that TeamViewer
        remote access has been disabled.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.teamviewer_disconnected_subject_message(),
                                         self.email_message.teamviewer_disconnected_body_message())

    def send_email_teamviewer_connection_already_opened(self) -> None:
        '''
        Sends a notification email indicating that a TeamViewer
        remote access session is already active.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.teamviewer_connection_already_opened_subject_message(),
                                         self.email_message.teamviewer_connection_already_opened_body_message())

    def send_email_teamviewer_connection_already_closed(self) -> None:
        '''
        Sends a notification email indicating that the TeamViewer
        remote access session is already closed.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.teamviewer_connection_already_closed_subject_message(),
                                         self.email_message.teamviewer_connection_already_closed_body_message())

    def send_email_failed_to_open_teamviewer(self) -> None:
        '''
        Sends a notification email indicating that the application
        failed to open TeamViewer.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.failed_to_open_teamviewer_subject_message(),
                                         self.email_message.failed_to_open_teamviewer_body_message())

    def send_email_failed_to_close_teamviewer(self) -> None:
        '''
        Sends a notification email indicating that the application
        failed to close TeamViewer.

        :Parameters: None
        :Returns: None
        '''
        self.send_email_to_all_receivers(self.email_message.failed_to_close_teamviewer_subject_message(),
                                         self.email_message.failed_to_close_teamviewer_body_message())

    def send_email_unable_to_read_emails(self) -> None:
        self.send_email_to_all_receivers(self.email_message.email_message_unable_to_read_emails_subject_message(),
                                         self.email_message.email_message_unable_to_read_emails_body_message())

    def send_email_reset_all_files(self) -> None:
        self.send_email_to_all_receivers(self.email_message.email_message_reset_all_files_subject_message(),
                                         self.email_message.email_message_reset_all_files_body_message())
