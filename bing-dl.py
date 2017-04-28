# -*- coding: utf-8 -*-

import os
import time
import requests

IMG_PATH = '/home/cc/downloads/bing_wallpaper'

if __name__ == '__main__':
	nc  = int(time.time() * 1000)
	n   = 8
	idx = 0
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
