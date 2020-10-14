#!/bin/bash
if [ ! -d ~/venv ] ; then
    virtualenv -p python3 ~/venv &&\
    ~/venv/bin/pip install configargparse hotqueue redis ssh_agent_setup pyyaml flask ansible pylint psutil requests git+https://github.com/jefg60/ansible-vault.git
    git clone https://github.com/bats-core/bats-core.git
    cd bats-core
    sudo ./install.sh /usr/local
    ln -s /vagrant/test/configtest.nodry.ini /home/vagrant/.anmad.conf
fi

~/venv/bin/pip install -e /vagrant
/usr/bin/screen -dmS anmaddev /home/vagrant/venv/bin/python -m anmad.interface
/vagrant/dummy-ansible-playbook.sh &&\
/home/vagrant/venv/bin/pylint /vagrant/*.py &&\
/home/vagrant/venv/bin/pylint /vagrant/anmad &&\
export PYTHONPATH=/vagrant
/home/vagrant/venv/bin/python -m unittest discover -s /vagrant &&\
bats /vagrant/test/anmad.bats &&\
/home/vagrant/venv/bin/python /vagrant/test_requests.py 
