Extending Salt's capabilities for event-driven network automation and orchestration: NANOG 76 tutorial
======================================================================================================

This repository contains the Pillars and the extension modules used during the 
live demo for the `NANOG 76 tutorial 
<https://pc.nanog.org/static/published/meetings//NANOG76/daily/day_3.html#talk_1982>`__.

The slides are available at:
https://pc.nanog.org/static/published/meetings/NANOG76/1982/20190612_Ulinic_Extending_Salt_S_Capabilities_v1.pdf

During the live demo I have provided access to several 
https://www.digitalocean.com/ `Droplets 
<https://www.digitalocean.com/products/droplets/>`__, from where we can manage 
Juniper and Arista VMs, courtesy of https://www.tesuto.com/.

As the resources are limited, the users are also able to follow the steps 
together with me, by starting up the Salt processes using Docker, see the 
:ref:`docker` section below. Similarly, this could be useful for anyone that 
would like to repeat the demo offline.

Using DigitalOcean Droplets
---------------------------

There are 10 droplets you can use, ``srv1.automatethe.net``, 
``srv2.automatethe.net`` ... ``srv10.automatethe.net``. The credentials will be 
provided during the live session. 

.. code-block:: bash

  mircea@master-roshi ~
  > ssh salt@srv1.automatethe.net
  Linux srv1 4.9.0-9-amd64 #1 SMP Debian 4.9.168-1+deb9u2 (2019-05-13) x86_64

  The programs included with the Debian GNU/Linux system are free software;
  the exact distribution terms for each program are described in the
  individual files in /usr/share/doc/*/copyright.

  Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
  permitted by applicable law.
  Last login: Fri Jun  7 08:15:25 2019 from 89.34.165.210
  salt@srv1:~$

On each Droplet there's a Salt Master running, and two Proxy Minions, named 
``eos<ID>`` and ``junos<ID>``, e.g., ``eos1`` and ``junos1`` on 
``srv1.automatethe.net`` - ready to be used. Example:

.. code-block:: bash

  salt@srv1:~$ sudo salt \* test.ping
  junos1:
      True
  eos1:
      True

The Master config file used in this case is the one from this repository -
https://github.com/mirceaulinic/nanog76-tutorial/blob/master/master:

.. code-block:: yaml

  open_mode: true

  pillar_roots:
    base:
      - /srv/salt/pillar

  file_roots:
    base:
      - /srv/salt
      - /srv/salt/extmods

For simplicity, the ``/srv/salt`` directory is a symlink to 
``/home/salt/nanog76-tutorial`` which is the place where this repository has 
been cloned:

.. code-block:: bash

  salt@srv1:~$ ls -la /srv/salt
  lrwxrwxrwx 1 root root 27 Jun  6 09:56 /srv/salt -> /home/salt/nanog76-tutorial
  salt@srv1:~$

Therefore, the Master is going to load the Pillar data from the ``pillar`` 
directory in this repository, and the extension modules from the ``extmods`` 
directory in this repository, respectively.

Using Docker
------------

When using Docker, please see the Docker installation instructions: 
https://docs.docker.com/install/, as well as Docker Compose:
https://docs.docker.com/compose/install/.

Clone this repository and move into the ``nanog76-tutorial`` directory:

.. code-block:: bash

    $ git clone https://github.com/mirceaulinic/nanog76-tutorial.git
    $ cd nanaog76-tutorial/

Edit the ``pillar/junos_pillar.sls`` and / or ``pillar/arista_pillar.sls`` with 
the connection credentials to a virtual machine or real device.

To verify that the credentials are correct and it is possible to connect to the
device, you can use the NAPALM CLI tool, e.g.,

.. code-block:: bash

    $ docker run --rm -ti mirceaulinic/salt-proxy:2019.2.0 \
        napalm --vendor junos \
               --user salt \
               --password password \
               junos.nanog76-demo.digitalocean.cloud.tesuto.com \
               call get_facts

During the live session, it is possible to use the following hostnames to 
connect to a Tesuto-provided Juniper or Arista VM, 
``junos<ID>.nanog76-demo.digitalocean.cloud.tesuto.com``, or 
``eos<ID>.nanog76-demo.digitalocean.cloud.tesuto.com``, e.g., 
``junos5.nano76-demo.digitalocean.cloud.tesuto.com``. Otherwise, you should be 
able to use any VM or real device you might have available.

To start the environment for Junos, you can execute:

.. code-block:: bash

    $ make up PROXYID=juniper-router
    docker-compose up -d
    Creating salt-proxy-juniper-router ... done
    Creating salt-master               ... done

Or for Arista:

.. code-block:: bash

    $ make up PROXYID=arista-switch
    docker-compose up -d
    Creating salt-master              ... done
    Creating salt-proxy-arista-switch ... done

Jump into the ``salt-master`` container from where we'll be running command 
from now on:

.. code-block:: bash
    $ docker exec -it salt-master bash

    root@salt-master:/# salt-key -L
    Accepted Keys:
    arista-switch
    Denied Keys:
    Unaccepted Keys:
    Rejected Keys:


    root@salt-master:/# salt arista-switch example.version
    arista-switch:
        4.21.1F
