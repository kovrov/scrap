APPNAME = "Directory listing scanner"
DATAFILES = ["./datafile1.txt", "./datafile2.txt"]
AGENTNAME = "webls/0.1"

"""
example of datafile headers:

http://s7d3.scene7.com/is/image/JanieAndJack/%s (i,) {'begin':100009412,'end':100009420}
http://www.gap.com/Asset_Archive/GPWeb/Assets/Product/%(prefix)03d/%(sku)06d/main/gp%(sku)06d-%(variant)02dp01v01.jpg {'prefix':i/1000,'sku':i,'variant':v} {'begin':501758,'end':501760,'variants':3}
"""

import urllib2
import time
import wx

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

def process_file(filename):
	found = 0
	# init data
	file = open(filename, 'r+')
	pattern = file.readline().split()
	url_format = pattern[0]
	url_format_args_expr = compile(pattern[1], '<string>', 'eval')
	url_args = eval(pattern[2])
	begin = url_args['begin']
	end = url_args['end']
	variants = url_args.get('variants')
	known = [line.split(' ', 1)[0] for line in file if len(line) > 1 and line[0] != '#']
	# init io
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', AGENTNAME)]
	# init gui
	MAX = end - begin
	dlg = wx.ProgressDialog(APPNAME, "scanning ...", MAX-1, None)
	for i in xrange(begin, end):
		if variants:
			for v in xrange (variants):
				iv = ":".join((str(i), str(v)))
				if iv in known:
					continue
				# update data
				url = url_format % eval(url_format_args_expr)
				info = img_info(opener, url)
				if info:
					found += 1
					file.write(iv + ' ' + url + ' ' + info['date'] + '\n')
				# update ui
				n = i - begin
				dlg.Update(n, "%d of %d" % (n + 1, MAX))
		else:
			if str(i) in known:
				continue
			# update data
			url = url_format % eval(url_format_args_expr)
			info = img_info(opener, url)
			if info:
				found += 1
				file.write(str(i) + ' ' + url + ' ' + info['date'] + '\n')
			# update ui
			n = i - begin
			dlg.Update(n, "%d of %d" % (n + 1, MAX))
	# update data
	file.write("# scan ended at " + time.strftime("%Y/%m/%d-%H:%M") + " - " + str(found) + ' images found\n')
	# update ui
	return (n+1, found)

if __name__ == "__main__":
	total_scanned = 0
	total_found = 0
	app = wx.App(0)
	for filename in DATAFILES:
		scanned, found = process_file(filename)
		total_scanned += scanned
		total_found += found
	dlg = wx.MessageDialog(None, "Done.\n"
							"Scanned %d URLs, found %d files." % (total_scanned, total_found),
							APPNAME, wx.OK | wx.ICON_INFORMATION)
	dlg.ShowModal()
	dlg.Destroy()
