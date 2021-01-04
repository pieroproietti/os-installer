from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/disk_row.ui')
class DiskRow(Gtk.ListBoxRow):
    __gtype_name__ = 'DiskRow'

    device_path = Gtk.Template.Child()
    name = Gtk.Template.Child()
    size = Gtk.Template.Child()

    def __init__(self, name, size, device_path, additional_info=None, **kwargs):
        super().__init__(**kwargs)

        self.device_path.set_label(device_path)
        self.name.set_label(name)
        self.size.set_label(size)

        self.info = additional_info

    def get_device_path(self):
        return self.device_path.get_label()

    def get_info(self):
        return self.info

    def get_disk_name(self):
        return self.name.get_label()

    def get_disk_size(self):
        return self.size.get_label()


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/label_row.ui')
class LabelRow(Gtk.ListBoxRow):
    __gtype_name__ = 'LabelRow'

    label = Gtk.Template.Child()
    arrow = Gtk.Template.Child()

    def __init__(self, label, additional_info, show_navigation_arrow=False, **kwargs):
        super().__init__(**kwargs)

        self.label.set_label(label)

        self.arrow.set_visible(show_navigation_arrow)

        self.info = additional_info

    def get_info(self):
        return self.info

    def get_label(self):
        return self.label.get_label()


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/widgets/partition_row.ui')
class PartitionRow(Gtk.ListBoxRow):
    __gtype_name__ = 'PartitionRow'

    size = Gtk.Template.Child()
    name = Gtk.Template.Child()

    def __init__(self, name, size, additional_info=None, **kwargs):
        super().__init__(**kwargs)

        self.name.set_label(name)
        self.size.set_label(size)

        self.info = additional_info

    def get_info(self):
        return self.info

    def get_partition_name(self):
        return self.name.get_label()

    def get_partition_size(self):
        return self.size.get_label()
