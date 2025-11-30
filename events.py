# event_system.py
listeners = {}

def on(event_name, func):
    listeners.setdefault(event_name, []).append(func)

def emit(event_name, *args, **kwargs):
    for func in listeners.get(event_name, []):
        func(*args, **kwargs)