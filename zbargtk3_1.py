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
        
        
        zbarw = ZBar.Gtk()
        zbarw.request_video_size(600,400)
        zbarw.connect("decoded",self.on_decodedd,label)
        main_vbox.pack_start(zbarw,False,False,0)
        
        
        
        im = GdkPixbuf.Pixbuf.new_from_file("apb-qr-code.png")
        zbarw.scan_image(im)
        

        
    def on_decodedd(self,zbarw,type_,data,label):
        print(type_)
        print(data)
        label.props.label  = str(type_) + " : " + str(data)

        
        
        
mw = MainWindow()
mw.connect("delete-event",Gtk.main_quit)
mw.show_all()
Gtk.main()
