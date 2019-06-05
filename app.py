import time
import ast
import redis
from flask import Flask, jsonify


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
	retries = 5
	while True:
		try:
			return cache.incr('hits')
		except redis.exceptions.ConnectionError as exc:
			if retries == 0:
				raise exc
			retries -= 1
			time.sleep(0.5)

def prime_check(prime_no):
	if prime_no > 1:
		i = 2
		while i*i <= prime_no:
			if (prime_no % i) == 0:
				return False
			i += 1
	else:
		return False
	return True
				

@app.route('/primesStored')
def get_all():
	primes = []
	stored_primes = cache.hgetall("prime_number")
	
	for key in stored_primes.keys():
		primes.append(key.decode('utf-8'))

	return jsonify(primes)

@app.route('/isPrime/<int:prime_no>')
def is_prime(prime_no):

	if cache.hexists("prime_number", prime_no):
		return '%d is prime' % prime_no

	if not prime_check(prime_no):
		return '%d is not prime' % prime_no
	
	cache.hset("prime_number", prime_no, prime_no)
	return '%d is prime' % prime_no

@app.route('/clear')
def clear():
	stored_primes = cache.hgetall("prime_number")
	for key in stored_primes:
		cache.delete(key)
	return 'Done'


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
