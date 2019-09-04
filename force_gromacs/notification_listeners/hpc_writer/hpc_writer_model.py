from traits.api import Unicode, Bool, Code
from traitsui.api import View, Item

from force_bdss.api import BaseNotificationListenerModel


class HPCWriterModel(BaseNotificationListenerModel):

    prefix = Unicode("hpc_sub_script")

    header = Code()

    dry_run = Bool(True)

    traits_view = View(
        Item('header'),
        Item("prefix"),
        Item("dry_run")
    )
