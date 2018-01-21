# SimplerMock
Straight to the fun

SimplerMock is a short class that helps writing mocking for python quicker and easier.

I simply got fed-up about how tedious and slow it was to write simple tests for python software.

## Example

The class is used by overloading the tested module

So suppose we want to mock the api of the famous cache server [redis](http://redis-py.readthedocs.io/en/latest/)
:

```python

import redis

class RedisMock(SimplerMock):
    def __init__(self, host='', port='', db=0, password=''):
        self.d = {}
        super().__init__()

    def __new__(cls, host='', port='', db=0, password=''):
        return super(RedisMock, cls).__new__(cls)

    def lpush(self, k, v):
        if self.d.get(k) is None:
            self.d[k] = []
        self.d[k].append(str(v).encode('utf-8'))

    def set(self, k, v):
        self.d[k] = str(v).encode('utf-8')

    def get(self, k):
        return self.d.get(k) 

    def rpoplpush(self, k1, k2):
        try:
            v = self.d[k1].pop()
        except:
            return None
        if self.d.get(k2) is None:
           self.d[k2] = []
        self.d[k2] = [v] + self.d[k2]
        return v 

    def lrem(self, channel, val):
        self.d[channel].remove(val)

    def lrange(self, k, x, y):
        try:
            if y == -1:
                return self.d[k][x:]
            elif x == -1:
                return self.d[k][:y]
            else:
                return self.d[k][x:y]
        except:
            return None
            
# we change the object at redis.StrictRedis with our newely created mock
redis.StrictRedis = RedisMock

# we can then proceed with our tests

class BrokerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
         '''Usualy you want to create your context here.'''
        cls.redis = RedisMock()
        cls.redis.lpush('channels', 'test')
        cls.redis.aMethod()  # notice this method hasn't been writen in our mock
        super(BrokerTests, cls).setUpClass()

    def tearDown(self):
        '''
            Don't forget to clean it up properly, otherwhise
            you will corrupt your tests with data left from
            previous tests.
        '''
        # this can be done calling .reset() on the mock
        self.redis.reset()

    def test_0_has_been_called(self):
        '''
            All called methoed will succeed and will be saved in attrs attribute.
            They can be checked trough was_called method wich returns a Boolean.
        '''
        assert self.mc.was_called('ASimplerMock.aMethod')

    def test_1_existing(self):
        '''Should test existing methods.'''
        assert self.mc.was_called('ASimplerMock.lpush')

    def test_2_unkown(self):
        '''Should test unknown methods.'''
        assert self.mc.was_called('ASimplerMock.unknownMethod') != True

    def test_3_other_class(self):
        '''Should test unicity from other class.'''
        assert self.mc.was_called('BSimplerMock.bMethod')
        assert not self.mc.was_called('ASimplerMock.bMethod')

    def test_4_other_object(self):
        '''Should test same class share entity.'''
        assert self.mc.was_called('ASimplerMock.anotherMethod')

    def test_5_status(self):
        '''
           Test order is alphabetical / numeral, Numeroting them helps
           knowing which method is called in which order more clearly.
        '''
        self.assertEqual(self.redis.get('channels'), [])

```

## Install
```pip3.6 install simplermock```
