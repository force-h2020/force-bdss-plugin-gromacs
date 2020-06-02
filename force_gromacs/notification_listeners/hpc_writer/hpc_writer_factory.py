#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from force_bdss.api import BaseNotificationListenerFactory

from .hpc_writer import HPCWriter
from .hpc_writer_model import HPCWriterModel


class HPCWriterFactory(BaseNotificationListenerFactory):
    def get_identifier(self):
        return "hpc_writer"

    def get_name(self):
        return "HPC Writer"

    def get_model_class(self):
        return HPCWriterModel

    def get_listener_class(self):
        return HPCWriter
