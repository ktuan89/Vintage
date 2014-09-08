import sublime, sublime_plugin
from .vintage import transform_selection

class Bookmark():
    def __init__(self, view_id, row, col):
        self.view_id = view_id
        self.row = row
        self.col = col

bookmarks = {}

class ViKtSetBookmark(sublime_plugin.WindowCommand):
    def run(self, character):
        view = self.window.active_view()
        for s in view.sel():
            if s.empty():
                sublime.status_message("Set bookmark " + character)
                (row, col) = view.rowcol(s.begin())
                bookmarks[character] = Bookmark(view.id(), row, col)
                return
        sublime.status_message("Unable to set bookmark " + character)

class ViKtWindowSelectBookmark(sublime_plugin.WindowCommand):
    def run(self, view_id, row, col):
        view = None
        for v in self.window.views():
            if v.id() == view_id:
                view = v
        if view is not None:
            self.window.focus_view(view)
            text_position = view.text_point(row, col)
            view.run_command('vi_kt_view_select_bookmark', {"position": text_position})

class ViKtViewSelectBookmark(sublime_plugin.TextCommand):
    def run(self, edit, position):
        self.view.show_at_center(position)
        transform_selection(self.view, lambda pt: position, extend=True)

class ViKtSelectBookmark(sublime_plugin.TextCommand):
    def run(self, edit, character, extend=True):
        if character in bookmarks:
            bookmark = bookmarks[character]
            if bookmark.view_id == self.view.id():
                text_position = self.view.text_point(bookmark.row, bookmark.col)
                visible_region = self.view.visible_region()

                if visible_region.begin() <= text_position and text_position < visible_region.end():
                    pass
                else:
                    self.view.show_at_center(text_position)

                transform_selection(self.view, lambda pt: text_position, extend=extend)
            else:
                self.view.window().run_command('vi_kt_window_select_bookmark', {"view_id": bookmark.view_id, "row": bookmark.row, "col": bookmark.col})

