# Converts a 44bit hex input into a printable string
def hex_to_perm_str(sigma):
	sigma_str_array = [str(int(c, 16)) for c in sigma]
	sigma_str = "(" + ",".join(sigma_str_array) + ")"
	return sigma_str

# Converts a 44bit hex input into a length 11 array with integer entries, i.e., a permutation
def hex_to_perm_arr(sigma):
	sigma_str_array = [int(c, 16) for c in sigma]
	return sigma_str_array

# Converts the hex file into a readable ASCII file. Uses approximately 9x more storage.
def convert_file(old_file, new_file):
	with open(old_file, "rb") as old_f:
		with open(new_file, "a+") as new_f:
				cur_x = ""
				output_text = ""
				for chunk in iter(lambda : old_f.read(6), b''):
					sigma_hex = chunk.hex()
					if sigma_hex[-1] == 'f':
						cur_x = sigma_hex[:-1]
						new_f.write(output_text)
						output_text = ""
					elif sigma_hex[-1] == 'e':
						output_text += hex_to_perm_str(cur_x) + ", " + hex_to_perm_str(sigma_hex[:-1]) + "\n"

# Prints the hex file into the console (readable)
def print_file(old_file):
	with open(old_file, "rb") as old_f:
		cur_x = ""
		for chunk in iter(lambda : old_f.read(6), b''):
			sigma_hex = chunk.hex()
			if sigma_hex[-1] == 'f':
				cur_x = sigma_hex[:-1]
			elif sigma_hex[-1] == 'e':
				print(hex_to_perm_str(cur_x) + ", " + hex_to_perm_str(sigma_hex[:-1]))

# Imports a file into memory. Can specify the start and end counts for the x's. For example, you could pick all the pairs for the 1st x through the 8th x with start_x = 1, end_x = 8. If end_x = 0, then it will import the entire file. 
def import_file_n_idx(old_file, start_x=1, end_x=0):
	if start_x > end_x and end_x != 0 :
		return []
	i = 0
	output_data = []
	with open(old_file, "rb") as old_f:
		cur_x = None
		for chunk in iter(lambda : old_f.read(6), b''):
			sigma_hex = chunk.hex()
			if sigma_hex[-1] == 'f':
				cur_x = hex_to_perm_arr(sigma_hex[:-1])
				i += 1
				if i > end_x and end_x != 0:
					return output_data
			if sigma_hex[-1] == 'e':
				cur_o = hex_to_perm_arr(sigma_hex[:-1])
				output_data.append((cur_x, cur_o))
		return output_data

# Imports a file into memory. Can specify the start and end x's. For this, they should be the hex strings for the permutation.
def import_file_sigma_idx(old_file, start_x, end_x):
	start_flag = False
	end_flag = False
	output_data = []
	with open(old_file, "rb") as old_f:
		cur_x = None
		cur_x_hex = ""
		for chunk in iter(lambda : old_f.read(6), b''):
			sigma_hex = chunk.hex()
			if sigma_hex[-1] == 'f':
				cur_x_hex = sigma_hex[:-1]
				cur_x = hex_to_perm_arr(cur_x_hex)
				if end_flag:
					return output_data
				if cur_x_hex == end_x:
					end_flag = True
				if cur_x_hex == start_x:
					start_flag = True
			if sigma_hex[-1] == 'e':
				cur_o = hex_to_perm_arr(sigma_hex[:-1])
				if start_flag:
					output_data.append((cur_x, cur_o))
		return output_data

convert_file("output_file", "parsed_file")