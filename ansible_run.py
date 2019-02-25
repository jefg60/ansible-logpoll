"""Functions to run ansible playbooks."""
import os
import subprocess
from multiprocessing import Pool

import anmad_args
import anmad_logging

def run_one_playbook(my_playbook):
    """Run exactly one ansible playbook."""
    my_playbook = os.path.abspath(my_playbook)
    anmad_logging.LOGGER.info(
        "Attempting to run ansible-playbook --inventory %s %s",
        anmad_args.MAININVENTORY, my_playbook)
    ret = subprocess.call(
        [anmad_args.ANSIBLE_PLAYBOOK_CMD,
         '--inventory', anmad_args.MAININVENTORY,
         '--vault-password-file', anmad_args.ARGS.vault_password_file,
         my_playbook])

    if ret == 0:
        anmad_logging.LOGGER.info(
            "ansible-playbook %s return code: %s",
            my_playbook, ret)
        return ret

    anmad_logging.LOGGER.error(
        "ansible-playbook %s return code: %s",
        my_playbook, ret)
    return ret


def runplaybooks(listofplaybooks):
    """Run a list of ansible playbooks."""
    pool = Pool(anmad_args.ARGS.concurrency)
    pool.map(run_one_playbook, listofplaybooks)

def runplaybooks_async(listofplaybooks):
    """Run a list of ansible playbooks asyncronously."""
    pool = Pool(anmad_args.ARGS.concurrency)
    pool.map_async(run_one_playbook, listofplaybooks)
