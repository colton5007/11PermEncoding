from numpy import random

# Generates n random permutation pairs for testing reader/writer
def random_data(n):
	test_data = []
	k = 0
	while k < n:
		x = random.permutation([1,2,3,4,5,6,7,8,9,10,11])
		os = []
		for i in range(random.randint(1,40)):
			o = random.permutation([1,2,3,4,5,6,7,8,9,10,11])
			os.append(o)
			k += 1
		test_data.append((x,os))
	return test_data

# Converts a permutation into a hex-encoded 6 bytes payload for writing to files. 
# The format will have the first 44 bits will be the permutation encoded in hexademical and the last 4 bits will be "f" if the permutation is of type x, and "e" if the permutation is of type o.
# Since 14,15 are outside of the permutation scope, the only time e or f will appear in these paylaod is at the last place to indicate this parity data 
def serialize(sigma, x_flag):
	sigma_hex = ''.join([hex(sv)[2] for sv in sigma])
	if x_flag:
		sigma_hex += "f"
	else:
		sigma_hex += "e"
	sigma_bytes = bytes.fromhex(sigma_hex)
	return sigma_bytes

# Combines the above functions to have a demo where fake permutations are generated and written to a dummy output file
def test_write(n):
	test_data = random_data(n)
	with open("output_file", "ab+") as f:
		output_str = b''
		for x,os in test_data:
			output_str += serialize(x,True)
			for o in os:
				output_str += serialize(o,False)
		f.write(output_str)