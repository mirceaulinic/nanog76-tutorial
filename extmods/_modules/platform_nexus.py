def __virtual__():
    if __grains__['os'] == 'nxos':
        return 'platform'
    else:
        return (False, 'Not loading this module, as this is not Cisco Nexus switch')


def version():
    ret = __salt__['napalm.nxos_api_rpc']('show version')
    return ret[0]['result']['body']['sys_ver_str']
