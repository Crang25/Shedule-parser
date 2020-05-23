from fake_useragent import UserAgent
from shutil import get_terminal_size
from json import loads
from os import system
import requests
import re

groups = {
	# 1 course
	'ктбо1-1': 1,
	'ктбо1-2': 2,
	'ктбо1-3': 3,
	'ктбо1-4': 4,
	'ктбо1-5': 5,
	'ктбо1-6': 6,
	'ктбо1-7': 7,
	'ктбо1-8': 8,
	'ктбо1-9': 9,
	'ктбо1-10': 10,
	'ктcо1-1': 11,
	'ктcо1-2': 12,
	'ктсо1-3': 13,
	'ктсо1-4': 14,
	'ктсо1-5': 15,
	'ктсо1-6': 16,

	# 2 course
	'ктбо2-1': 38,
	'ктбо2-2': 39,
	'ктбо2-3': 40,
	'ктбо2-4': 41,
	'ктбо2-5': 42,
	'ктбо2-6': 43,
	'ктбо2-7': 44,
	'ктбо2-8': 45,
	'ктбо2-9': 46,
	'ктcо2-1': 47,
	'ктcо2-2': 48,
	'ктсо2-3': 49,
	'ктсо2-4': 50,
	'ктсо2-5': 51,

	# 3 course
	'ктбо3-1': 71,
	'ктбо3-2': 72,
	'ктбо3-3': 73,
	'ктбо3-4': 74,
	'ктбо3-5': 75,
	'ктбо3-6': 76,
	'ктбо3-7': 77,
	'ктбо3-8': 78,
	'ктбо3-9': 79,
	'ктcо3-1': 80,
	'ктcо3-2': 81,
	'ктсо3-3': 82,
	'ктсо3-4': 83,
	'ктсо3-5': 84,
	'ктсо3-6': 85,

	# 4 course
	'ктбо4-1': 94,
	'ктбо4-2': 95,
	'ктбо4-3': 96,
	'ктбо4-4': 97,
	'ктбо4-5': 98,
	'ктбо4-6': 99,
	'ктбо4-7': 100,
	'ктбо4-8': 101,
	'ктбо4-10': 102,
	'ктcо4-1': 103,
	'ктбc4-2': 104,
	'ктсо4-3': 105,
	'ктсо4-4': 106,
	'ктсо4-5': 107,

	# 5 course
	'ктcо5-1': 116,
	'ктбо5-2': 117,
	'ктсо5-3': 118,
	'ктсо5-4': 119,
	'ктсо5-5': 120,
	'ктсо5-6': 121,
}
max_len = get_terminal_size((110, 30)).columns
main_url = 'http://165.22.28.187/schedule-api/?group='
day_url = '.htm&week='

def program_exit():
	input('Нажмите что-нибудь, чтобы выйти...')
	quit()

def display_week(table_ls, week):
	couple = table_ls[0][1:]
	times = table_ls[1][1:]
	
	# for i in table_ls[2:]:
	# 	for j in i[1:]:
	# 		if len(j) > max_len: max_len = len(j)	
	sepr = '.' * max_len
	star_sepr = '*' * max_len

	print(f'\n{week}, неделя')
	for i in table_ls[2:]:
		day = [j for j in i[1:]]
		print(f'\n{star_sepr}\n{i[0]}\n')
		for k in range(0, len(couple)):
			print(f"{sepr}\n{couple[k]} пара, с {times[k].split('-')[0]} до {times[k].split('-')[1]}")
			if(day[k] == ''):
				print(f'Нет\n{sepr}\n')
				continue
			print(f'{day[k]}\n{sepr}\n')
		print(star_sepr)

def get_day(table_ls, date):
	'''Функция, которая выводит расписание на день "date"
	:param: table_ls: Список со списками строк таблицы
	:type table_list: list
	:param str date: Строка - дата искомой недели
	'''

	couple = table_ls[0][1:]
	times = table_ls[1][1:]
	
	# Search for a date in the schedule
	day = [i[1:] for i in table_ls[2::] if ' '.join(i[0].split(',')[1].split(' ')[0::2]).lower() == date.lower()][0]
	
	sepr = '.' * max_len
	
	print(f'\n{date.lower()}')
	for i in range(0, len(couple)):
		print(f"\n{sepr}")
		print(f"{couple[i]} пара, с {times[i].split('-')[0]} до {times[i].split('-')[1]}")
		if(day[i]==''):
			print(f'Нет\n{sepr}')
			continue
		print(day[i])
		print(sepr)

