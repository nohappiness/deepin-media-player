#! /usr/bin/env python
# -*- coding: utf-8 -*-

# houshaohui:code->[str_size function, get size, type, mtime, combox]. 
# Copyright (C) 2012 Deepin, Inc.
#               2012 Hailong Qiu
#
# Author:     Hailong Qiu <356752238@qq.com>
# Maintainer: Hailong Qiu <356752238@qq.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Deein ui.
from dtk.ui.utils import alpha_color_hex_to_cairo, color_hex_to_cairo
from dtk.ui.draw import draw_pixbuf

from skin import app_theme

import gtk
import gobject

'''
100 / 500 = 0.2
当前高亮位置(x=100) * 0.2 = 20
x = 500 -> 500 * 0.2 = 100
x = 100 -> 100 * 0.2 = 20
'''

class VolumeButton(gtk.EventBox):
    __gsignals__ = {
        "get-value-event":(gobject.SIGNAL_RUN_LAST,
                           gobject.TYPE_NONE,(gobject.TYPE_INT,gobject.TYPE_INT,))
        }
    def __init__(self,
                 volume_max_value = 100,
                 volume_width     = 500,
                 volume_x         = 50,
                 volume_y         = 50,
                 scroll_bool = False,
                 bg_color = app_theme.get_alpha_color("volumebutton_bg"),
                 fg_color = app_theme.get_alpha_color("volumebutton_fg"),
                 min_volume_pixbuf   = app_theme.get_pixbuf("min_volume.png"),
                 mid_volume_pixbuf   = app_theme.get_pixbuf("mid_volume.png"),
                 max_volume_pixbuf   = app_theme.get_pixbuf("max_volume.png"),
                 mute_volume_pixbuf  = app_theme.get_pixbuf("mute.png"),
                 point_volume_pixbuf = app_theme.get_pixbuf("volume_button.png")
                 ):
        
        gtk.EventBox.__init__(self)
        '''Init pixbuf.'''
        self.bg_color               = bg_color
        self.fg_color               = fg_color
        self.min_volume_pixbuf      = min_volume_pixbuf
        self.mid_volume_pixbuf      = min_volume_pixbuf
        self.max_volume_pixbuf      = max_volume_pixbuf
        self.mute_volume_pixbuf     = mute_volume_pixbuf
        self.point_volume_pixbuf    = point_volume_pixbuf        
        '''Init Set VolumeButton attr.'''
        self. set_visible_window(True)
        '''Init value.'''
        self.current_value    = 0
        self.mute_bool        = False  # left.
        self.drag             = False  # right.
        self.volume_max_value = volume_max_value
        self.volume_width     = volume_width
        self.volume_right_x   = volume_x
        self.volume_right_y   = volume_y
        # bg value.
        self.bg_x    = 0
        self.bg_y    = self.volume_right_y
        self.bg_padding_x = self.volume_right_x
        # fg value.
        self.fg_x    = 0
        self.fg_y    = self.volume_right_y
        self.fg_padding_x = self.volume_right_x
        # point value.
        self.point_x = 0
        self.point_y = self.volume_right_y
        self.point_padding_x = self.volume_right_x
        
        '''Init VolumeButton event.'''
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.connect("expose-event",         self.expose_draw_volume)
        self.connect("motion-notify-event",  self.motion_mouse_set_point)
        self.connect("button-press-event",   self.press_mouse_set_point)
        self.connect("button-release-event", self.release_mouse_set_point)
        # scroll event.
        if scroll_bool:
            self.connect("scroll-event",         self.scroll_mouse_set_point)
                
    def set_volume_position(self, x, y):        
        self.volume_right_x = x
        self.volume_right_y = y
        # Set x.
        self.bg_padding_x    = self.volume_right_x
        self.fg_padding_x    = self.volume_right_x
        self.point_padding_x = self.volume_right_x
        # Set y.
        self.bg_y    = self.volume_right_y
        self.fg_y    = self.volume_right_y
        self.point_y = self.volume_right_y
        
    def set_volume_max_value(self, value):    
        self.volume_max_value = value
        
    def scroll_mouse_set_point(self, widget, event):    
        point_width_average      = self.point_volume_pixbuf.get_pixbuf().get_width() / 2 
        temp_min = (self.point_x + 50 - point_width_average)
        temp_max = (self.point_x + 50 + self.volume_width - point_width_average)

        if event.direction == gtk.gdk.SCROLL_UP:
            if self.point_padding_x >= temp_max:
                self.point_padding_x = temp_max
            else:    
                self.point_padding_x += 1
        elif event.direction == gtk.gdk.SCROLL_DOWN:
            if self.point_padding_x <= temp_min:
                self.point_padding_x = temp_min
            else:    
                self.point_padding_x -= 1
            
        self.queue_draw()
        
    def set_point_padding_x(self, event):
        self.point_padding_x = int(event.x)        
        self.queue_draw()
        
    def press_mouse_set_point(self, widget, event):    
        self.set_point_padding_x(event)
        self.drag = True
        
    def release_mouse_set_point(self, widget, event):        
        self.drag = False
        
    def motion_mouse_set_point(self, widget, event):
        if self.drag:
            self.set_point_padding_x(event)
        
        
    def expose_draw_volume(self, widget, event):
        self.draw_volume_left(widget, event)
        self.draw_volume_right(widget, event)         
        self.emit("get-value-event", self.current_value, self.mute_bool)
        return True
        
    def draw_volume_left(self, widget, event):
        cr = widget.window.cairo_create()
        x, y, w, h = widget.allocation
                    
        
    def draw_volume_right(self, widget, event):
        cr = widget.window.cairo_create()
        x, y, w, h = widget.allocation
        point_width_average      = self.point_volume_pixbuf.get_pixbuf().get_width() / 2 
        ##################################################
        # Draw bg. ->
        cr.set_source_rgba(*alpha_color_hex_to_cairo(self.bg_color.get_color_info()))
        cr.move_to(self.bg_x + self.bg_padding_x,
                   self.bg_y + point_width_average)
        cr.line_to(self.bg_x + self.bg_padding_x + self.volume_width,
                   self.bg_y + point_width_average)
        cr.stroke()
        ##################################################
        
        temp_fg_padding_x = self.point_padding_x - (self.fg_x + self.fg_padding_x) 
        
        # if 0 <= temp_fg_padding_x <= self.volume_width:
        if temp_fg_padding_x < 0:
            temp_fg_padding_x = 0
        if temp_fg_padding_x > self.volume_width:    
            temp_fg_padding_x = self.volume_width
        # Get current value.    
        self.current_value = temp_fg_padding_x * (float(self.volume_max_value) / self.volume_width)    

        # Draw fg. 
        cr.set_source_rgba(*alpha_color_hex_to_cairo((self.fg_color.get_color_info())))
        cr.move_to(self.fg_x + self.fg_padding_x,
                   self.fg_y + point_width_average)
        cr.line_to(self.fg_x + self.fg_padding_x + temp_fg_padding_x,
                   self.fg_y + point_width_average)
        cr.stroke()        
        #################################################        
        # Draw point.                        
        temp_point_padding_x     = (self.point_x + self.point_padding_x - point_width_average)

        temp_min = (self.point_x + self.volume_right_x - point_width_average)
        temp_max = (self.point_x + self.volume_right_x + self.volume_width - point_width_average)
        if temp_point_padding_x < temp_min:
            temp_point_padding_x = temp_min
        if temp_point_padding_x > temp_max:    
            temp_point_padding_x = temp_max
            
        draw_pixbuf(cr, 
                    self.point_volume_pixbuf.get_pixbuf(), 
                    temp_point_padding_x,
                    self.point_y)    
            
        
gobject.type_register(VolumeButton)                       

if __name__ == "__main__":        
    def set_time_position():
        volume_button.set_volume_position(100, 100)
    def get_volume_value(volume_button, value, mute_bool):    
        print volume_button
        print value
        print mute_bool
        
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    volume_button = VolumeButton()
    volume_button.connect("get-value-event", get_volume_value)
    win.add(volume_button)
    gtk.timeout_add(2000, set_time_position)
    win.show_all()
    gtk.main()

