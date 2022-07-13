from errorlistener import ErrorListener


PACKAGE_NAME = "org.telegram.messenger"

if __name__ == '__main__':
    listener = ErrorListener(PACKAGE_NAME,30)
    logs =  listener.listen()
    if logs:
        print(logs)
    else:
        print('No errors raised within timeout')
