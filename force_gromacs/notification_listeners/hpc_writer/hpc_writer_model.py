#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Unicode, Bool, Code

from force_bdss.api import BaseNotificationListenerModel


class HPCWriterModel(BaseNotificationListenerModel):

    #: Header to include in all HPC submission scripts
    header = Code(desc="Header to include in all HPC submission scripts")

    #: Prefix to include at beginning of all HPC submission files
    prefix = Unicode(
        "hpc_sub_script",
        desc="Prefix to include at beginning of all HPC submission files")

    #: Whether or not to perform a dry run - i.e, generate but do not
    #: write bash files
    dry_run = Bool(True)
