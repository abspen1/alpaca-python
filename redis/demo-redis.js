var Redis = require('ioredis')

const dotenv = require('dotenv')
dotenv.config()
const redisPass = process.env.REDIS

var client = new Redis({
    port: 6379,          // Redis port
    host: '10.10.10.1',   // Redis host
    password: redisPass,
    db: 1,
})


// ioredis supports all Redis commands:
client.set("foo", "bar"); // returns promise which resolves to string, "OK"

// the format is: redis[SOME_REDIS_COMMAND_IN_LOWERCASE](ARGUMENTS_ARE_JOINED_INTO_COMMAND_STRING)
// the js: ` client.set("mykey", "Hello") ` is equivalent to the cli: ` redis> SET mykey "Hello" `

// ioredis supports the node.js callback style
client.get("foo", function (err, result) {
    if (err) {
        console.error(err);
    } else {
        console.log(result); // Promise resolves to "bar"
    }
});

// Or ioredis returns a promise if the last argument isn't a function
client.get("foo").then(function (result) {
    console.log(result);
});

client.del("foo");

// Arguments to commands are flattened, so the following are the same:
client.sadd("set", 1, 3, 5, 7);
client.sadd("set", [1, 3, 5, 7]);
client.spop("set").then((res) => console.log(res)); // Promise resolves random value from the set

// Most responses are strings, or arrays of strings
client.zadd("sortedSet", 1, "one", 2, "dos", 4, "quatro", 3, "three");
client.zrange("sortedSet", 0, 2, "WITHSCORES").then((res) => console.log(res));
// Promise resolves to ["one", "1", "dos", "2", "three", "3"] as if the command was ` redis> ZRANGE sortedSet 0 2 WITHSCORES `

// Some responses have transformers to JS values
client.hset("myhash", "field1", "Hello");
client.hgetall("myhash").then((res) => console.log(res)); // Promise resolves to Object {field1: "Hello"} rather than a string, or array of strings

// All arguments are passed directly to the redis server:
client.set("key", 100, "EX", 10); // set's key to value 100 and expires it after 10 seconds

// Change the server configuration
// client.config("set", "notify-keyspace-events", "KEA");


// Demo the strings

client.set('language', 'JavaScript')

client.get('language').then(function (result) {
    console.log(result);
});

client.set("language", "JavaScript", "EX", 10); // set's key to value JavaScript and expires it after 10 seconds

// Demo the sets 

client.sadd('jslist', "value1", "value2", "value3", "value4")
client.sadd('powerlist', "value1", "value5", "value6", "value7")

// Intercept of the two sets
client.sinter('jslist', 'powerlist').then((res) => console.log(res));
client.sunion('jslist', 'powerslist').then((res) => console.log(res));
client.scard('jslist').then((res) => console.log(res));
client.scard('powerlist').then((res) => console.log(res));



// Demo the hashes

client.hset('Hero', 'Name', 'Drow Ranger')
client.hset('Hero', 'Health', '600')
client.hset('Hero', 'Mana', '200')

client.hgetall('Hero').then((res) => console.log(res));

// Hero = {
//     Name: 'Draw Ranger',
//     Health: 600, 
//     Mana, 200
// }
