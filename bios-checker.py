"""Show system details such as BIOS version, CPU version and kernel version."""

from subprocess import check_output
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk  # nopep8 # noqa: E402 # pylint: disable=C0413

# Set locale to US English so output matches the expected strings.
env = {"LC_ALL": "en_US.utf8"}


def run_with_pkexec(cmd: str) -> bytes:
    """Run a command with pkexec.

    :param cmd: The command to run.
    :return: The output of the command.
    """
    return check_output(['pkexec', 'sh', '-c', cmd], env=env)


# Run the commands and store their output in variables.
bios_info = run_with_pkexec("dmidecode | grep -A3 'Vendor:'")
cpu_info = check_output("lshw -C cpu | grep -A3 'product:'", shell=True,
                        env=env)
kernel_version = check_output("uname -r", shell=True, env=env)

# Create a GTK dialog window with larger text and a bigger size.
dialog = Gtk.MessageDialog(parent=None, flags=0,
                           message_type=Gtk.MessageType.INFO,
                           buttons=Gtk.ButtonsType.OK,
                           text="Framework System Details")
markup = f"""<span size='xx-large' weight='bold'>BIOS Information:</span>
{bios_info.decode()}
<span size='xx-large' weight='bold'>CPU Information:</span>
{cpu_info.decode()}
<span size='xx-large' weight='bold'>Kernel Version:</span>
       {kernel_version.decode()}"""
print(markup)
dialog.set_markup(markup)
dialog.format_secondary_markup(None)
dialog.set_size_request(600, 400)
dialog.run()
dialog.destroy()
