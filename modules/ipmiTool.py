
POWER_CYCLE = "ipmitool power cycle"


def power_cycle(host_obj):
    host_obj.run_cmd(POWER_CYCLE)
