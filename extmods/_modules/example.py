def first():
    return True


def second():
    return __salt__['test.ping']()


def third():
    return __salt__['example.first']()


def junos_version():
    ret = __salt__['napalm.junos_cli']('show version', format='xml')
    return ret['message']['software-information']['junos-version']


def os_grains():
    return __grains__['os']


def version():
    if __grains__['os'] == 'junos':
        ret = __salt__['napalm.junos_cli']('show version', format='xml')
        return ret['message']['software-information']['junos-version']
    elif __grains__['os'] == 'eos':
        ret = __salt__['napalm.pyeapi_run_commands']('show version')
        return ret[0]['version']
    elif __grains__['os'] == 'nxos':
        ret = __salt__['napalm.nxos_api_rpc']('show version')
        return ret[0]['result']['body']['sys_ver_str']
    raise Exception('Not supported on this platform')
