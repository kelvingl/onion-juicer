PROJECT ?= onion_juicer
TOR_PORT ?= 9150

run:
	- torsocks -P $(TOR_PORT) python main.py
