import pickle


def marshall(msg):
    return pickle.dumps(msg)


def unmarshall(msg):
    return pickle.loads(msg)
