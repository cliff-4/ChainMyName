import json
def hf_api_keys():
	with open("tokens.json", "r") as f:
		token_data = json.load(f)

	return token_data

if __name__ == "__main__":
	print(hf_api_keys())