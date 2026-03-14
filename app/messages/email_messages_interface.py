from abc import ABC, abstractmethod
from datetime import datetime


class EmailMessagesInterface(ABC):
    @abstractmethod
    def time_message(self) -> str:
        pass

    @abstractmethod
    def built_with_python_and_copyright_message(self) -> str:
        pass

    @abstractmethod
    def launch_app_subject_message(self) -> str:
        pass

    @abstractmethod
    def launch_app_body_message(self) -> str:
        pass

    @abstractmethod
    def no_internet_subject_message(self) -> str:
        pass

    @abstractmethod
    def no_internet_body_message(self, occured: str, restored: str):
        pass

    @abstractmethod
    def daily_report_subject_message(self) -> str:
        pass

    @abstractmethod
    def daily_report_body_message(self,
                                  total_updates_of_day: int,
                                  total_machines: int,
                                  general_issues: int,
                                  internet_issues: int,
                                  captcha_challenges: int,
                                  inserted_machines: int,
                                  removed_machines: int,
                                  app_version: int,
                                  updated_result: str) -> str:
        pass

    @abstractmethod
    def new_version_started_subject_message(self) -> str:
        pass

    @abstractmethod
    def new_version_started_body_message(self) -> str:
        pass

    @abstractmethod
    def credentails_update_subject_message(self, cond_str: str) -> str:
        pass

    @abstractmethod
    def credentials_update_body_message(self, cond_str: str) -> str:
        pass

    @abstractmethod
    def progress_subject_message(self) -> str:
        pass

    @abstractmethod
    def progress_body_message(self,
                              number_of_machines: int,
                              current_updates: int,
                              current_errors: int,
                              internet_errors: int,
                              most_recent_error: str,
                              added_machines: int,
                              removed_machines: int,
                              progress_body_message: int,
                              version: str
                              ) -> str:
        pass

    @abstractmethod
    def machine_inserted_subject_message(self, number_of_inserted_machines: int, invalid_machines: list[str]) -> str:
        pass

    @abstractmethod
    def machine_inserted_body_message(self, list_of_added_machines: list[str], not_existing_machines: list[str], number_of_machines: int) -> str:
        pass

    @abstractmethod
    def machine_removed_subject_message(self, number_of_removed_machines: int, not_existing_machines: list[str]) -> str:
        pass

    @abstractmethod
    def machine_removed_body_message(self, list_of_removed_machines: list[str], not_existing_machines: list[str], number_of_machines: int) -> str:
        pass

    @abstractmethod
    def error_installing_new_version_subject_message(self) -> str:
        pass

    @abstractmethod
    def general_error_installing_new_version_body_message(self) -> str:
        pass

    @abstractmethod
    def error_installing_new_version_body_message_missing_type(self) -> str:
        pass

    @abstractmethod
    def see_all_available_links_subject_message(self) -> str:
        pass

    @abstractmethod
    def see_all_available_links_body_message(self, list_of_all_machines: str) -> str:
        pass

    @abstractmethod
    def unable_to_login_subject_message(self) -> str:
        pass

    @abstractmethod
    def unable_to_login_body_message(self) -> str:
        pass

    @abstractmethod
    def login_error_body_message(self) -> str:
        pass

    @abstractmethod
    def login_error_subject_message(self) -> str:
        pass

    @abstractmethod
    def captcha_failed_to_be_solved_subject_message(self) -> str:
        pass

    @abstractmethod
    def captcha_failed_to_be_solved_in_login_body_message(self) -> str:
        pass

    @abstractmethod
    def captcha_failed_to_be_solved_body_message(self) -> str:
        pass

    @abstractmethod
    def notify_every_10_errors_subject_message(self) -> str:
        pass

    @abstractmethod
    def notify_every_10_errors_body_message(self, errors: int) -> str:
        pass

    @abstractmethod
    def teamviewer_connected_subject_message(self) -> str:
        pass

    @abstractmethod
    def teamviewer_connected_body_message(self) -> str:
        pass

    @abstractmethod
    def teamviewer_disconnected_subject_message(self) -> str:
        pass

    @abstractmethod
    def teamviewer_disconnected_body_message(self) -> str:
        pass

    @abstractmethod
    def teamviewer_connection_already_opened_subject_message(self) -> str:
        pass

    @abstractmethod
    def teamviewer_connection_already_opened_body_message(self) -> str:
        pass

    @abstractmethod
    def teamviewer_connection_already_closed_subject_message(self) -> str:
        pass

    @abstractmethod
    def teamviewer_connection_already_closed_body_message(self) -> str:
        pass

    @abstractmethod
    def failed_to_open_teamviewer_subject_message(self) -> str:
        pass

    @abstractmethod
    def failed_to_open_teamviewer_body_message(self) -> str:
        pass

    @abstractmethod
    def failed_to_close_teamviewer_subject_message(self) -> str:
        pass

    @abstractmethod
    def failed_to_close_teamviewer_body_message(self) -> str:
        pass
