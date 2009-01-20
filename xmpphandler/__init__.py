# -*- codign: utf-8 -*-

__authors__ = "Peter Vizi"
__license__ = "GPLv3"
__version__ = "0.1"
__docformat__ = "restructuredtext en"

import logging
import xmpp

class XMPPHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET, fromjid=None, pwd=None, tojid=None, subject=logging.Formatter("%(name)s %(levelname)s")):
        if not fromjid or not pwd:
            raise AttributeError('JID and password is needed')

        self._fromjid = xmpp.protocol.JID(fromjid)
        self._pwd = pwd
        if tojid:
            self._tojid = xmpp.protocol.JID(tojid)
        else:
            self._tojid = xmpp.protocol.JID(fromjid)
        self._subject = subject
        self._client = xmpp.Client(self._fromjid.getDomain(), debug=[])
        logging.Handler.__init__(self, level)

    def emit(self, record):
        message = self.format(record)
        subject = self._subject.format(record)
        self._fromjid.setResource(record.name)
        if not self._client.isConnected():
            if not self._client.connect():
                raise Exception('Could not connect to XMPP server')
            if not self._client.auth(self._fromjid.getNode(), self._pwd, self._fromjid.getResource()):
                raise Exception('Could not authenticate XMPP user %s %s' % (self._fromjid, self._pwd))
        
        if not self._client.send(xmpp.protocol.Message(self._tojid, body=message, subject=subject)):
            raise Exception('Could not send message to XMPP server')
