class CallBackClass(object):
    def __init__(self, a):
        self.a = a

    def __call__(self, arg):
        print 'arg: %s, a: %s' % (arg, self.a)

if __name__ == '__main__':
    cc = CallBackClass('this is a!')
    cc('This is arg!')  #arg: This is arg!, a: this is a!
    # if not __call__, will report error: TypeError: 'CallBackClass' object is not callable
