# -*- coding: utf-8 -*-

import wx
import wx.xrc
import wx.richtext
import os
from ffmpy import FFmpeg
import threading
import platform

class window ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 537,343 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.url_label = wx.StaticText( self, wx.ID_ANY, u"m3u8链接", wx.DefaultPosition, wx.Size( 100,200 ), 0 )
		self.url_label.Wrap( -1 )

		fgSizer2.Add( self.url_label, 0, wx.ALL, 5 )

		self.urls = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 500,200 ), 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		fgSizer2.Add( self.urls, 1, wx.EXPAND |wx.ALL, 5 )

		self.path_label = wx.StaticText( self, wx.ID_ANY, u"保存路径", wx.DefaultPosition, wx.Size( 100,50 ), 0 )
		self.path_label.Wrap( -1 )

		fgSizer2.Add( self.path_label, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.path = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.Size( 400,50 ), wx.DIRP_DEFAULT_STYLE )
		fgSizer2.Add( self.path, 0, wx.ALL, 5 )


		fgSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.download_btn = wx.Button( self, wx.ID_ANY, u"下载", wx.DefaultPosition, wx.Size( 80,40 ), 0 )
		fgSizer2.Add( self.download_btn, 0, wx.ALL, 5 )


		self.SetSizer( fgSizer2 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.download_btn.Bind( wx.EVT_BUTTON, self.download )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def download( self, event ):
		url = self.urls.GetValue()
		path = self.path.GetPath()

		url_arr = url.split(";")
		threading_arr = []
		k = 1
		for i in url_arr:
			filename = '{path}/{file}.mp4'.format(path=path, file=k)
			t = threading.Thread(target=self.download_video, args=(i, filename,))
			threading_arr.append(t)
			k += 1

		for i in threading_arr:
			i.start()
			# i.join()
		for i in threading_arr:
			i.join()

		# print("下载完成")
		dlg = wx.MessageDialog(None, u"下载完成", u"提示", wx.OK_DEFAULT)
		if dlg.ShowModal() == wx.ID_YES:
			self.Close(True)
		dlg.Destroy()


	def download_video(self, url, filename):

		xh = platform.system()
		ml = ""
		if xh == "Darwin":
			ml = "./ffmpeg-mac/ffmpeg"
		elif xh == "Windows":
			ml = "./ffmpeg-win64/bin/ffmpeg.exe"
		if os.path.isfile(filename):
			os.unlink(filename)
		ff = FFmpeg(
			executable=ml,
			inputs={url: None},
			outputs={filename: None}
		)
		ff.run()




if __name__ == '__main__':
	app = wx.App()
	frame = window(None)
	frame.SetSize((600, 400))
	frame.SetMaxSize((600, 400))
	frame.SetMinSize((600, 400))
	frame.Show(True)
	app.MainLoop()