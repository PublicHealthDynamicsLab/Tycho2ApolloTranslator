'''
Created on Jun 27, 2016

@author: kjm84
'''

class DataSource(object):
   
    data = [ b"<roo", b"t><", b"a/", b"><", b"/root>" ]

    def __init__(self):
        '''
        Constructor
        '''
        
    def read(self, requested_size):
        try:
            return self.data.pop(0)
        except IndexError:
            return b''

class ParserTarget:
    events = []
    close_count = 0
    def start(self, tag, attrib):
        self.events.append(("start", tag, attrib))
    def close(self):
        events, self.events = self.events, []
        self.close_count += 1
        return events