from datetime import datetime

def time(request):
    return {
        'now': datetime.now(),
        'utcnow': datetime.utcnow(),
    }
