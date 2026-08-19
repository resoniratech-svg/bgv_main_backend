import os

port = os.getenv("PORT")
bind_list = ["0.0.0.0:80", "0.0.0.0:5000", "0.0.0.0:8000"]
if port and f"0.0.0.0:{port}" not in bind_list:
    bind_list.append(f"0.0.0.0:{port}")

bind = bind_list
workers = 2
timeout = 120
