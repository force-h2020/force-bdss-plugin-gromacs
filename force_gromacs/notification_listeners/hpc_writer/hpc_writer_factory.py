from force_bdss.api import BaseNotificationListenerFactory

from .hpc_writer_notification_listener import (
    HPCWriterNotificationListener
)
from .hpc_writer_model import HPCWriterModel


class HPCWriterFactory(BaseNotificationListenerFactory):
    def get_identifier(self):
        return "hpc_writer"

    def get_name(self):
        return "HPC Writer"

    def get_model_class(self):
        return HPCWriterModel

    def get_listener_class(self):
        return HPCWriterNotificationListener
