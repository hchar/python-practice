import requests
import re
import os,sys
import json
import argparse


class get_qmkg(object):
	def __init__(self,address,uid):
		self.url = 'http://node.kg.qq.com/play?s='
		self.listurl = 'http://node.kg.qq.com/cgi/fcgi-bin/kg_ugc_get_homepage?jsonpCallback=callback_0&type=get_ugc&num=8&share_uid=' + str(uid) + '&start='
		self.audionames = []
		self.raw_urls = []
		self.audiourls = []
		self.address = address + '/qmkg/'

	def get_html(self,url):
		response = requests.get(url)
		if response.status_code == 200:
			return response
		else:
			print(url + 'request failed')
			return None
'''
爬取list表单中的歌曲标题以及单首歌曲页面
'''
	def parse_response(self,response):
		pattern = 'callback_0\((.*)\)'
		response = re.findall(pattern,response)[0]
		response = json.loads(response)
		if response['data']['ugclist']:
			for item in response['data']['ugclist']:
				self.raw_urls.append(self.url + item['shareid'])
				self.audionames.append(item['title'])
'''
爬取单首歌曲中音频文件的url
'''
	def parse_stream(self):		
		for one_url in self.raw_urls:
			html = self.get_html(one_url).text

			pattern = 'playurl":"(.*?)","playurl_video'		
			url = re.findall(pattern,html)[0]
			self.audiourls.append(url)

	def file_path(self):
		for num in range(0,len(self.audiourls)):
			with open(self.address + self.audionames[num] + '.mp3','wb') as f:
				content = self.get_html(self.audiourls[num]).content
				f.write(content)
				sys.stdout.write('正在下载:' + str(num) + '/' + str(len(self.audiourls)) +'首歌曲：' + self.audionames[num] + '\n')
				sys.stdout.flush()
			
			'''
			file_path = self.address + 'pictures/' + str(self.picturenames[num])
			content = self.get_html(self.pictures[num]).content
			with open(file_path + '.jpg','wb') as f:
				f.write(content)
			'''
		print('finished!')
		print('path =  + self.address')
	
	def main(self):	
		if not os.path.exists(self.address):
			os.mkdir(self.address)
		else:
			print('dir is exist!')
		
		for i in range(1,10):
			response = self.get_html(self.listurl + str(i))
			self.parse_response(response.text)
		self.parse_stream()
		self.file_path()
		
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-u','--uid',required = True,help = ('input the uid that the people''s K歌id '))
	parser.add_argument('-d','--dir',required = True,help = ('input the path that you want to save'))
	args = parser.parse_args()

	get_qmkg = get_qmkg(args.dir,args.uid)

	get_qmkg.main()
