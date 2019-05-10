def __virtual__():
    if __grains__['os'] == 'junos':
        return 'platform'
    else:
        return (False, 'Not loading this module, as this is not a Junos device')


def version():    
    ret = __salt__['napalm.junos_cli']('show version', format='xml')
    return ret['message']['software-information']['junos-version']
