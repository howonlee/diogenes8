import os
import getpass
import os.path
from .settings import Settings
from typing import Optional

class DioDir(object):
    """
    Object corresponding to diogenes directory
    Note the default
    Also note that it created dir if not exists
    """
    def __init__(self, dirname: str=None) -> None:
        if not dirname:
            self.dirname = os.path.expanduser("~/.diogenes")
        else:
            self.dirname = str(dirname)
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)

    def get_settings_filename(self) -> str:
        filename = "{}_settings.json".format(getpass.getuser())
        return os.path.join(self.dirname, filename)

    def append_to_gitignore(self, to_append: str) -> None:
        """
        If you use git to deal with this, as I do,
        you shouldn't check in settings.json, it has an app pwd
        """
        with open(os.path.join(self.dirname, ".gitignore"), "r") as gitignore_file:
            for line in gitignore_file:
                # it's in the file already
                if to_append in line:
                    return
        with open(os.path.join(self.dirname, ".gitignore"), "a+") as gitignore_file:
            gitignore_file.write("{}\n".format(to_append))

    def get_settings(self) -> Optional[Settings]:
        settings_filename = self.get_settings_filename()
        if os.path.isfile(settings_filename):
            return Settings.from_file(settings_filename)
        else:
            return None

    def get_settings_interactive(self) -> Settings:
        """
        try to get settings.
        if fail, then interactively set them and get them
        """
        res = self.get_settings()
        if res is None:
            return self.set_settings_interactive()
        else:
            return res

    def set_settings(self, new_settings: Settings) -> Settings:
        settings_filename = self.get_settings_filename()
        new_settings.to_file(settings_filename)
        self.append_to_gitignore(settings_filename)
        return new_settings

    def set_settings_interactive(self) -> Settings:
        settings_filename = self.get_settings_filename()
        smtp_username = input("SMTP username (your webmail username, usually) > ")
        smtp_password = input("SMTP app password (for gmail, see https://support.google.com/accounts/answer/185833) > ")
        smtp_dest_email = input("Destination email. Can be same or different from SMTP username. > ")
        smtp_url = input("SMTP url [smtp.gmail.com] > ") or "smtp.gmail.com"
        smtp_port = input("SMTP port [587] > ") or 587
        new_settings = Settings(smtp_username=smtp_username,
                                smtp_password=smtp_password,
                                smtp_dest_email=smtp_dest_email,
                                smtp_url=smtp_url,
                                smtp_port=int(smtp_port))
        new_settings.to_file(settings_filename)
        self.append_to_gitignore(settings_filename)
        return new_settings
