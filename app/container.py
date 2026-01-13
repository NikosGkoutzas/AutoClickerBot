def configure_dependencies(binder):
    # Files
    from .files.read_files_interface import ReadFilesInterface
    from .files.read_files import ReadFiles
    from .files.write_files_interface import WriteFilesInterface
    from .files.write_files import WriteFiles
    from .files.reset_files_interface import ResetFilesInterface
    from .files.reset_files import ResetFiles

    binder.bind_to_constructor(ReadFilesInterface , ReadFiles)
    binder.bind_to_constructor(WriteFilesInterface , WriteFiles)
    binder.bind_to_constructor(ResetFilesInterface , ResetFiles)

    # Email messages
    from .messages.email_messages_interface import EmailMessagesInterface
    from .messages.email_messages import EmailMessages
    binder.bind_to_constructor(EmailMessagesInterface , EmailMessages)

    # Browser
    from .browser_launcher.chrome_boot_interface import ChromeBootInterface
    from .browser_launcher.chrome_boot import ChromeBoot
    binder.bind_to_constructor(ChromeBootInterface , ChromeBoot)

    # Driver
    from .driver.driver_interface import DriverInterface
    from .driver.driver import Driver
    binder.bind_to_constructor(DriverInterface , Driver)

    # Calculations
    from .calculations.calculations_interface import CalculationInterface
    from .calculations.calculations import Calculations
    binder.bind_to_constructor(CalculationInterface , Calculations)

    # Email
    from .email.send_email_interface import SendEmailInterface
    from .email.send_email import SendEmail
    from .email.process_emails_interface import ProcessEmailsInterface
    from .email.process_emails import ProcessEmails
    from .email.read_email_interface import ReadEmailInterface
    from .email.read_email import ReadEmail

    binder.bind_to_constructor(SendEmailInterface , SendEmail)
    binder.bind_to_constructor(ProcessEmailsInterface , ProcessEmails)
    binder.bind_to_constructor(ReadEmailInterface , ReadEmail)

    # Action
    from .action.action_interface import ActionInterface
    from .action.action import Action
    binder.bind_to_constructor(ActionInterface , Action)

    # Internet
    from .internet.internet_interface import InternetInterface
    from .internet.internet import Internet
    binder.bind_to_constructor(InternetInterface , Internet)

    # Run
    from .run.run_interface import RunInterface
    from .run.run import Run
    binder.bind_to_constructor(RunInterface , Run)