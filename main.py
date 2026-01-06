from app.driver.driver import Driver
from app.browser_launcher.chrome_boot import ChromeBoot
from .files.read_files import ReadFiles
from .files.write_files import WriteFiles
from .action.action import Action
from .messages.email_messages import EmailMessages
from .calculations.calculations import Calculations
from .email.send_email import SendEmail
from .driver.driver import Driver
from .email.read_email import ReadEmail
from .email.process_emails import ProcessEmails
from .internet.internet import Internet
from .action.action import Action
from .run.run import Run
import time


if(__name__ == '__main__'):
    boot = ChromeBoot()
    boot.boot()
    rf = ReadFiles()
    wf = WriteFiles(rf)
    e = EmailMessages()
    driver = Driver(wf)
    calc = Calculations(driver , rf , wf)
    email = SendEmail(rf , e , calc)
    action = Action(driver , rf , wf , email)
    internet = Internet(email , rf , wf)
    process_emails = ProcessEmails(rf , wf)
    read_email = ReadEmail(process_emails , email , rf , wf)
    run = Run(calc,internet,action,rf,wf,email,driver , read_email)
    #run.run()
    wf.reset_all_files()