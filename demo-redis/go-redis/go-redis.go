package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/go-redis/redis/v8"
	"github.com/joho/godotenv"
)

func goDotEnvVariable(key string) string {
	// load .env file
	err := godotenv.Load(".env")
	if err != nil {
		log.Fatalf("Error loading .env file")
	}
	return os.Getenv(key)
}

var ctx = context.Background()

/*
redis.Bool() – converts a single reply to a bool
redis.Bytes() – converts a single reply to a byte slice ([]byte)
redis.Float64() – converts a single reply to a float64
redis.Int() – converts a single reply to a int
redis.String() – converts a single reply to a string
redis.Values() – converts an array reply to a slice of individual replies
redis.Strings() – converts an array reply to a slice of strings ([]string)
redis.ByteSlices() – converts an array reply to a slice of byte slices ([][]byte)
redis.StringMap() – converts an array of strings (alternating key, value) into a map[string]string. Useful for HGETALL etc
*/

// ExampleNewClient sets up the client
func ExampleNewClient() {
	client := redis.NewClient(&redis.Options{
		Addr:     "10.10.10.1:6379",
		Password: goDotEnvVariable("REDIS"), // get password from .env
		DB:       1,                         // use DB 1
	})

	pong, err := client.Ping(ctx).Result()
	fmt.Println(pong, err)
	// Output: PONG <nil>
}

// ExampleClient sets up the client object
func ExampleClient() {
	client := redis.NewClient(&redis.Options{
		Addr:     "10.10.10.1:6379",
		Password: goDotEnvVariable("REDIS"), // no password set
		DB:       1,                         // use DB 1
	})
	err := client.Set(ctx, "key", "value", 0).Err() // 0 since it does not expire
	if err != nil {
		panic(err)
	}

	val, err := client.Get(ctx, "key").Result()
	if err != nil {
		panic(err)
	}
	fmt.Println("key", val)

	val2, err := client.Get(ctx, "key2").Result()
	if err == redis.Nil {
		fmt.Println("key2 does not exist")
	} else if err != nil {
		panic(err)
	} else {
		fmt.Println("key2", val2)
	}
	// Output: key value
	// key2 does not exist
}

// OtherExamples is a list of the same examples from the other demos
func OtherExamples() {
	client := redis.NewClient(&redis.Options{
		Addr:     "10.10.10.1:6379",
		Password: goDotEnvVariable("REDIS"), // no password set
		DB:       1,                         // use DB 1
	})

	// Demo the strings

	_ = client.Set(ctx, "language", "Go", 0) // does not expire

	val, err := client.Get(ctx, "language").Result()
	if err != nil {
		panic(err)
	}
	fmt.Println("language", val)

	err = client.Set(ctx, "language", "Go", 1000000).Err() // I dont know how long til this expires tbh
	if err != nil {
		panic(err)
	}

	// Demo the sets

	err = client.SAdd(ctx, "goList", "value1", "value2", "value3", "value4").Err()
	if err != nil {
		panic(err)
	}

	err = client.SAdd(ctx, "powerList", "value1", "value5", "value6", "value7").Err()
	if err != nil {
		panic(err)
	}

	// Intercept of the two sets
	results := client.SInter(ctx, "goList", "powerList")
	fmt.Println(results)

	results = client.SUnion(ctx, "goList", "powerList")
	fmt.Println(results)

	resul := client.SCard(ctx, "goList")
	fmt.Println(resul)

	resul = client.SCard(ctx, "powerList")

	// Demo the hashes

	err = client.HSet(ctx, "Hero", "Name", "Draw Ranger").Err()
	if err != nil {
		panic(err)
	}

	err = client.HSet(ctx, "Hero", "Health", "600").Err()
	if err != nil {
		panic(err)
	}

	err = client.HSet(ctx, "Hero", "Mana", "200").Err()
	if err != nil {
		panic(err)
	}

	// client.hgetall('Hero').then((res) => console.log(res));

	hash := client.HGetAll(ctx, "Hero")
	fmt.Println(hash)

	// Hero = {
	//     Name: 'Draw Ranger',
	//     Health: 600,
	//     Mana, 200
	// }
}

func main() {
	ExampleNewClient()
	ExampleClient()
	OtherExamples()
}
