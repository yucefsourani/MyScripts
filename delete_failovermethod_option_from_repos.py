#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  delete_failovermethod_options_from_repos.py
#  
#  Copyright 2021 yucef sourni <youssef.m.sourani@gmail.com>
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
import configparser
import os
import sys

if os.getuid()!=0:
     sys.exit("Run Script With Root Permissions.")
        
repos_locations = ["/etc/yum.repos.d"]

for repo_location in repos_locations:
    if os.path.isdir(repo_location):
        for repo_file_name in os.listdir(repo_location):
            if repo_file_name.endswith(".repo"):
                modified  = False
                repo_file = os.path.join(repo_location,repo_file_name)
                config    = configparser.ConfigParser()
                try:
                    config.read(repo_file)
                    for session_name in config.sections():
                        if config.has_option(session_name,"failovermethod"):
                            session = config[session_name]
                            del session["failovermethod"]
                            modified = True
                    if modified:
                        with open(repo_file, 'w') as configfile:
                            config.write(configfile)
                except Exception as e:
                    print(e)


