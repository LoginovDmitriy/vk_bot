import requests
import json
import pymysql.cursors  
import os

token = '4b32f8e7eb6e896617c28649b7b32d0adbc1d421ea6b3d47f8a41b45cf1c7ad6d30407dad4cf72f1500b'
def write_json(data):
	with open('r.json', 'w', encoding='utf-8') as file:
		json.dump(data, file, indent=2, ensure_ascii=False)

def get_upload_server():
	r = requests.get('https://api.vk.com/method/photos.getUploadServer', params={'access_token': token,
																		   			 'album_id':272765578,
																		   			 'group_id':193176076,
																		  			 'v':'5.103'}).json()
	write_json(r)
	return r['response']['upload_url']

def get_market_upload_server():
	r = requests.get('https://api.vk.com/method/photos.getMarketUploadServer', params={'access_token': token,
																		   			 'main_photo':1,
																		   			 'group_id':193176076,
																		  			 'v':'5.103'}).json()
	write_json(r)
	return r['response']['upload_url']



# def add_market():
# 	r = requests.get('https://api.vk.com/method/photos.getUploadServer', params={'access_token': token,
# 																		   			 'owner_id':-272765578,
# 																		   			 'name':name,
# 																		   			 'description': caption,
# 																		   			 'category_id':500,
# 																		   			 'price':price,
# 																		   			 'main_photo_id':
# 																		  			 'v':'5.103'}).json()
	# write_json(r)
	# return r['response']['upload_url']


def main():
	
	connection = pymysql.connect(host='mysql.9967724406.myjino.ru',
							user='047077889_eci',
							password='*********',
							db='9967724406_eci',
							charset='utf8mb4',
							cursorclass=pymysql.cursors.DictCursor)
	
	print ("connect successful!!")

	with connection.cursor() as cursor:
		sql = "SELECT * FROM flats WHERE deadline LIKE 'Дом сдан' OR deadline LIKE 'Заселен' OR deadline LIKE 'Собств-ть'" #jk='GreenЛандия-2'
		cursor.execute(sql)
		c = cursor.fetchall()

	upload_url = get_market_upload_server()
	for i in range(3): #len(c)):
		ids = c[i]['ids']
		jk = c[i]['jk'].strip()
		price = str(c[i]['price'])
		flat_type = c[i]['room']

		if flat_type == '1 к' or flat_type == '2Е':
			rooms = '1'
		elif flat_type == '2 к' or flat_type == '3Е':
			rooms = '2'
		elif flat_type == '3 к' or flat_type == '4Е':
			rooms = '3'		
		elif flat_type == '4 к':
			rooms = '4'
		else:
			rooms = None
		if flat_type != 'Ст.':
			room_d = flat_type + '-комнатная квартира.'
		else:
			room_d = 'квартира-студия'

		caption = 'Продается ' + room_d + ' в ЖК ' +jk+ '. Дом полностью построен и сдан. Возможна продажа в ипотеку. Стоимость - ' + price + ' рублей. #' + jk + ', #переуступки, #новостройка, #ипотека, #сэтлсити, #ЛСР, #сбербанк, #домклик, #маткапитал'
		

		file = {'file': open('c:\\Python37\\ECN\\'+str(ids)+'\\2.jpg', 'rb')}
		ur = requests.post(upload_url, files=file).json()
		write_json(ur)
		res = requests.get('https://api.vk.com/method/photos.saveMarketPhoto', params={'access_token':token,
																			   'group_id': 193176076,
																			   'server': ur['server'],
																			   'photo': ur['photo'],
																			   'hash':ur['hash'],
																			   'v':'5.102'})
		if ' ' in price:
			print('Yes')
		else:
			print('No')
		write_json(res.json())
		name = room_d + ' в ЖК ' +jk
		r = requests.get('https://api.vk.com/method/market.add', params={'access_token': token,
																			   			 'owner_id':-272765578,
																			   			 'name':name,
																			   			 'description': caption,
																			   			 'category_id':500,
																			   			 'price':float(price),
																			   			 'main_photo_id':res.json()['response'][0]['id'],
																			  			 'v':'5.103'})
		write_json(r.json())	

		# result = requests.get('https://api.vk.com/method/photos.save', params={'access_token':token,
		# 																	   'album_id': 272765578,
		# 																	   # 'user_id': 482980,
		# 																	   'group_id': 193176076,
		# 																	   'server': ur['server'],
		# 																	   'photos_list': ur['photos_list'],
		# 																	   'hash':ur['hash'],
		# 																	   'caption': caption,
		# 																	   'v':'5.102'})
	# print(result)

	# post = requests.get('https://api.vk.com/method/wall.post', params={'access_token':token,
	# 																   'owner_id':-193176076,
	# 																   'from_group':1,
	# 																   'message':'Продается квартир по переуступке.',
	# 																   'attachments':'photo-193176076_457239021',
	# 																   'v':'5.103'})
	# write_json(post.json())
	# r = requests.get('https://api.vk.com/method/wall.post', params={'access_token': token,
	# 																	   'owner_id':-193176076,
	# 																	   'from_group':1, 
	# 																	   'friends_only': 0,
	# 																	   'message': 'Продается однокомнатная квартира по переуступке.',
	# 																	   'v':'5.102'})
	# write_json(r.json())

if __name__ == '__main__':
	main()