from app.ingest.ingestion import *

def test_ResultThread():
    def say(greeting, name):
        return f'{greeting} {name}!'

    t = ResultThread(target=say, args=('Hello', 'World'))
    t.start()
    t.join()

    assert t.result == 'Hello World!'
