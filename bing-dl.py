# -*- coding: utf-8 -*-

import os
import time
import requests
import datetime
import re

IMG_PATH = '/home/cc/downloads/bing_wallpaper'

def get_pic_name(name):
	pattern = re.compile("](.*)(_EN-US|_ZH-CN)")
	g = pattern.search(name)
	if g:
		return g.groups(0)[0]
	else:
		return ''

def list_pic(path):
	pic_name = os.listdir(path)
	pics = []
	pattern = re.compile("](.*)(_EN-US|_ZH-CN)")

	for name in pic_name:
		g = pattern.search(name)
		if g:
			pics.append(g.groups(0)[0])

	return pics


if __name__ == '__main__':
	nc  = int(time.time() * 1000)
	n   = 8
	# idx = 0
	print "[*] cn"
	for idx in [0,7]:
		post_url = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=%d&n=%d&nc=%d&pid=hp' % (idx, n, nc)
		res = requests.get(post_url)
		urls = []
		if res:
			img_json = res.json()
			for row in img_json['images']:
				name = row['url'].rfind('/rb/')
				urls.append([row['startdate'], row['url'].split('/')[-1], 'http://cn.bing.com' + row['url']])
		for img in urls:
			fn = '['+img[0]+']'+img[1]
			try:
				os.stat(fn)
			except OSError:
				res = requests.get(img[-1])
				print "[+] download: "+img[1]
				with open(IMG_PATH+'/['+img[0]+']'+img[1], 'w') as fd:
					fd.write(res.content)
			else:
				print "[-] skip: "+img[1]

	print "[*] world"
	pics = list_pic(IMG_PATH)
	for idx in [0,7]:
		post_url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=%d&n=%d&nc=%d&pid=hp&scope=web&FORM=QBLH&intlF=&quiz=1&fav=1' % (idx, n, nc)
		res = requests.get(post_url, cookies=dict(ENSEARCH="BENVER=1"))
		urls = []
		if res:
			img_json = res.json()
			for row in img_json['images']:
				name = row['url'].rfind('/rb/')
				urls.append([row['startdate'], row['url'].split('/')[-1], 'http://cn.bing.com' + row['url']])
		for img in urls:
			d1 = datetime.datetime(int(img[0][:4]), int(img[0][4:6]), int(img[0][6:8]))
			d2 = d1 - datetime.timedelta(days=1)
			img[0] = unicode("{:04}{:02}{:02}".format(d2.year, d2.month, d2.day))
			
			fn = '['+img[0]+']'+img[1]

			name = get_pic_name(fn)
			if name:
				if pics.count(name) == 0:
					pics.append(name)
					print "[+] download: "+img[1]

					res = requests.get(img[-1])
					with open(IMG_PATH+'/['+img[0]+']'+img[1], 'w') as fd:
						fd.write(res.content)
				else:
					print "[-] skip: "+img[1]

