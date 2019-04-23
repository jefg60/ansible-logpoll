#!/usr/bin/env python3
"""Daemon to watch redis queues for ansible jobs."""
import os
import sys

import anmad_logging
import anmad_syntaxchecks
import anmad_ssh
import ansible_run

QUEUES = anmad_logging.QUEUES
ARGS = anmad_logging.ARGS
VERSION = anmad_logging.VERSION
DEFAULT_CONFIGFILE = anmad_logging.DEFAULT_CONFIGFILE
ANSIBLE_PLAYBOOK_CMD = anmad_logging.ANSIBLE_PLAYBOOK_CMD
MAININVENTORY = anmad_logging.MAININVENTORY
PRERUN_LIST = anmad_logging.PRERUN_LIST
RUN_LIST = anmad_logging.RUN_LIST

anmad_ssh.add_ssh_key_to_agent(ARGS.ssh_id)

for playbookjob in QUEUES.queue.consume():
    anmad_logging.LOGGER.info("Starting to consume playbooks queue...")
    if playbookjob is not None:
        anmad_logging.LOGGER.info("Found playbook queue job: %s", str(playbookjob))

        # when an item is found in the PLAYQ, first process all jobs in preQ!
        anmad_logging.LOGGER.info("Starting to consume prerun queue...")
        while True:
            # get first item in preQ and check if its a list of 1 item,
            # if so run it
            preQ_job = QUEUES.prequeue.get()
            if isinstance(preQ_job, list) and len(preQ_job) == 1:
                anmad_logging.LOGGER.info(
                    " Found a pre-run queue item: %s", str(preQ_job))
                # statements to process pre-Q job
                ansible_run.runplaybooks(preQ_job)

            # if it wasnt a list, but something is there, something is wrong
            elif preQ_job is not None:
                anmad_logging.LOGGER.warning(
                    "item found in pre-run queue but its not a single item list")
                break
            else:
                anmad_logging.LOGGER.info(
                    "processed all items in pre-run queue")
                break #stop processing pre-Q if its empty

        if playbookjob[0] == 'restart_anmad_run':
            anmad_logging.LOGGER.info(
                'Restarting %s %s %s %s',
                str(sys.executable),
                str(sys.executable),
                str(__file__),
                " ".join(sys.argv[1:])
                )
            os.execl(sys.executable, sys.executable, __file__, *sys.argv[1:])

        anmad_logging.LOGGER.info('Running job from playqueue: %s', str(playbookjob))
        #Syntax check playbooks, or all playbooks in syntax_check_dir
        if ARGS.syntax_check_dir is None:
            problemlist = anmad_syntaxchecks.checkplaybooks(playbookjob)
        else:
            problemlist = anmad_syntaxchecks.syntax_check_dir(
                ARGS.syntax_check_dir)

        if  ''.join(problemlist):
            anmad_logging.LOGGER.warning(
                "Playbooks/inventories that failed syntax check: "
                "%s", " \n".join(problemlist))
            anmad_logging.LOGGER.warning(
                "Refusing to queue requested playbooks until "
                "syntax checks pass")
            continue

        # if we get to here syntax checks passed. Run the job
        anmad_logging.LOGGER.info(
            "Running playbooks %s", str(playbookjob))
        ansible_run.runplaybooks(playbookjob)
        anmad_logging.LOGGER.info(
            "Continuing to process items in playbooks queue...")

anmad_logging.LOGGER.warning("Stopped processing playbooks queue!")
