"""Initialize arguments for anmad."""
import shutil
import os
from os.path import expanduser
import configargparse

DEFAULT_CONFIGFILE = '/etc/ansible-logpoll/conf.d/*.conf'

def parse_args():
    """Read arguments from command line."""

    __version__ = "0.9.4"

    home = expanduser("~")

    try:
        ansible_home = os.path.dirname(
            os.path.dirname(shutil.which("ansible-playbook"))
        )
    except TypeError:
        ansible_home = os.getcwd()

    parser = configargparse.ArgParser(
        default_config_files=[
            DEFAULT_CONFIGFILE,
            '~/.ansible-logpoll.conf'
            ]
        )
    parser.add_argument(
        "-v",
        "-V",
        "--version",
        action="version",
        version=__version__
        )
    parser.add_argument(
        "-c",
        "--configfile",
        is_config_file=True,
        help="override default config file (/etc/ansible-logpoll/conf.d/*.conf)"
        )
    parser.add_argument(
        "--venv",
        help="python virtualenv to run ansible from",
        default=ansible_home
        )
    parser.add_argument(
        "--interval",
        type=int,
        help="interval in seconds at which to check for new code",
        default=15
        )
    parser.add_argument(
        "--ssh_id",
        help="ssh id file to use, default ~/.ssh/id_rsa",
        default=home + "/.ssh/id_rsa"
        )
    parser.add_argument(
        "--dir_to_watch",
        help="dir to watch",
        required=True
        )
    parser.add_argument(
        "--vault_password_file",
        help="vault password file, default ~/.vaultpw",
        default=home + "/.vaultpw"
        )
    parser.add_argument(
        "--syntax_check_dir",
        help="Optional directory to search for *.yml and *.yaml files to "
             "syntax check when changes are detected"
        )
    parser.add_argument(
        "--playbooks",
        "-p",
        nargs='*',
        required=True,
        help="space separated list of ansible playbooks to run. "
        )
    parser.add_argument(
        "--pre_run_playbooks",
        nargs='*',
        help="space separated list of ansible playbooks to run "
             "before doing any syntax checking. Useful "
             "for playbooks that fetch roles required by other playbooks"
        )
    parser.add_argument(
        "--inventories",
        "-i",
        nargs='*',
        required=True,
        help="space separated list of ansible inventories to syntax check "
             "against. The first inventory file "
             "will be the one that playbooks are run against if syntax "
             "checks pass"
        )
    parser.add_argument(
        "--ssh_askpass",
        help="location of a script to pass as SSH_ASKPASS env var,"
             "which will enable this program to load an ssh key if "
             "it has a passphrase. Only works if not running in a terminal"
        )
    parser.add_argument(
        "--no-syslog",
        dest="syslog",
        action="store_false",
        help="disable logging to syslog"
        )
    parser.add_argument(
        "--syslogdevice",
        help="syslog device to use",
        default="/dev/log"
        )
    parser.add_argument(
        "--dry-run",
        dest="dryrun",
        action="store_true",
        help="only wait for one --interval, for testing"
        )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        help="print debugging info to logs"
        )
    parser.add_argument(
        "--concurrency",
        help="number of simultaneous processes to run,"
             "defaults to number of cpu reported by OS",
        default=os.cpu_count()
        )
    parser.add_argument(
        "--ara_url",
        help="ARA URL to display after starting jobs",
        default='http://ara/'
        )

    parser.set_defaults(debug=False, syslog=True, dryrun=False)
    myargs = parser.parse_args()
    return myargs

ARGS = parse_args()

# filter list args to remove empty strings that may have been passed from
# the config file
ARGS.inventories = list(filter(None, ARGS.inventories))
ARGS.playbooks = list(filter(None, ARGS.playbooks))
if ARGS.pre_run_playbooks:
    ARGS.pre_run_playbooks = list(filter(None, ARGS.pre_run_playbooks))

# First inventory is the one that plays run against
MAININVENTORY = os.path.abspath(ARGS.inventories[0])

ANSIBLE_PLAYBOOK_CMD = ARGS.venv + '/bin/ansible-playbook'