"""Hauptmodul für PyJournal
"""
import datetime
import keyword
import wx
import wx.stc

from pyj_daydata import DayData


class PyjMain(wx.Frame):
    """Haupt-Klasse für Py-Journal
    """

    def __init__(self, *args, **kw):
        """Konstruktor für den PyjMain Frame"""
        super().__init__(*args, **kw)

        sizer = wx.BoxSizer()

        self.create_menu()
        self.create_day_tree()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to Py-Journal")

        sizer.Add(self.day_tree, 2, flag=wx.EXPAND)
        self.day_editor = self.create_day_editor()
        sizer.Add(self.day_editor, 8, flag=wx.EXPAND)
        sizer.SetSizeHints(self)
        self.SetSizer(sizer)

    def create_day_editor(self):
        """Den Editor für die Bearbeitung des Tagesjournals aufbauen"""
        editor = wx.stc.StyledTextCtrl(self, size=wx.Size(500, 300))
        editor.SetLexer(wx.stc.STC_LEX_PYTHON)
        keyw = " ".join(keyword.kwlist)
        editor.SetKeyWords(0, keyw)
        if wx.Platform == '__WXMSW__':
            faces = {'times': 'Times New Roman',
                     'mono': 'Courier New',
                     'helv': 'Arial',
                     'other': 'Comic Sans MS',
                     'size': 10,
                     'size2': 8,
                     }
        else:
            faces = {'times': 'Times',
                     'mono': 'Courier',
                     'helv': 'Helvetica',
                     'other': 'new century schoolbook',
                     'size': 12,
                     'size2': 10,
                     }

        # Global default styles for all languages
        editor.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,
                            "face:%(helv)s,size:%(size)d" % faces)
        editor.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,
                            "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
        editor.StyleSetSpec(wx.stc.STC_STYLE_CONTROLCHAR,
                            "face:%(other)s" % faces)
        editor.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,
                            "fore:#FFFFFF,back:#0000FF,bold")
        editor.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,
                            "fore:#000000,back:#FF0000,bold")

        # Python styles
        # White space
        editor.StyleSetSpec(wx.stc.STC_P_DEFAULT,
                            "fore:#808080,face:%(helv)s,size:%(size)d" % faces)
        # Comment
        editor.StyleSetSpec(wx.stc.STC_P_COMMENTLINE,
                            "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
        # Number
        editor.StyleSetSpec(wx.stc.STC_P_NUMBER,
                            "fore:#007F7F,size:%(size)d" % faces)
        # String
        editor.StyleSetSpec(wx.stc.STC_P_STRING,
                            "fore:#7F007F,italic,face:%(times)s,size:%(size)d" % faces)
        # Single quoted string
        editor.StyleSetSpec(
            wx.stc.STC_P_CHARACTER, "fore:#7F007F,italic,face:%(times)s,size:%(size)d" % faces)
        # Keyword
        editor.StyleSetSpec(wx.stc.STC_P_WORD,
                            "fore:#00007F,bold,size:%(size)d" % faces)
        # Triple quotes
        editor.StyleSetSpec(wx.stc.STC_P_TRIPLE,
                            "fore:#7F0000,size:%(size)d" % faces)
        # Triple double quotes
        editor.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE,
                            "fore:#7F0000,size:%(size)d" % faces)
        # Class name definition
        editor.StyleSetSpec(wx.stc.STC_P_CLASSNAME,
                            "fore:#0000FF,bold,underline,size:%(size)d" % faces)
        # Function or method name definition
        editor.StyleSetSpec(wx.stc.STC_P_DEFNAME,
                            "fore:#007F7F,bold,size:%(size)d" % faces)
        # Operators
        editor.StyleSetSpec(wx.stc.STC_P_OPERATOR,
                            "bold,size:%(size)d" % faces)
        # Identifiers
        editor.StyleSetSpec(wx.stc.STC_P_IDENTIFIER,
                            "fore:#808080,face:%(helv)s,size:%(size)d" % faces)
        # Comment-blocks
        editor.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK,
                            "fore:#7F7F7F,size:%(size)d" % faces)
        # End of line where string is not closed
        editor.StyleSetSpec(wx.stc.STC_P_STRINGEOL,
                            "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)
        return editor

    def create_menu(self):
        """Das Hauptmenü aufbauen
        """
        file_men = wx.Menu()
        save_item = file_men.Append(-1,
                                    "&Sichern\tCtrl-S",
                                    "Aktuelle Daten Speichern")
        self.Bind(wx.EVT_MENU, self.on_save,  save_item)

        print_day_item = file_men.Append(-1, "&Tag drucken\tCtrl-P",
                                         "Den aktuellen Tag drucken")
        self.Bind(wx.EVT_MENU, self.on_print_day,  print_day_item)

        exit_item = file_men.Append(-1, "&Beenden\tCtrl+Q",
                                    "Py-Journal Beenden")
        self.Bind(wx.EVT_MENU, self.on_exit,  exit_item)

        help_men = wx.Menu()
        markdown_help_item = help_men.Append(
            -1, "&Markdown-Hilfe", "Zeigt Hilfe zur Markdown Sytax an")
        about_item = help_men.Append(-1, "Über PyJournal",
                                     "Zeigt Infos zur installierten Version an")

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_men, "&Datei")
        menu_bar.Append(help_men, "&Hilfe")

        self.SetMenuBar(menu_bar)

    def create_day_tree(self):
        self.day_tree = wx.TreeCtrl(self, size=wx.Size(150, 300))
        root = self.day_tree.AddRoot("Root")

        yr = self.day_tree.AppendItem(root, "2018")
        month = self.day_tree.AppendItem(yr, "01")
        daydt = datetime.date.today()
        day_data = DayData(daydt, "#{}\n".format(daydt))
        day = self.day_tree.AppendItem(month, day_data.to_str(), data=day_data)

    def on_exit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def on_save(self, event):
        pass

    def on_print_day(self, event):
        pass


if __name__ == '__main__':
    app = wx.App()
    # Then a frame.
    frm = PyjMain(None, title="PyJournal")
    frm.Show()
    app.MainLoop()
