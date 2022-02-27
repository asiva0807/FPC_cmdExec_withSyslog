#!/usr/lib/python
 
# Event option configuration
#set event-options policy TEST events CHASSISD_SNMP_TRAP7
#set event-options policy TEST attributes-match chassisd_snmp_trap7.value5 matches "^.*MPC10E.*$"
#set event-options policy TEST then event-script demo.py
#set event-options event-script file demo.py python-script-user labroot
#set system scripts language python
 
import jcs
from junos import Junos_Trigger_Event
from jnpr.junos import Device
import os
import time
 
# Get the slot value from the message
def get_slot_value():
    message = Junos_Trigger_Event.xpath('//trigger-event/message')[0].text
    slotvalue = message.split(" ")
    slotvalue = str(slotvalue[-1].replace(")",""))
    return slotvalue
 
# Execute all the cli command
def main():
    pfe_command = '''request pfe execute command "test fabric self_ping blackhole action disable" target fpc{0}.0'''.\
        format(get_slot_value())
    with Device() as dev:
        time.sleep(10)
        jcs.trace("Running script to disable fabric selfping blackhole action")
        jcs.trace(dev.cli(pfe_command, warning=False))
        jcs.trace(dev.cli("show chassis fpc detail", warning=False))
        jcs.trace(dev.cli("show chassis fpc errors", warning=False))
 
if __name__ == '__main__':              
    main()
