#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  get_and_install_virtualbox_extension_pack.py
#  
#  Copyright 2018 youcef sourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import subprocess
import os
import urllib.request
import grp


def get_virtualbox_version():
    out=subprocess.Popen("virtualbox -h",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
    if out:
        return out.decode("utf-8").split("\n")[0].split()[-1].split("_")[0]
    else:
        return False

def download_pack():
    show_link = True
    version = get_virtualbox_version()[1:]
    print(version)
    if version:
        download_folder = os.path.expanduser("~/Downloads")
        os.makedirs(download_folder,exist_ok=True)
        pack_name       = "Oracle_VM_VirtualBox_Extension_Pack-{}.vbox-extpack".format(version)
        saveas          = os.path.join(download_folder,pack_name)
        link            = "http://download.virtualbox.org/virtualbox/{}/{}".format(version,pack_name) 
    else:
        return False
        
    try:
        url   = urllib.request.Request(link,headers={"User-Agent":"Mozilla/5.0"})
        opurl = urllib.request.urlopen(url,timeout=10)
        if  os.path.isfile(saveas):
            show_link = False
            while True:
                print("https://arfedora.blogspot.com\n")
                print ("{} Is Exists\n\nF To Force ReDownload || S To Skip Redownload || Q To Exit :".format(saveas))
                answer = input("- ")
                if answer == "q" or answer == "Q":
                    exit("\nbye...\n")
                elif answer == "S" or answer == "s":
                    return saveas
                elif answer == "F" or answer == "f":
                    break
        size = int(opurl.headers["Content-Length"])
        psize = 0
        if show_link:
            print("https://arfedora.blogspot.com\n")
        print ("["+"-"*80+"]"+" "+str(size)+"b"+" "+"0%",end="\r",flush=True)
        with open(saveas, 'wb') as op:
            while True:
                chunk = opurl.read(600)
                if not chunk:
                    break
                count = int((psize*80)//size)
                n = "#" * count
                fraction = count/80
                op.write(chunk)
                psize += 600
                print ("["+n+"-"*(80-count)+"]"+" "+str(size)+"b"+" "+str(round((psize*80)/size,2))+"%",end="\r",flush=True)
        print (" "*200,end="\r",flush=True)
        print ("["+"#"*80+"]"+" "+str(size)+"b"+" "+"100%")
    except Exception as e:
        print(e)
        return False
        
    return saveas

def add_pack_and_user_to_group_vboxusers(pack_location):
    if   os.getlogin() in grp.getgrnam("vboxusers").gr_mem:
        p = subprocess.call("yes | sudo VBoxManage extpack install --replace {} >/dev/null".format(pack_location),shell=True)
        if p!=0:
            return False
        else:
            return "n"
    else:
        p = subprocess.call("yes | sudo VBoxManage extpack install --replace {} >/dev/null|sudo usermod -a -G vboxusers {}".format(pack_location,os.getlogin()),shell=True)
        if p!=0:
            return False
        else:
            return "r"
    
pack_location = download_pack()
if pack_location:
    result = add_pack_and_user_to_group_vboxusers(pack_location)
    if result:
        if result=="n":
            print("\nInstall VirtualBox Extension Pack Done.\n")
        else:
            print("\nInstall VirtualBox Extension Pack Done.\nPlease Reboot System To Add User {} To Group vboxusers.\n".format(os.getlogin()))
    else:
        print("\nInstall VirtualBox Extension Pack Fail.\n")
else:
    print("\nDownload Fail.\n")
    