def get_content(url):
	proxies = {
		'SOCKS5':'184.185.2.146:47659', #USA NY
		# 'SOCKS5':'96.44.183.149:55225', #USA LS
		'HTTPS':'176.115.197.118:8080' #Russia Mcw
	}

	u = UserAgent()
	#Random User_Agent
	ua = u.random

	# Url main page
	refer = 'http://165.22.28.187/schedule-api/static/index.html'
	headers = {
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
		'Connection': 'keep-alive',
		'DNT': '1',
		'Host': '165.22.28.187',
		'Referer': refer,
		'User-Agent' : str(ua)
	}

	return requests.get(url, headers=headers, proxies=proxies).content

def get_week(url, group):
	table = loads(get_content(url))
	
	# Quantity of weeks
	weeks = table['weeks']
	print('Возможные недели:\n', *weeks)
	week = int(input('\nВведите номер искомой недели: '))
	if(week not in weeks):
		print('Такой недели нет, попробуйте ещё раз')
		program_exit()
	
	table = loads(get_content(main_url+str(groups[group])+day_url+str(week)))
	#List with lists rows
	data = table['table']['table']
	display_week(data, week)

def search_day(url, group):
	jsons = loads(get_content(url))
	weeks = jsons['weeks']
	# check = '23 мая 1 сентября 6 марта'
	print("Введите день в формате: 'день месяца название месяца(в родительном падеже)\nПример: 14 апреля")
	day = input(": ")
	pattern = re.findall(r'(\d+) (января|февраля|марта|апреля|мая|июня|июля|сентября|октября|ноября|декабря)', day)
	if(len(pattern) == 0):
		print('Такой даты нет')
		quit()
	day = (pattern[0][0] + ' '+ pattern[0][1]).lower()
	
	print('Поиск даты...')
	search_group, k = groups[group], 0
	for i in weeks:
		new_url = main_url + str(search_group) + day_url + str(i)
		new_json = loads(get_content(new_url))
		new_table = new_json['table']['table'][2:]
		new_day = ''
		
		for j in new_table:
			new_day = ' '.join(j[0].split(',')[1].split(' ')[0::2])
			if(new_day == day):
				get_day(new_json['table']['table'], day)
				k = 1
				break
	if(k == 0):
		print('Ничего не найдено')
		program_exit()

def display_current_week(url):
	table = loads(get_content(url))['table']
	couple = table['table'][0][1:]
	times = table['table'][1][1:]
	week =table['week']
	
	sepr = '.' * max_len
	star_sepr = '*' * max_len

	print(f'\n{week}, неделя')
	for i in table['table'][2:]:
		day = [j for j in i[1:]]
		print(f'\n{star_sepr}\n{i[0]}\n')
		for k in range(0, len(couple)):
			print(f"{sepr}\n{couple[k]} пара, с {times[k].split('-')[0]} до {times[k].split('-')[1]}")
			if(day[k] == ''):
				print(f'Нет\n{sepr}\n')
				continue
			print(f'{day[k]}\n{sepr}\n')
		print(star_sepr)

def main():
	# Url from which a server request is generated 
	base_url = 'http://165.22.28.187/schedule-api/?query='

	system('cls')
	choose = int(input('1 - Вывести расписание на неделю\n2 -  Вывести расписание на один день\n3 - Вывести расписание на текущую неделю\n:'))
	if(choose!=1 and choose !=2 and choose!=3):
		quit()

	#Group name
	group = input('Введите имя искомой группы: ').lower()
	if(group not in groups):
		print('Такой группы нет в списке, либо ее еще не добавили в программу')
		program_exit()
	if(choose == 1):
		get_week(base_url+group, group)
		program_exit()
	elif(choose == 2):
		search_day(base_url+group, group)
		program_exit()
	else:
		display_current_week(base_url+group)
		program_exit()
if __name__=='__main__':
	main()