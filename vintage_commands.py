import sublime, sublime_plugin
import os
#import subprocess

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

class CopyCurrentWord(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                sublime.set_clipboard(self.view.substr(self.view.word(region.begin())))

class OpenFileInXcode(sublime_plugin.TextCommand):
    def run(self, edit):
        if self.view.file_name() is not None:
            #print self.view.file_name()
            #subprocess.call(["open", "-a", "/Applications/Xcode.app", self.view.file_name()])
            os.system("open -a /Applications/Xcode.app '" + self.view.file_name() + "'")

class ViSaveAndExit(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command('save')
        self.window.run_command('close')
        if len(self.window.views()) == 0:
            self.window.run_command('close')


#class MoveFocusedViewToBeginning(sublime_plugin.EventListener):
#    def on_activated(self, view):
#        view.window().set_view_index(view, 0, 0)
