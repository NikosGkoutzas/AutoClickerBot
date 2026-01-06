from .chrome_boot_interface import ChromeBootInterface
from ..paths.paths import chrome_path , user_data_dir , port
import subprocess




class ChromeBoot(ChromeBootInterface):
    def boot(self) -> None:
        subprocess.Popen(
                            [
                                chrome_path,
                                '--window-size=1920,1080',
                                '--window-position=0,0',
                                f'--remote-debugging-port={port}',
                                f'--user-data-dir={user_data_dir}'
                            ] ,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )