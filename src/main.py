import os
import openai
import unicodedata
from my_utils import obj2json2file, file2json2obj

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

def response_pl_fix(call_result):
	first_choice = call_result["choices"][0]
	message = first_choice["message"] 
	message['content'] = f"{message['content']}"
	return message

def call_api(message):
	call_params = {
		"model": "gpt-3.5-turbo",
		"messages": message,
	}

	call_result = openai.ChatCompletion.create(**call_params)
	message = response_pl_fix(call_result)
	return message
		

def history_subset(history):
	if len(history) < 3:
		return history
	
	return history[-3:]


def bootstrap(history):
	system = "Hej wspólnie z użytkownikiem, zastanowicie się na architekturą kognitywną dla aplikacji"
	system_object = {"role": "system", "content": system}
	past = history_subset(history)
	message = call_api([system_object, *past])
	return message

def integrate_history(history, message):
	history.append(message)
	return history

def logic(history):
	print("+++ jakie pytanie chcesz zadac dla bootstrapa?")
	while True:
		your_msg = {"role": "user", "content": input()}
		integrate_history(history, your_msg)
		his_msg = bootstrap(history)
		integrate_history(history, his_msg)
		print(f"he said: {his_msg}")
	
def load_history():
	json_file = "fs/chats/bootstrap.json"
	history = file2json2obj(json_file)
	return history

def save_history(history):
	json_file = "fs/chats/bootstrap.json"
	obj2json2file(history, json_file)

def main():
	history = load_history()
	print("+++ app started")
	try:
		logic(history)
	except KeyboardInterrupt:
		save_history(history)
		print("+++ zapisuje historię")


# rzeczywistość odsłoniła prede mną kierunke, w którym może rozwijać się ten projekt
# Wojetek to jednak ma dobrą banię do takich rozkmin xD
# a więc tak stworzenie architektury kognitywnej npc'ta który potencjalnie może zostać streamerem na twitch tv
# streamer będzie taki jakby awatearem/wykreowaną postacią. Bęzdie można bardzo kreatywnie zdefiniowac jego background i cechy
# A ostatecznie powstanie z tego pewnego rodzaju agi, z któreym będziemy móc rozkminiac kierunek rozwoju i scenariusze streamów
main()