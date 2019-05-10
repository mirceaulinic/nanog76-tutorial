def __virtual__():
    if __grains__['os'] == 'eos':
        return 'platform'
    else:
        return (False, 'Not loading this module, as this is not an Arista switch')


def version():
    ret = __salt__['napalm.pyeapi_run_commands']('show version')
    return ret[0]['version']
