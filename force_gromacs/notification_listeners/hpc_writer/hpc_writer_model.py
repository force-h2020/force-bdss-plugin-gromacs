from traits.api import Unicode, Bool, Code
from traitsui.api import View, Item

from force_bdss.api import BaseNotificationListenerModel


class HPCWriterModel(BaseNotificationListenerModel):

    header = Code()

    path = Unicode("hpc_sub_script")

    dry_run = Bool(True)

    traits_view = View(
        Item('header'),
        Item("path"),
        Item("dry_run")
    )
