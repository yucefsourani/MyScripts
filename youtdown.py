#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import youtube_dl
import threading
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk , Pango, GLib, Gdk

class DownloadVideo(threading.Thread):
    def __init__(self,link,start_button,stop_button,progressbar):
        threading.Thread.__init__(self)
        
        self.link         = link
        self.start_button = start_button
        self.stop_button  = stop_button
        self.progressbar  = progressbar
        
        self.break_       = False
    
    def run(self):
        GLib.idle_add(self.progressbar.show)
        GLib.idle_add(self.start_button.set_sensitive,False)
        GLib.idle_add(self.stop_button.set_sensitive,True)
        
        video_location = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_VIDEOS )
        options = {}
        options["format"]          = "best"
        options["socket_timeout"]  = 10
        options["ignoreerrors"]    = True
        options["nooverwrites"]    = True
        options["continue_dl"]     = True
        options["outtmpl"]         = os.path.join(video_location,"%(id)s.%(format)s.%(title)s.%(ext)s")
        options["progress_hooks"]  = []
        options["progress_hooks"].append(self.my_hook)
            
        try:
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([self.link])
        except Exception as e:
            GLib.idle_add(self.progressbar.set_text,"error")
            GLib.idle_add(self.start_button.set_sensitive,True)
            GLib.idle_add(self.stop_button.set_sensitive,False)
            print(e)
    
    def my_hook(self,info):
        if self.break_:
            GLib.idle_add(self.start_button.set_sensitive,True)
            GLib.idle_add(self.stop_button.set_sensitive,False)
            raise Exception('Canceled!')
        status  = info["status"] 
        if status == 'finished':
            print('finished')
            GLib.idle_add(self.progressbar.set_text,"Done")
            GLib.idle_add(self.start_button.set_sensitive,True)
            GLib.idle_add(self.stop_button.set_sensitive,False)
            return 
        elif status == "error":
            print('error')
            GLib.idle_add(self.progressbar.set_text,"error")
            GLib.idle_add(self.start_button.set_sensitive,True)
            GLib.idle_add(self.stop_button.set_sensitive,False)
            return 
        
        _percent_str      = info["_percent_str"]
        _speed_str        = info["_speed_str"]
        _eta_str          = info["_eta_str"]
        filename          = info["filename"]
        tmpfilename       = info["tmpfilename"]
        total_bytes       = info["total_bytes"]
        downloaded_bytes  = info["downloaded_bytes"]
        print("\n*************************************************************")
        print(_percent_str)
        print(_speed_str)
        print(_eta_str)
        print(filename)
        print(tmpfilename)
        print(total_bytes)
        print(downloaded_bytes)
        print("*************************************************************\n")
        count = int((downloaded_bytes*100)//total_bytes)
        fraction = count/100
        GLib.idle_add(self.progressbar.set_fraction,fraction)
        GLib.idle_add(self.progressbar.set_text,_percent_str+" "+str(downloaded_bytes)+"/"+str(total_bytes)+" B")


#download_video = DownloadVideo("https://www.youtube.com/watch?v=vbpGVi7kRR4")
#download_video.start()

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        
        mainvbox = Gtk.VBox()
        mainvbox.props.margin = 10
        self.add(mainvbox)
        
        link_hbox = Gtk.HBox()
        link_hbox.set_spacing(10)
        mainvbox.pack_start(link_hbox,False,False,0)
        
        link_label = Gtk.Label()
        link_label.set_label("Link")
        link_hbox.pack_start(link_label,False,False,0)
        
        link_entry = Gtk.Entry()
        link_entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY ,"edit-clear-symbolic")
        link_entry.connect("icon_press",self.on_entry_icon_press)
        link_entry.set_placeholder_text("Enter Video Link...")
        link_hbox.pack_start(link_entry,True,True,0)
        
        header_bar = Gtk.HeaderBar()
        header_bar.props.show_close_button = True
        self.set_titlebar(header_bar)
        
        self.start_button = Gtk.Button.new_from_icon_name("media-playback-start-symbolic",Gtk.IconSize.SMALL_TOOLBAR )
        self.start_button.connect("clicked",self.on_start_button_clicked,link_entry)
        
        self.stop_button  = Gtk.Button.new_from_icon_name("media-playback-stop-symbolic",Gtk.IconSize.SMALL_TOOLBAR )
        self.stop_button.set_sensitive(False)
        self.stop_button.connect("clicked",self.on_stop_button_clicked)
        
        self.paste_button  = Gtk.Button.new_from_icon_name("edit-paste-symbolic",Gtk.IconSize.SMALL_TOOLBAR )
        self.paste_button.connect("clicked",self.on_paste_button_clicked,link_entry)
        
        header_bar.pack_start(self.start_button)
        header_bar.pack_start(self.stop_button)
        header_bar.pack_end(self.paste_button)
        
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_show_text(True)
        self.progress_bar.props.no_show_all = True
        
        self.progress_bar.set_ellipsize(Pango.EllipsizeMode.END)
        mainvbox.pack_start(self.progress_bar,False,False,0)
        
        
    def on_entry_icon_press(self,entry, icon_pos, event):
        entry.set_text("")
        
    def on_start_button_clicked(self,button,link_entry):
        link = link_entry.get_text().strip()
        if not link:
            return
        self.download_video = DownloadVideo(link,button,self.stop_button,self.progress_bar)
        self.download_video.start()
        
        
    def on_stop_button_clicked(self,button):
        self.download_video.break_ = True
        
    def on_paste_button_clicked(self,button,link_entry):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD )
        text = clipboard.wait_for_text()
        if text:
            link_entry.set_text(text)
        

mainwindow = MainWindow()
mainwindow.connect("delete-event",Gtk.main_quit)
mainwindow.show_all()
Gtk.main()






