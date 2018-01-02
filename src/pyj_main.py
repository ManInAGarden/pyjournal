"""Hauptmodul für PyJournal
"""
import wx, wx.stc
import datetime

from pyj_daydata import DayData

class PyjMain(wx.Frame):
    """Haupt-Klasse für Py-Journal
    """
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super().__init__(*args, **kw)

        # create a panel in the frame
        #pnl = wx.Panel(self)
        sizer = wx.BoxSizer()

         # create a menu bar
        self.MakeMenuBar()

        self.CreateDayTree()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to Py-Journal")

        sizer.Add(self.day_tree, 2, flag= wx.EXPAND)
        self.day_editor = wx.stc.StyledTextCtrl(self)
        self.day_editor.SetLexerLanguage("markdown")
        sizer.Add(self.day_editor, 8, flag= wx.EXPAND)
        sizer.SetSizeHints(self)
        self.SetSizer(sizer)

    def MakeMenuBar(self):
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
       

    def CreateDayTree(self):
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
