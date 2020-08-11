import redis
import requests
import json
import time
import os
# https: // www.tutorialspoint.com/redis/redis_lists.htm
client = redis.Redis(host="10.10.10.1",port=6379,db=0,password=os.getenv("REDIS_PASS"))

### demo the strings ###

client.set('language', 'Python')

print(client.get('language'))

client.set('language', 'Python', px=10000)
print(client.get('language'))
print(client.ttl('language'))
time.sleep(3)
print(client.ttl('language'))

client.set('language', 'Python')
print(client.expire('language', 10))
print(client.ttl('language'))
time.sleep(3)
print(client.ttl('language'))

#####           ####

#### Demo the sets ####

client.sadd('pythonlist', "value1", "value2", "value3", "value4")
client.sadd('powerlist', "value1", "value5", "value6", "value7")

#intercept of the two sets
print(client.sinter('pythonlist', 'powerlist'))
print(client.sunion('pythonlist', 'powerslist'))
print(client.scard('pythonlist'))
print(client.scard('powerlist'))


#####

#### demo the hashes

client.hset('Hero', 'Name', 'Drow Ranger')
client.hset('Hero', 'Health', '600')
client.hset('Hero', 'Mana', '200')

print(client.hgetall('Hero'))

# Hero = {
#     Name: Drow,
#     Health: 600,
#     Mana: 200
# }
