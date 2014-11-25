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

class ExtendedSwitcherHaha(sublime_plugin.WindowCommand):
    # declarations
    open_files = []
    open_views = []
    window = []
    settings = []

    # lets go
    def run(self, list_mode):
        print "Here here here"
        # self.view.insert(edit, 0, "Hello, World!")
        self.open_files = []
        self.open_views = []
        self.window = sublime.active_window()
        self.settings = sublime.load_settings('ExtendedSwitcher.sublime-settings')

        for f in self.getViews(list_mode):
            # if skip the current active is enabled do not add the current file it for selection
            if self.settings.get('skip_current_file') == True:
                if f.id() == self.window.active_view().id():
                    continue

            self.open_views.append(f) # add the view object
            file_name = f.file_name() # get the full path

            if file_name:
                if f.is_dirty():
                    file_name += self.settings.get('mark_dirty_file_char') # if there are any unsaved changes to the file

                if self.settings.get('show_full_file_path') == True:
                    self.open_files.append(os.path.basename(file_name) + ' - ' + os.path.dirname(file_name))
                else:
                    self.open_files.append(os.path.basename(file_name))

            else:
                self.open_files.append("Untitled")

        if self.check_for_sorting() == True:
            self.sort_files()

        self.window.show_quick_panel(self.open_files, self.tab_selected) # show the file list

    # display the selected open file
    def tab_selected(self, selected):
        if selected > -1:
            self.window.focus_view(self.open_views[selected])

        return selected

    # sort the files for display in alphabetical order
    def sort_files(self):
        open_files = self.open_files
        open_views = []

        open_files.sort()

        for f in open_files:
            for fv in self.open_views:
                if fv.file_name():
                    f = f.replace(" - " + os.path.dirname(fv.file_name()),'')
                    if (f == os.path.basename(fv.file_name())) or (f == os.path.basename(fv.file_name())+self.settings.get('mark_dirty_file_char')):
                        open_views.append(fv)
                        self.open_views.remove(fv)

                if f == "Untitled" and not fv.file_name():
                    open_views.append(fv)
                    self.open_views.remove(fv)

        self.open_views = open_views



    # flags for sorting
    def check_for_sorting(self):
        if self.settings.has("sort"):
            return self.settings.get("sort", False)


    def getViews(self, list_mode):
        views = []
        # get only the open files for the active_group
        if list_mode == "active_group":
            views = self.window.views_in_group(self.window.active_group())

        # get all open view if list_mode is window or active_group doesnt not have any files open
        if (list_mode == "window") or (len(views) < 1):
            views = self.window.views()

        return views
