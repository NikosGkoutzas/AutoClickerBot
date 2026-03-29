from .read_email_interface import ReadEmailInterface
from .process_emails_interface import ProcessEmailsInterface
from .send_email_interface import SendEmailInterface
from ..files.read_files_interface import ReadFilesInterface
from ..files.reset_files_interface import ResetFilesInterface
from ..files.write_files_interface import WriteFilesInterface
from ..driver.driver_interface import DriverInterface
from ..action.action_interface import ActionInterface
from dotenv import load_dotenv
import email.message
import inject
import imaplib
import os
import email


class ReadEmail(ReadEmailInterface):
    @inject.autoparams()
    def __init__(self,
                 process_emails_interface: ProcessEmailsInterface,
                 send_email_interface: SendEmailInterface,
                 read_files_interface: ReadFilesInterface,
                 reset_files_interface: ResetFilesInterface,
                 write_files_interface: WriteFilesInterface,
                 driver_interface: DriverInterface,
                 action_interface: ActionInterface):

        self.process_emails = process_emails_interface
        self.send_email = send_email_interface
        self.read_files = read_files_interface
        self.reset_files = reset_files_interface
        self.write_files = write_files_interface
        self.driver = driver_interface
        self.action = action_interface

    def fetch_last_emails(self) -> None:
        '''
        Connects to the configured Gmail inbox and processes the most recent emails.

        The function retrieves the last N emails from the inbox (as defined in the
        environment configuration) and inspects their subjects and contents to
        detect supported commands, such as: - adding or removing links,
                                            - requesting application progress,
                                            - updating login credentials,
                                            - triggering a new version update,
                                            - starting or stopping a TeamViewer connection,
                                            - retrieving all available links.

        For each supported command type, only the most recent relevant
        email is processed to avoid duplicate or conflicting actions.

        :Parameters: None
        :Returns: None
        '''
        try:
            # server domain
            self.SMTP_SERVER = 'imap.gmail.com'
            self.SMTP_PORT = 993                                                        # port
            # connect to gmail server
            mail = imaplib.IMAP4_SSL(self.SMTP_SERVER)
            load_dotenv(override=True)
            mail.login(os.getenv('email_sender'), os.getenv(
                'email_sender_password'))  # login to gmail with credentials
            # select inbox
            mail.select('inbox')
            # get the last X recent emails
            number_of_recent_emails = int(
                os.getenv('read_number_of_recent_emails'))
            _, data = mail.uid('search', None, 'ALL')
            # first 20 recent unique email ids
            uids = data[0].split()[-number_of_recent_emails:]

            for email_uid in uids:
                status, email_data = mail.uid('fetch', email_uid, '(RFC822)')

                if (status == 'OK'):
                    msg = email.message_from_bytes(email_data[0][1])
                    email_subject = msg['subject'].lower(
                    ).strip() if msg['subject'] else 'No subject'

                    if (email_uid not in self.read_files.read_email_uids()):
                        self._read_add_subject(email_subject,
                                               msg,
                                               email_uid)
                        self._read_remove_subject(email_subject,
                                                  msg,
                                                  email_uid)
                        self._read_connect_via_teamviewer_email(email_subject,
                                                                email_uid)
                        self._read_disconnect_from_teamviewer_email(email_subject,
                                                                    email_uid)
                        self._read_new_version_email(email_subject,
                                                     msg,
                                                     email_uid)
                        self._read_progress_email(email_subject,
                                                  email_uid)
                        self._read_credentials_subject(email_subject,
                                                       msg,
                                                       email_uid)
                        self._read_all_links_email(email_subject,
                                                   email_uid)
                        self._reset_all_files(email_subject,
                                              email_uid)

        except Exception as e:
            print("An error occured: " + str(e))
            self.send_email.send_email_unable_to_read_emails()

    def _read_email_body(self,
                         msg: email.message.Message
                         ) -> list[str]:
        '''
        Extracts and returns the plain text body of an email.

        The function walks through the email parts and collects the content
        of all "text/plain" sections. Empty lines are ignored and the result
        is returned as a list of cleaned text lines.

        :Parameters:msg (email.message.Message): The email message object.

        :Returns: list[str]: A list of non-empty lines extracted from the email body.
        '''
        try:
            body_list = []
            if (msg is not None):
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if (content_type == 'text/plain'):
                        body = part.get_payload(decode=True).decode(
                            'utf-8', errors='ignore')
                        lines = body.splitlines()
                        body = [line.strip() for line in lines if line.strip()]
                        body_list.extend(body)

            return body_list

        except Exception as e:
            print(f'An error occured: {str(e)}')
            self.write_files.write_total_errors()

    def _read_add_subject(self,
                          email_subject: str,
                          msg: email.message.Message,
                          email_uid: int
                          ) -> None:
        '''
        Handles emails with the subject "add" and processes link insertion requests.

        If the email subject matches "add", the email UID is stored to avoid
        re-processing the same message. The email body is parsed to extract links,
        which are then validated and categorized into valid and invalid entries.
        A response email is sent summarizing which links were successfully added
        and which were rejected.

        :Parameters: email_subject (str): The subject of the email being processed.
                     msg (email.message.Message): The email message object.
                     email_uid (int): The unique ID of the email.

        :Returns: None
        '''
        if (email_subject.lower().strip() == 'add'):
            self.write_files.write_email_uids(email_uid)
            list_added_links = self._read_email_body(msg)
            valid_links, invalid_added_links = self.process_emails.process_add_link_email(
                list_added_links)

            for _ in range(len(valid_links)):
                self.write_files.write_number_of_inserted_machines(
                    self.read_files.read_number_of_inserted_machines())

            self.send_email.send_email_link_inserted(valid_links,
                                                     invalid_added_links)

    def _read_remove_subject(self,
                             email_subject: str,
                             msg: email.message.Message,
                             email_uid: int
                             ) -> None:
        '''
        Handles emails with the subject "delete" and processes link removal requests.

        If the email subject matches "delete", the email UID is stored to avoid
        re-processing the same message. The email body is parsed to extract links,
        which are then validated and categorized into successfully removed and
        invalid entries. A response email is sent summarizing the results.

        :Parameters: email_subject (str): The subject of the email being processed.
                     msg (email.message.Message): The email message object.
                     email_uid (int): The unique ID of the email.

        :Returns: None
        '''
        if (email_subject.lower().strip() == 'delete'):
            self.write_files.write_email_uids(email_uid)
            list_removed_links = self._read_email_body(msg)
            valid_links, invalid_removed_links = self.process_emails.process_remove_link_email(
                list_removed_links)

            for _ in range(len(valid_links)):
                self.write_files.write_number_of_removed_machines(
                    self.read_files.read_number_of_removed_machines())

            self.send_email.send_email_link_removed(valid_links,
                                                    invalid_removed_links)

    def _read_progress_email(self,
                             email_subject: str,
                             email_uid: int
                             ) -> None:
        '''
        Handles emails with the subject "progress" and sends a progress status email.

        If the email subject matches "progress", the email UID is stored to avoid
        re-processing the same message and a response email is sent with the current
        application progress information.

        :Parameters: email_subject (str): The subject of the email being processed.
                     email_uid (int): The unique ID of the email.

        :Returns: None
        '''
        if (email_subject.lower().strip() == 'progress'):
            self.write_files.write_email_uids(email_uid)
            self.send_email.send_email_progress()

    def _read_new_version_email(self,
                                email_subject: str,
                                msg: email.message.Message,
                                email_uid: int
                                ) -> None:
        '''
        Handles emails with the subject "update" and triggers the application update process.

        If the email subject matches "update", the email UID is stored to avoid
        re-processing the same message. The email body is parsed to extract the
        requested semantic version update (e.g. major, minor, patch) and the update
        request is validated.

        If the request is valid, the application attempts to download and install
        the new version from GitHub. If the update fails, an error email is sent and
        TeamViewer is opened for manual intervention.

        If the request is invalid or missing, an error email is sent to the user.

        :Parameters: email_subject (str): The subject of the email being processed.
                     msg (email.message.Message): The email message object.
                     email_uid (int): The unique ID of the email.

        :Returns: None
        '''
        if (email_subject.lower().strip() == 'update'):
            self.write_files.write_email_uids(email_uid)
            semantic_versioning = self._read_email_body(msg)
            success, semantic_input = self.process_emails.process_new_version_email(
                semantic_versioning)

            if (success):
                if (not self.process_emails.process_download_new_version_from_github(semantic_input)):
                    self.send_email.send_email_new_version_failed_to_update()

                    if (not self.action.check_if_teamviewer_is_already_connected()):
                        self.action.open_teamviewer()

            else:
                self.send_email.send_email_error_installing_new_version_missing_type()

    def _read_credentials_subject(self,
                                  email_subject: str,
                                  msg: email.message.Message,
                                  email_uid: int
                                  ) -> None:
        '''
        Handles emails with the subject "credentials" and processes credential update requests.

        If the email subject matches "credentials", the email UID is stored to prevent
        duplicate processing. The email body is parsed to extract credential change
        instructions, which are then validated and applied.

        If the credentials are successfully updated, the user is logged out and a new
        login attempt is performed using the updated credentials. A notification email
        is sent to report the result of the operation.

        :Parameters: email_subject (str): The subject of the email being processed.
                     msg (email.message.Message): The email message object.
                     email_uid (int): The unique ID of the email.

        :Returns: None
        '''
        if (email_subject.lower().strip() == 'credentials'):
            self.write_files.write_email_uids(email_uid)
            list_changed_credentials = self._read_email_body(msg)
            credential_messages = self.process_emails.process_change_credentials_email(
                list_changed_credentials)

            if (credential_messages.strip().lower() == 'ok'):
                self.driver.logout()
                self.action.check_login()

            self.send_email.send_email_credentials_updated(credential_messages)

    def _read_connect_via_teamviewer_email(self,
                                           email_subject: str,
                                           email_uid: int
                                           ) -> None:
        '''
        Handles emails with the subject "start teamviewer" and initiates
        a TeamViewer remote access session.

        If the email subject matches "start teamviewer", the email UID is stored
        to prevent duplicate processing and TeamViewer is launched to allow
        remote access to the system.

        :Parameters: email_subject (str): The subject of the email being processed.
                     email_uid (int): The unique ID of the email.

        :Returns: None
        '''
        if (email_subject.lower().strip() == 'start teamviewer'):
            self.write_files.write_email_uids(email_uid)

            if (not self.action.check_if_teamviewer_is_already_connected()):
                self.action.open_teamviewer()

    def _read_disconnect_from_teamviewer_email(self,
                                               email_subject: str,
                                               email_uid: int
                                               ) -> None:
        '''
        Handles emails with the subject "stop teamviewer" and terminates
        an active TeamViewer remote access session.

        If the email subject matches "stop teamviewer", the email UID is stored
        to prevent duplicate processing and TeamViewer is closed to disable
        remote access to the system.

        :Parameters: email_subject (str): The subject of the email being processed.
                     email_uid (int): The unique ID of the email.

        :Returns: None
        '''
        if (email_subject.lower().strip() == 'stop teamviewer'):
            self.write_files.write_email_uids(email_uid)
            if (not self.action.check_if_teamviewer_is_already_disconnected()):
                self.action.close_teamviewer()

    def _read_all_links_email(self,
                              email_subject: str,
                              email_uid: int
                              ) -> None:
        '''
        Handles emails with the subject "links" and sends back all stored links.

        If the email subject matches "links", the email UID is stored to avoid
        duplicate processing and a response email is sent containing the full
        list of links currently stored in the system.

        :Parameters: email_subject (str): The subject of the email being processed.
                     email_uid (int): The unique ID of the email.

        :Returns: None
        '''
        if (email_subject.lower().strip() == 'links'):
            self.write_files.write_email_uids(email_uid)
            self.send_email.send_email_all_links()

    def _reset_all_files(self,
                         email_subject: str,
                         email_uid: int
                         ) -> None:
        '''
        Reset all files of the application.

        :Parameters: email_subject (str): The subject of the email being processed.
                     email_uid (int): The unique ID of the email.

        :Returns: None
        '''
        if (email_subject.lower().strip() == 'reset'):
            self.write_files.write_email_uids(email_uid)
            self.reset_files.reset_all_files()
            self.reset_files.reset_all_updates_per_machine()
            self.send_email.send_email_reset_all_files()
