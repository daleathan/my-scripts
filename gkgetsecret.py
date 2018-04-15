#!/usr/bin/python
#A quick 'n dirty way of retrieving a password from GNOME Keyring
#using libsecret. We identify the password from its description

from gi import require_version
require_version('Secret', '1')
from gi.repository import Secret

def get_password(pw_desc) :
    # Get service
    service = Secret.Service.get_sync(Secret.ServiceFlags.LOAD_COLLECTIONS)

    # Get default keyring
    keyring = Secret.Collection.for_alias_sync(service, "default", \
          Secret.CollectionFlags.NONE, None)

    # Get keyring items
    items = keyring.get_items()

    # Load secrets
    Secret.Item.load_secrets_sync(items)

    # Loop through items, find the matching one and return its password
    password = None
    for item in items :
        if item.get_label() == pw_desc :
            password = item.get_secret().get_text()
            break

    # Close connection
    service.disconnect()

    return password
