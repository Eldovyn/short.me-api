from .account_active_sent import *
from .account_activation import *
from .reset_password_sent import *
from .reset_password_changed import *


def register_socket_io(socket_io):
    register_account_active_sent_socketio_events(socket_io)
    register_account_activation_socketio_events(socket_io)
    register_reset_password_sent_socketio_events(socket_io)
    register_reset_password_changed_socketio_events(socket_io)
