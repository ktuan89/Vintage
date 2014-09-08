import sublime, sublime_plugin
import os
import re
from subprocess import Popen, PIPE
#import subprocess

from os import listdir
from os.path import isfile, join

# Global state for current mode (insert/command)
g_current_mode_is_command = True
g_count = 0

def is_legal_path_char(c):
    # XXX make this platform-specific?
    return c not in " \n\"|*<>{}[]()"

def move_while_path_character(view, start, is_at_boundary, increment=1):
    while True:
        if not is_legal_path_char(view.substr(start)):
            break
        start = start + increment
        if is_at_boundary(start):
            break
    return start

class ViOpenFileUnderSelectionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        #sel = self.view.sel()[0]
        region = self.view.sel()[0]
        """if not sel.empty():
            file_name = self.view.substr(sel)
        else:
            caret_pos = self.view.sel()[0].begin()
            current_line = self.view.line(caret_pos)

            left = move_while_path_character(
                                            self.view,
                                            caret_pos,
                                            lambda x: x < current_line.begin(),
                                            increment=-1)
            right = move_while_path_character(
                                            self.view,
                                            caret_pos,
                                            lambda x: x > current_line.end(),
                                            increment=1)
            file_name = self.view.substr(sublime.Region(left + 1, right))"""

        if region.empty():
            line = self.view.line(region)
            file_name = self.view.substr(line)
        else:
            file_name = self.view.substr(region)

        """file_name = os.path.join(os.path.dirname(self.view.file_name()),
                                    file_name)"""

        if file_name.endswith(":"):
            file_name = file_name[0:-1]

        if os.path.exists(file_name):
            self.view.window().open_file(file_name)

class ViSaveAndExit(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('save')
        self.window.run_command('close')
        if len(self.window.views()) == 0:
            self.window.run_command('close')


class MoveFocusedViewToBeginning(sublime_plugin.EventListener):
    def on_activated(self, view):
        if view.window() is None:
            return
        has_view = False
        for v in view.window().views():
            if v.id() == view.id():
                has_view = True
        if not has_view:
            return
        global g_current_mode_is_command
        if g_current_mode_is_command and not view.settings().get('command_mode'):
            view.run_command('exit_insert_mode')
        if view.settings().get('command_mode') and not g_current_mode_is_command:
            view.run_command('enter_insert_mode')

    def on_deactivated(self, view):
        if view.window() is None:
            return
        has_view = False
        for v in view.window().views():
            if v.id() == view.id():
                has_view = True
        if not has_view:
            return
        global g_current_mode_is_command
        if view.settings().get('command_mode'):
            g_current_mode_is_command = True
        else:
            g_current_mode_is_command = False

