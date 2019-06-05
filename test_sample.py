import requests
from collections import Callable

def test_primes():

	reqs = requests.get('http://localhost:6432/isPrime/1213')

	assert reqs.text == '1213 is prime'
	
	
def test_non_prime():

	reqs = requests.get('http://localhost:6432/isPrime/1005')

	assert reqs.text == '1005 is not prime'
	
	
def test_get_primes():

	reqs = requests.get('http://localhost:6432/primesStored')
	
	assert reqs.text.find('"1213"') > -1
	assert reqs.text.find('"1005"') == -1
