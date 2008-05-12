import urllib2


APPNAME = "Directory listing scanner"
DATAFILE = "image_robot.txt"
AGENTNAME = "webls/0.1"

def img_info(opener, url):
	try:
		res = opener.open(url)
	except:
		return None
	info = res.info()
	res.close()
	if info["Content-Type"].lower() not in ("image/jpeg", "image/png"):
		return None
	if int(info["Content-Length"]) < 1024:
		return None
	return {'date': info["Last-Modified"],
			'length': int(info["Content-Length"]),
			'type': info["Content-Type"]}


if __name__ == "__main__":
	import wx
	import time
	# init data
	file = open(DATAFILE, 'a+')
	pattern = file.readline().split()
	url = pattern[0]
	begin = int(pattern[1])
	end = int(pattern[2])
	known = [int(line.split()[0]) for line in file if line and line[0] != '#']
	found = 0
	# init io
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', AGENTNAME)]
	# init gui
	app = wx.App()
	MAX = end - begin
	dlg = wx.ProgressDialog(APPNAME, "scanning ...", MAX-1, None)
	for i in xrange(begin, end):
		if i in known:
			continue
		# update data
		info = img_info(opener, url % i)
		if info:
			found += 1
			file.write(str(i) + ' ' + info['date'] + '\n')
		# update ui
		n = i - begin
		dlg.Update(n, "%d of %d" % (n + 1, MAX))
	# update data
	file.write("# scan ended at " + time.strftime("%Y/%m/%d-%H:%M") + " - " + str(found) + ' images found\n')
	# update ui
	dlg = wx.MessageDialog(None, "Done.\n"
							"Scanned %d URLs, found %d files." % (n+1, found),
							APPNAME, wx.OK | wx.ICON_INFORMATION)
	dlg.ShowModal()
	dlg.Destroy()
