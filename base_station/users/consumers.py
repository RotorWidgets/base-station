"""User specific websocket channel consumer shared only with that logged in user"""

from channels import Group
from channels.decorators import channel_session, linearize
from channels.auth import http_session_user, channel_session_user, transfer_user


# Connected to websocket.connect
@linearize
@channel_session
@http_session_user
def ws_add(message):
    # Copy user from HTTP to channel session
    transfer_user(message.http_session, message.channel_session)
    # Add them to the right group
    Group("user-{}".format(message.user.username)).add(message.reply_channel)


# Connected to websocket.keepalive
# We don't linearize as we know this will happen a decent time after add
@channel_session_user
def ws_keepalive(message):
    # Keep them in the right group
    Group("user-{}".format(message.user.username)).add(message.reply_channel)


# Connected to websocket.receive
@linearize
@channel_session_user
def ws_message(message):
    Group("user-{}".format(message.user.username)).send(message.content)


# Connected to websocket.disconnect
# We don't linearize as even if this gets an empty session, the group
# will auto-discard after the expiry anyway.
@channel_session_user
def ws_disconnect(message):
    Group("user-{}".format(message.user.username)).discard(message.reply_channel)
