# saltstack_tmate
This is a simple tmate execution module for saltstack that can be used for installing tmate and opening a tmate session.

This can be useful for controlling minions behind a firewall. You can now run tmate.new_session against a target and it will return the session name so that you can ssh into it.


```
root@saltmaster:~# salt saltminion tmate.new_session
saltminion:
    ssh YNCKohVaD2Ccx4vV2Yemt9Sge@ny2.tmate.io
```


# installation

Place this file into your execution modules into your execution modules directory (default: /srv/salt/_modules).

Sync the module to your minions:

```
salt '*' saltutil.sync_modules
```
