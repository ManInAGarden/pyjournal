"""Hauptmodul für PyJournal
"""
import datetime
import wx
import wx.stc

from pyj_daydata import DayData

class PyjMain(wx.Frame):
    """Haupt-Klasse für Py-Journal
    """
    def __init__(self, *args, **kw):
        """Konstruktor für den PyjMain Frame"""
        # ensure the parent's __init__ is called
        super().__init__(*args, **kw)

        # create a panel in the frame
        #pnl = wx.Panel(self)
        sizer = wx.BoxSizer()

         # create a menu bar
        self.create_menu()

        self.create_day_tree()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to Py-Journal")

        sizer.Add(self.day_tree, 2, flag= wx.EXPAND)
<<<<<<< HEAD
        self.create_day_editor(sizer)
=======
        self.day_editor = wx.stc.StyledTextCtrl(self)
        self.day_editor.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.day_editor.StyleSetForeground(wx.stc.STC_C_COMMENT, wx.Colour(150,150,150))
        self.day_editor.StyleSetForeground(wx.stc.STC_C_STRING, wx.Colour(150,0,0))
        self.day_editor.StyleSetForeground(wx.stc.STC_C_IDENTIFIER, wx.Colour(40,0,60))
        #wx.stc.T("return for while break continue")
        self.day_editor.SetKeyWords(0, "return for while break continue")
        self.day_editor.SetKeyWords(1, "const int float void char double")
        self.day_editor.SetKeyWords(2, "def class")
        sizer.Add(self.day_editor, 8, flag= wx.EXPAND)
>>>>>>> dd7ca9b9677ad18c6377b0a9962b3aefd49f7901
        sizer.SetSizeHints(self)
        self.SetSizer(sizer)
        self.day_editor = self.create_day_editor(self)
        sizer.Add(self.day_editor, 8, flag= wx.EXPAND)

    def create_day_editor(self, sizer):
        editor = wx.stc.StyledTextCtrl(self)
        editor.SetLexer(wx.stc.STC_LEX_PYTHON)
        return editor

    def create_menu(self):
        """Das Hauptmenü aufbauen
        """
        file_men = wx.Menu()
        save_item = file_men.Append(-1,
                                  "&Sichern\tCtrl-S",
                                  "Aktuelle Daten Speichern")
        self.Bind(wx.EVT_MENU, self.on_save,  save_item)
        
        print_day_item = file_men.Append(-1, "&Tag drucken\tCtrl-P", "Den aktuellen Tag drucken")
        self.Bind(wx.EVT_MENU, self.on_print_day,  print_day_item)

        exit_item = file_men.Append(-1, "&Beenden\tCtrl+Q", "Py-Journal Beenden")
        self.Bind(wx.EVT_MENU, self.on_exit,  exit_item)

        help_men = wx.Menu()
        markdown_help_item = help_men.Append(-1, "&Markdown-Hilfe", "Zeigt Hilfe zur Markdown Sytax an")
        about_item = help_men.Append(-1, "Über PyJournal", "Zeigt Infos zur installierten Version an")
        
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
