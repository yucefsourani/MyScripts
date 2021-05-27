import gi
gi.require_version('ZBar', '1.0')
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, GdkPixbuf, ZBar
                
class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        
        main_vbox = Gtk.VBox()
        self.add(main_vbox)
        
        label = Gtk.Label()
        main_vbox.pack_start(label,False,False,0)
        
        button = Gtk.Button()
        button.props.label = "Read Barcode"
        main_vbox.pack_start(button,False,False,0)
        
        
        self.video_device = "/dev/video0"
        zbarw = ZBar.Gtk()
        main_vbox.pack_start(zbarw,False,False,0)
        
        zbarw.request_video_size(600,400)

        zbarw.connect("decoded",self.on_decodedd,button,label)
        button.connect("clicked",self.on_button_clicked,zbarw,label)
        
    def on_button_clicked(self,button,zbarw,label):
        label.props.label = ""
        if zbarw.get_video_device() == self.video_device:
            zbarw.set_video_device("")
            zbarw.set_video_enabled(False)
            button.props.label = "Start Read Barcode"
        else:
            zbarw.set_video_device(self.video_device)
            zbarw.set_video_enabled(True)
            button.props.label = "Stop Read Barcode"

        
    def on_decodedd(self,zbarw,type_,data,button,label):
        print(type_)
        print(data)
        zbarw.set_video_device("")
        zbarw.set_video_enabled(False)
        button.props.label = "Start Read Barcode"
        label.props.label  = str(type_) + " : " + str(data)

        
        
        
mw = MainWindow()
mw.connect("delete-event",Gtk.main_quit)
mw.show_all()
Gtk.main()
