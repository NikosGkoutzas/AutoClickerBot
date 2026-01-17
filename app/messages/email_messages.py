from .email_messages_interface import EmailMessagesInterface
from datetime import datetime
import os


class EmailMessages(EmailMessagesInterface):
    def time_message(self) -> str:
        time_message = datetime.now().replace(microsecond=0).strftime('%b %d, %Y - %H:%M:%S')
        return f'''
        <table align='center' cellpadding="0" cellspacing="0" style="background-color:#007BFF; padding:7px; border-radius:12px; width:100%;">
            <tr>
                <td align="center"><b>{time_message}</b></td>
            </tr>
        </table>
        '''
        
        
        
    def built_with_python_and_copyright_message(self) -> str:
        copyright = f'<b>© {datetime.now().year} Nikos Gkoutzas.<br><b>All Rights Reserved.</b>'


        built_with_python = '<i>Built with Python</i>'
        
        return f'''
                <table align="center" width="100%" cellpadding="0" cellspacing="0" style="background-color:#007BFF; padding:7px; border-radius:12px;">
                    <tr>
                        <td align="center">{built_with_python}</td>
                    </tr>
                    <tr>
                        <td align="center">{copyright}</td>
                    </tr>
                </table>
                '''

        
        
        
    def launch_app_title_message(self) -> str:
        return '✅ Application Launch'
        
        
        
    def launch_app_body_message(self) -> str:
        developer = 'Nikos Gkoutzas'
        developer_email = 'nickgkoutzas@gmail.com'
        body_add = 'The urls you want to add one per line.'
        action_add = 'Adds the provided urls to the app.'
        body_delete = 'The urls you want to remove one per line.'
        action_delete = 'Removes the specified urls from the app.'
        body_update = 'Provide the semantic versioning'
        body_update_semantic_versioning = '(Major, Minor or Patch).'
        action_update = 'Updates the app to the latest version from GitHub.'
        action_progress = 'Returns a summary of the app\'s current status.'
        action_links = 'Returns all available links.'
        body_credentials = 'Provide only the field you want to update (username/password). Eg:'
        body_example_username_credential = 'username: admin'
        body_example_password_credential = 'password: •••••'
        action_credentials = 'Updates the user login credentials.'
        email = os.getenv('email_sender')
        perform_email = f'To perform an action, send an email to {email}.'
        summary_email = 'A summary email is sent every day at 23:55.'
        confirmation_email = 'A confirmation email will be sent.'
        
        ##### prepei na to kanw me inject <<<<<<<<<<<<<<<<<<<<
        from ..files.read_files import ReadFiles
        rf = ReadFiles()
        app_version = rf.read_app_version()
        
        return f'''
        <table cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed; width:100%;">
            <tr>
                <td style="padding:0; margin:0;">
                    {self.time_message()}
                </td>
            </tr>
            <tr>
                <td align='center'>
                    <table width="100%" cellpadding="0" cellspacing="0">
                        <tr>
                            <td colspan="2" align="center"><u><b><br>About</b></u></td>
                        </tr>
                        <tr><br></tr>
                        <tr>
                            <td><i>Developer</i></td>
                            <td align="right">{developer}</td>
                        </tr>
                        <tr>
                            <td><i>Email</i></td>
                            <td align="right">{developer_email}</td>
                        </tr>
                        <tr>
                            <td><i>Created</i></td>
                            <td align="right">2022</td>
                        </tr>
                        <tr>
                            <td><i>Rebuilt</i></td>
                            <td align="right">2025</td>
                        </tr>
                        <tr>
                            <td><i>Version</i></td>
                            <td align="right">{app_version}</td>
                        </tr>
                    </table>
                </td>
                <tr><br></tr>
            </tr>
        
            <tr>
                <td>
                    <table cellpadding="0" cellspacing="0" style="background-color:#ffffff; padding:7px; border-radius:16px; width:100%;">
                        <tr>
                            <td colspan="3" align="center">
                                <u><b>Actions</b></u>
                            </td>
                        </tr>
                        <tr><br></tr>
                        <tr>
                            <td colspan="3" align="center">
                                {perform_email}
                            </td>
                        </tr>
                        <tr><br></tr>
                                                            
                        <!-- ADD -->
                        <tr>
                            <td style='padding-right:7px;  vertical-align:top;'>⤵️</td>
                            <td><i>Title:</i></td>
                            <td><b>Add</b></td>
                        </tr>
                        <tr>
                            <td></td>
                            <td style='width:60px;  vertical-align:top;'><i>Body:</i></td>
                            <td>{body_add}</td>
                        </tr>
                        <tr>
                            <td></td>
                            <td style='width:60px;  vertical-align:top;'><i>Action:</i></td>
                            <td>{action_add}<br><br></td>
                        </tr>

                        <!-- DELETE -->
                        <tr>
                            <td style='padding-right:7px;  vertical-align:top;'>⤴️</td>
                            <td><i>Title:</i></td>
                            <td><b>Delete</b></td>
                        </tr>
                        <tr>
                            <td></td>
                            <td style='width:60px;  vertical-align:top;'><i>Body:</i></td>
                            <td>{body_delete}</td>
                        </tr>
                        <tr>
                            <td></td>
                            <td style='width:60px;  vertical-align:top;'><i>Action:</i></td>
                            <td>{action_delete}<br><br></td>
                            
                        <!-- UPDATE NEW VERSION -->
                        <tr>
                            <td style='padding-right:7px;  vertical-align:top;'>⚙️</td>
                            <td><i>Title:</i></td>
                            <td><b>Update</b></td>
                        </tr>
                        <tr>
                            <td></td>
                            <td style='width:60px;  vertical-align:top;'><i>Body:</i></td>
                            <td>{body_update}<br></td>
                        </tr>
                        <tr>
                            <td></td>
                            <td></td>
                            <td>{body_update_semantic_versioning}</td>
                        </tr>
                        <tr>
                            <td></td>
                            <td style='width:60px;  vertical-align:top;'><i>Action:</i></td>
                            <td>{action_update}<br><br></td>
                        </tr>
                        
                        <!-- PROGRESS -->
                        <tr>
                            <td style='padding-right:7px;  vertical-align:top;'>📝</td>
                            <td><i>Title:</i></td>
                            <td><b>Progress</b></td>
                        </tr>
                        <tr>
                            <td></td>
                            <td style='width:60px;  vertical-align:top;'><i>Action:</i></td>
                            <td>{action_progress}<br><br></td>
                            
                        <!-- LINKS -->
                        <tr>
                            <td style='padding-right:7px;  vertical-align:top;'>📎</td>
                            <td><i>Title:</i></td>
                            <td><b>Links</b></td>
                        </tr>
                        <tr>
                            <td></td>
                            <td style='width:60px;  vertical-align:top;'><i>Action:</i></td>
                            <td>{action_links}<br><br></td>
                            
                        <!-- UPDATE CREDENTIALS -->
                        <tr>
                            <td style='padding-right:7px;  vertical-align:top;'>🔐</td>
                            <td><i>Title:</i></td>
                            <td><b>Credentials</b></td>
                        </tr>
                        <tr>
                            <td></td>
                            <td style='width:60px;  vertical-align:top;'><i>Body:</i></td>
                            <td>{body_credentials}</td>
                        </tr>
                        <tr>
                            <td></td>
                            <td></td>
                            <td>{body_example_username_credential}</td>
                        </tr>
                        <tr>
                            <td></td>
                            <td></td>
                            <td>{body_example_password_credential}</td>
                        </tr>
                        <tr>
                            <td></td>
                            <td style='width:60px;  vertical-align:top;'><i>Action:</i></td>
                            <td>{action_credentials}<br></td>
                        </tr>
                    </table>
                    
                    <tr>
                        <td align='center'><br>{summary_email}</td>
                    </tr>
                    <tr>
                        <td align='center'>{confirmation_email}</td>
                    </tr>
                    <tr><br></tr>
                    {self.built_with_python_and_copyright_message()}
                </td>
            </tr>
        </table>    
        '''
        
        
        
        
        
        
        
        
    def no_internet_title_message(self) -> str:
        return '🌐 Internet Restored'
    
    
    
    def no_internet_body_message(self , occured: str , restored: str):
        return f'''
        <table cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed; width:100%;">
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.time_message()}
                </td>
            </tr>
            <tr>
                <td colspan="2" align="center"><br>A network connectivity issue occurred at</td>
            </tr>
            <tr>
                <td colspan="2" align="center">{occured}</td>
            </tr>
            <tr><br></tr>
            <tr>
                <td align="center" colspan="2"><i>Possible causes:</i></td>
            </tr>
            <tr>
                <td align="center" colspan="2" style='width:24px; padding-left:10px; vertical-align:top;'>● &nbsp;<b>Ethernet cable disconnection.</b></td>
            </tr>
            <tr>
                <td align="center" colspan="2" style='width:24px; padding-left:10px; vertical-align:top;'>● <b>Weak or unstable Wi-Fi signal.</b></td>
            </tr>
            <tr><br></tr>
            <tr>
                <td colspan="2" align="center" style="padding-top:12px;">Connection was restored at<br></td>
            </tr>
            <tr>
                <td colspan="2" align="center">{restored}</td>
            </tr>
            <tr><br></tr>
            <tr>
                <td>{self.built_with_python_and_copyright_message()}</td>
            </tr>
        </table>
        '''
        
        



    def daily_report_title_message(self) -> str:
        return '📊 Daily Report'



    def daily_report_body_message(self ,
                                  total_updates_of_day: int ,
                                  total_issues: int ,
                                  total_machines: int ,
                                  inserted_machines: int ,
                                  removed_machines: int ,
                                  updated_result: str) -> str:
        analytics_link = 'https://www.car.gr/analytics/overview?fbclid=IwAR0PP4jRq9XOQROeGJIRON7gSMOO4RPUDBAEiJXrPPhg44pTBiZNRsS6vz4&date-preset=lastDay'
        analytics_display_name = 'analytics'
        analytics = f'<a href="{analytics_link}">{analytics_display_name}</a>'

        total_updates_message = f'{total_updates_of_day}/{os.getenv('total_required_updates')}'
        total_machines_message = f'{total_machines}'
        total_issues_message = f'{total_issues}'
        inserted_machines_message = f'{inserted_machines}'
        removed_machines_message = f'{removed_machines}'
        view_analytics = f'View today\'s update {analytics}.'
        
        final = f'''
        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td colspan="2" align="center"><u><b><br>Summary</b></u></td>
            </tr>
            <tr>
                <td><b><br>Total updates</b></td>
                <td align="right"><br>{total_updates_message}</td>
            </tr>
            <tr>
                <td><b>Total machines</b></td>
                <td align="right">{total_machines_message}</td>
            </tr>
            <tr>
                <td><b>Total issues</b></td>
                <td align="right">{total_issues_message}</td>
            </tr>
            <tr>
                <td><b>Inserted machines</b></td>
                <td align="right">{inserted_machines_message}</td>
            </tr>
            <tr>
                <td><b>Removed machines</b></td>
                <td align="right">{removed_machines_message}</td>
            </tr>
            <tr><br></tr>
        </table>
            
        {updated_result}

        <table align="center" width="100%" cellpadding="0" cellspacing="0">
            <tr><br></tr>
            <tr>
                <td align="center">{view_analytics}</td>
            </tr>
            <tr><br></tr>
        </table>

        {self.built_with_python_and_copyright_message()}
        '''
        return f'''
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed;">
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.time_message()}
                </td>
            </tr>

            <tr>
                <td align="center">
                    {final}
                </td>
            </tr>
        </table>
        '''






    def new_version_started_title_message(self) -> str:
        return '✅ Application Updated'
    
    
    
    def new_version_started_body_message(self , app_version) -> str:        
        return f'''
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed;">
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.time_message()}
                </td>
            </tr>
            <tr><br></tr>
            <table align="center" width="100%" cellpadding="0" cellspacing="0">
                <tr> 
                    <td align="center">The application has been successfully updated and restarted to version {app_version}</td>
                </tr>
                <tr>
                    <td align="center">The system is now running normally.</td>
                </tr>
                <tr><br></tr>
            </table>
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.built_with_python_and_copyright_message()}
                </td>
            </tr>
        </table>
        '''
        
        
    
    def credentails_update_title_message(self , cond_str: str) -> str:
        return '✅ Credentials Updated' if cond_str.lower() == 'ok' else '❌ Credentials Update Failed'
    
    
    
    def credentials_update_body_message(self , cond_str: str) -> str:
        if(cond_str.lower() == 'ok'):
            msg = 'Your account credentials have been updated successfully. The application logged out, signed back in \
                with new credentials, and is now running normally.'
                
        else:
            msg = cond_str
            
        return f'''
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed;">
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.time_message()}
                </td>
            </tr>
            <table align="center" width="100%" cellpadding="0" cellspacing="0">
                <tr><br></tr>
                <tr>
                    <td align="center">{msg}</td>
                </tr>
                <tr><br></tr>
            </table>
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.built_with_python_and_copyright_message()}
                </td>
            </tr>
        </table>
        '''
        
        
        
        
    def progress_title_message(self) -> str:
        return '📝 Progress Update'
    
    
    
    def progress_body_message(self ,
                              number_of_machines: int ,
                              current_updates: int ,
                              current_errors: int ,
                              most_recent_error: str ,
                              added_machines: int ,
                              removed_machines: int ,
                              captcha_challenges: int ,
                              version: str
                              ) -> str:

        return f'''
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed;">
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.time_message()}
                </td>
            </tr>
            <tr><br></tr>
            {f'''<tr>
                <td width="100%" style="padding:0; margin:0;">
                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#ffffff; padding:15px; border-radius:16px;">
                        <tr>
                            <td><b>Number of machines</b></td>
                            <td align="right">{number_of_machines}</td>
                        </tr>
                        <tr>
                            <td><b>Current updates</b></td>
                            <td align="right">{current_updates}</td>
                        </tr>
                        <tr>
                            <td><b>Current errors</b></td>
                            <td align="right">{current_errors}</td>
                        </tr>
                        <tr>
                            <td><b>Added machines</b></td>
                            <td align="right">{added_machines}</td>
                        </tr>
                        <tr>
                            <td><b>Removed machines</b></td>
                            <td align="right">{removed_machines}</td>
                        </tr>
                        <tr>
                            <td><b>Captcha challenges</b></td>
                            <td align="right">{captcha_challenges}</td>
                        </tr>
                        <tr>
                            <td><b>App version</b></td>
                            <td align="right">{version}</td>
                        </tr> 
                    </table>
                </td>
            ''' if(current_errors == 0) else
            f'''
                <td width="100%" style="padding:0; margin:0;">
                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#ffffff; padding:15px; border-radius:16px;">
                        <tr>
                            <td><b>Number of machines</b></td>
                            <td align="right">{number_of_machines}</td>
                        </tr>
                        <tr>
                            <td><b>Current updates</b></td>
                            <td align="right">{current_updates}</td>
                        </tr>
                        <tr>
                            <td><b>Current errors:</b></td>
                            <td align="right">{current_errors}</td>
                        </tr>
                        <tr>
                            <td><b>Most recent error</b></td>
                            <td align="right">{most_recent_error}</td>
                        </tr>
                        <tr>
                            <td><b>Added machines</b></td>
                            <td align="right">{added_machines}</td>
                        </tr>
                        <tr>
                            <td><b>Removed machines</b></td>
                            <td align="right">{removed_machines}</td>
                        </tr>
                        <tr>
                            <td><b>Captcha challenges</b></td>
                            <td align="right">{captcha_challenges}</td>
                        </tr>
                        <tr>
                            <td><b>App version</b></td>
                            <td align="right">{version}</td>
                        </tr>
                    </table>
                </td>
            '''}
            <tr><br></tr>
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.built_with_python_and_copyright_message()}
                </td>
            </tr>
        </table>
        '''
        

            
            
    
    
    
    
    def empty_body(self):
        return f'''
                <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#ffffff; padding:7px; border-radius:16px; table-layout:fixed;">
                        <tr>
                            <td width="100%" style="padding:0; margin:0;">
                                {self.time_message()}
                            </td>
                        </tr>
                        <tr><br></tr>
                        <tr>
                            <td style="padding:0; margin:0;">
                                <table cellpadding="0" cellspacing="0" style="background-color:#FFD6D6; padding:5px; border-radius:16px;">
                                    <tr>
                                        <td align="center">No content was found in the email message.</td>
                                    </tr>
                                    <tr><br></tr>
                                </table>
                            </td>
                        </tr>
                        <tr><br></tr>
                        <tr>
                            <td width="100%" style="padding:0; margin:0;">
                                {self.built_with_python_and_copyright_message()}
                            </td>
                        </tr>
                    </table>
                    '''

                
                


    def machine_inserted_title_message(self , number_of_inserted_machines: int , invalid_machines: list[str]) -> str:
        if(number_of_inserted_machines == 1):
            if(len(invalid_machines) > 0):
                return '⚠️ Partial Machine Insertion'
            
            return f'⤵️ {number_of_inserted_machines} Machine Added'
        
        if(number_of_inserted_machines > 1):
            if(len(invalid_machines) > 0):
                return '⚠️ Partial Machine Insertion'
            return f'⤵️ {number_of_inserted_machines} Machines Added'
        
        return f'❌ Machine Insertion Failed'





    def machine_inserted_body_message(self , list_of_added_machines: list[str] , invalid_machines: list[str] , number_of_machines: int) -> str:
        s = 's' if len(list_of_added_machines) > 1 else ''
        s_invalid = 's' if len(invalid_machines) > 1 else ''

        machines_inserted = f'''
                            <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed;">
                                <tr>
                                    <td width="100%" style="padding:0; margin:0;">
                                        {self.time_message()}
                                    </td>
                                </tr>
                                <tr><br></tr>
                                <tr>
                                    <td width="100%" style="padding:0; margin:0;">
                                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#E6FFE6; padding:5px; border-radius:16px;">
                                            <tr>
                                                <td colspan="2" align="center">{len(list_of_added_machines)} machine{s} inserted successfully.</td>
                                            </tr>
                                            <tr><br></tr>
                                            {' '.join(f'''
                                                            <tr>
                                                                <td width="24" style="vertical-align: top; padding:7px; text-align:center;">➕</td>
                                                                <td style="vertical-align:top; padding:7px;" align="left">{list_of_added_machines[i]}</td>
                                                            </tr>
                                                            <tr>
                                                                <td></td>
                                                                {'<br>' if i < len(list_of_added_machines)-1  else ''}
                                                            </tr>
                                                        '''
                                                        for i in range(len(list_of_added_machines)))
                                            }
                                        </table>
                                    </td>
                                </tr>
                                
                                {f'''
                                    <tr><br></tr>
                                    <tr>
                                        <td width="100%" style="padding:0; margin:0;">
                                            <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#FFD6D6; padding:5px; border-radius:16px;">
                                                <tr>
                                                    <td colspan="2" align="center">{len(invalid_machines)} machine{s_invalid} could not be added due to duplication or invalid link.</td>
                                                </tr>
                                                <tr><br></tr>
                                                {''.join(f'''
                                                                <tr>
                                                                    <td width="24" style="vertical-align: top; padding:7px; text-align:center;">❌</td>
                                                                    <td style="vertical-align:top; padding:7px;" align="left">{invalid_machines[i]}</td>
                                                                </tr>
                                                                <tr>
                                                                    <td></td>
                                                                    {'<br>' if i < len(invalid_machines)-1  else ''}
                                                                </tr>
                                                            '''
                                                            for i in range(len(invalid_machines)))
                                                }
                                            </table>
                                        </td>
                                    </tr>
                                    '''
                                    if len(invalid_machines) > 0 else ''
                                }
                                <tr><br></tr>
                                <tr>
                                    {f'''
                                        <td align="center">Machines have been updated to {number_of_machines}.</td>''' if (len(list_of_added_machines)) > 0 else ''
                                    }
                                </tr>
                                <tr><br></tr>
                                <tr><br></tr>
                                <tr>
                                    <td width="100%" style="padding:0; margin:0;">
                                        {self.built_with_python_and_copyright_message()}
                                    </td>
                                </tr>
                            </table>
                            '''
                            
                            
        machines_insertion_failed = f'''
                                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#ffffff; padding:7px; border-radius:16px; table-layout:fixed;">
                                            <tr>
                                                <td width="100%" style="padding:0; margin:0;">
                                                    {self.time_message()}
                                                </td>
                                            </tr>
                                            <tr><br></tr>
                                            <tr>
                                                <td style="padding:0; margin:0;">
                                                    <table cellpadding="0" cellspacing="0" style="background-color:#FFD6D6; padding:5px; border-radius:16px;">
                                                        <tr>
                                                            <td colspan="2" align="center">{len(invalid_machines)} machine{s_invalid} could not be added due to duplication or invalid link.</td>
                                                        </tr>
                                                        <tr><br></tr>
                                                        {' '.join(f'''
                                                                        <tr>
                                                                            <td width="24" style="vertical-align: top; padding:7px; text-align:center;">❌</td>
                                                                            <td style="vertical-align:top; padding:7px;" align="left">{invalid_machines[i]}</td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td></td>
                                                                            {'<br>' if i < len(invalid_machines)-1  else ''}
                                                                        </tr>
                                                                    '''
                                                                    for i in range(len(invalid_machines)))
                                                        }
                                                    </table>
                                                </td>
                                            </tr>
                                            <tr><br></tr>
                                            <tr>
                                                <td width="100%" style="padding:0; margin:0;">
                                                    {self.built_with_python_and_copyright_message()}
                                                </td>
                                            </tr>
                                        </table>
                                        '''
                                        
        
        
        if(len(list_of_added_machines) > 0):
            return machines_inserted
        
        if(len(invalid_machines) > 0):
            return machines_insertion_failed

        return self.empty_body()
        
    
    
    
        
        
        
        
        
    def machine_removed_title_message(self , number_of_removed_machines: int , not_existing_machines: list[str]) -> str:
        if(number_of_removed_machines == 1):
            if(len(not_existing_machines) > 0):
                return '⚠️ Partial Machine Removal'
            
            return f'⤴️ {number_of_removed_machines} Machine Removed'
        
        if(number_of_removed_machines > 1):
            if(len(not_existing_machines) > 0):
                return '⚠️ Partial Machine Removal'
            
            return f'⤴️ {number_of_removed_machines} Machines Removed'
        
        return f'❌ Machine Removal Failed'





    def machine_removed_body_message(self , list_of_removed_machines: list[str] , not_existing_machines: list[str] , number_of_machines: int) -> str:
        s_removed = 's' if len(list_of_removed_machines) > 1 else ''
        s_not_existing = 's' if len(not_existing_machines) > 1 else ''
        
        machines_removed = f'''
                            <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed;">
                                <tr>
                                    <td width="100%" style="padding:0; margin:0;">
                                        {self.time_message()}
                                    </td>
                                </tr>
                                <tr><br></tr>
                                <tr>
                                    <td width="100%" style="padding:0; margin:0;">
                                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#E6FFE6; padding:5px; border-radius:16px;">
                                            <tr>
                                                <td colspan="2" align="center">{len(list_of_removed_machines)} machine{s_removed} removed successfully.</td>
                                            </tr>
                                            <tr><br></tr>
                                            {' '.join(f'''
                                                            <tr>
                                                                <td width="24" style="vertical-align: top; padding:7px; text-align:center;">➖</td>
                                                                <td style="vertical-align:top; padding:7px;" align="left">{list_of_removed_machines[i]}</td>
                                                            </tr>
                                                            <tr>
                                                                {'<br>' if i < len(list_of_removed_machines)-1  else ''}
                                                            </tr>
                                                        '''
                                                        for i in range(len(list_of_removed_machines)))
                                            }
                                        </table>
                                    </td>
                                </tr>
                                
                                {f'''
                                    <tr><br></tr>
                                    <tr>
                                        <td width="100%" style="padding:0; margin:0;">
                                            <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#FFD6D6; padding:5px; border-radius:16px;">
                                                <tr>
                                                    <td colspan="2" align="center">{len(not_existing_machines)} machine{s_not_existing} could not be removed due to non-existence or invalid link.</td>
                                                </tr>
                                                <tr><br></tr>
                                                {''.join(f'''
                                                                <tr>
                                                                    <td width="24" style="vertical-align: top; padding:7px; text-align:center;">❌</td>
                                                                    <td style="vertical-align:top; padding:7px;" align="left">{not_existing_machines[i]}</td>
                                                                </tr>
                                                                <tr>
                                                                    <td></td>
                                                                    {'<br>' if i < len(not_existing_machines)-1  else ''}
                                                                </tr>
                                                            '''
                                                            for i in range(len(not_existing_machines)))
                                                }
                                            </table>
                                        </td>
                                    </tr>
                                    '''
                                    if len(not_existing_machines) > 0 else ''
                                }
                                <tr><br></tr>
                                <tr>
                                    {f'''
                                            <td align="center">Machines have been updated to {number_of_machines}.</td>''' if len(list_of_removed_machines) > 0 else ''
                                    }
                                </tr>
                                <tr><br></tr>
                                <tr>
                                    <td width="100%" style="padding:0; margin:0;">
                                        {self.built_with_python_and_copyright_message()}
                                    </td>
                                </tr>
                            </table>
                            '''
                            
                            
        machines_removal_failed = f'''
                                   <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed;">
                                        <tr>
                                            <td width="100%" style="padding:0; margin:0;">
                                                {self.time_message()}
                                            </td>
                                        </tr>
                                        <tr><br></tr>
                                        <tr>
                                            <td width="100%" style="padding:0; margin:0;">
                                                <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#FFD6D6; padding:5px; border-radius:16px;">
                                                    <tr>
                                                        <td colspan="2" align="center">{len(not_existing_machines)} machine{s_not_existing} could not be removed due to non-existence or invalid link.</td>
                                                    </tr>
                                                    <tr><br></tr>
                                                    {' '.join(f'''
                                                                    <tr>
                                                                        <td width="24" style="vertical-align: top; padding:7px; text-align:center;">❌</td>
                                                                        <td style="vertical-align:top; padding:7px;" align="left">{not_existing_machines[i]}</td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td></td>
                                                                        {'<br>' if i < len(not_existing_machines)-1  else ''}
                                                                    </tr>
                                                                '''
                                                                for i in range(len(not_existing_machines)))
                                                    }
                                                </table>
                                            </td>
                                        </tr>
                                        <tr><br></tr>
                                        <tr>
                                            <td width="100%" style="padding:0; margin:0;">
                                                {self.built_with_python_and_copyright_message()}
                                            </td>
                                        </tr>
                                    </table>
                                    '''
        
        if(len(list_of_removed_machines) > 0):
            return machines_removed
        
        if(len(not_existing_machines) > 0):
            return machines_removal_failed

        return self.empty_body()
    
    


        
        
        
        

    def error_installing_new_version_title_message(self) -> str:
        return '❌ New Version Failed To Install'
    
    
    
    def general_error_installing_new_version_body_message(self) -> str:
        error_msg = 'An unexpected error occurred while attempting to install the latest version from GitHub. \
                     TeamViewer has been launched and the system is now available for remote access to allow manual resolution of the issue.'
        
        return f'''
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed;">
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.time_message()}
                </td>
            </tr>
            <tr><br></tr>
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#ffffff; padding:5px; border-radius:16px;">
                        <tr>
                            <td align="center">{error_msg}</td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr><br></tr>
            <tr><br></tr>
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.built_with_python_and_copyright_message()}
                </td>
            </tr>
        </table>
        '''
    
    
    def error_installing_new_version_body_message_missing_type(self) -> str:
        error_msg1 = 'The new version will not be installed due to an invalid or missing version type.'
        error_msg2 = 'Please specify one of the following:'
        error_msg3 = 'major, minor or patch.'

        
        return f'''
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed;">
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.time_message()}
                </td>
            </tr>
            <tr><br></tr>
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#ffffff; padding:5px; border-radius:16px;">
                        <tr>
                            <td align="center">{error_msg1}</td>
                        </tr>
                        <tr>
                            <td align="center">{error_msg2}</td>
                        </tr>
                        <tr>
                            <td align="center">{error_msg3}</td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr><br></tr>
            <tr><br></tr>
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.built_with_python_and_copyright_message()}
                </td>
            </tr>
        </table>
        '''
        
        
    
    
    
    
    
    def see_all_available_links_title_message(self) -> str:
        return '📎 All Available Links'
    
    
    
    
    
    def see_all_available_links_body_message(self , list_of_all_machines: str) -> str:
        return f'''
                <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed;">
                    <tr>
                        <td width="100%" style="padding:0; margin:0;">
                            {self.time_message()}
                        </td>
                    </tr>
                    <tr><br><br></tr>
                    <tr>
                        <td align="center" width="100%" style="padding:0; margin:0;">All available links are listed below.</td>
                    </tr>
                    <tr><br></tr>
                    {list_of_all_machines}
                    <tr><br><br></tr>
                    <tr>
                        <td width="100%" style="padding:0; margin:0;">
                            {self.built_with_python_and_copyright_message()}
                        </td>
                    </tr>
                </table>
                '''
                
                
                
    
    
    
    
    def unable_to_login_title_message(self) -> str:
        return '👤 Login Failed'
    
    

    def unable_to_login_body_message(self) -> str:
        msg = 'Sign-in failed. Authentication was unsuccessful after 3 attempts due to invalid username or password. Please verify your credentials.'
        
        return f'''
        <table cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed; width:100%;">
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.time_message()}
                </td>
            </tr>
            <tr><br></tr>
            <tr>
                <td colspan="2" align="center" style="padding-top:12px;">{msg}</td>
            </tr>
            <tr><br><br></tr>
            <tr>
                <td>{self.built_with_python_and_copyright_message()}</td>
            </tr>
        </table>
        '''
        
        
        
    def captcha_failed_to_solve_title_message(self) -> str:
        return '🚨 Captcha Manual Verification'
    
    
    
    def captcha_failed_to_solve_body_message(self) -> str:
        captcha_attempts = 10
        msg = f'Login failed. A CAPTCHA challenge blocked the process after {captcha_attempts} attempts. Manual verification is required.'        
        
        return f'''
        <table cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed; width:100%;">
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.time_message()}
                </td>
            </tr>
            <tr><br></tr>
            <tr>
                <td colspan="2" align="center" style="padding-top:12px;">{msg}</td>
            </tr>
            <tr><br><br></tr>
            <tr>
                <td>{self.built_with_python_and_copyright_message()}</td>
            </tr>
        </table>
        '''
        
        
        
        
    def notify_every_10_errors_title_message(self) -> str:
        return '⚠️ Error Status Update'
        
    
    
    def notify_every_10_errors_body_message(self , errors: int) -> str:
        msg = f'The system has reached {errors} errors. An email with the title \'TeamViewer\' may be sent to enable \
                TeamViewer access for further review.'

        return f'''
        <table cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed; width:100%;">
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.time_message()}
                </td>
            </tr>
            <tr><br></tr>
            <tr>
                <td colspan="2" align="center" style="padding-top:12px;">{msg}</td>
            </tr>
            <tr><br><br></tr>
            <tr>
                <td>{self.built_with_python_and_copyright_message()}</td>
            </tr>
        </table>
        '''
        
        
        
        
    def connect_via_teamviewer_title_message(self) -> str:
        return '🖥️ Connect Via TeamViewer'
    
    
    

    def connect_via_teamviewer_body_message(self) -> str:
        msg = 'TeamViewer has been launched and the system is now available for remote access.'
        
        return f'''
        <table cellpadding="0" cellspacing="0" style="background-color:#f1f1f1; padding:7px; border-radius:16px; table-layout:fixed; width:100%;">
            <tr>
                <td width="100%" style="padding:0; margin:0;">
                    {self.time_message()}
                </td>
            </tr>
            <tr><br></tr>
            <tr>
                <td colspan="2" align="center" style="padding-top:12px;">{msg}</td>
            </tr>
            <tr><br><br></tr>
            <tr>
                <td>{self.built_with_python_and_copyright_message()}</td>
            </tr>
        </table>
        '''