import os

workers = 4
bind = f"0.0.0.0:{os.getenv('PORT', '80')}"
timeout = 120
