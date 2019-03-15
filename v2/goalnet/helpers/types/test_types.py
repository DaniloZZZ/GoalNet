import unittest
from .Message import *



class TestTypes(unittest.TestCase):
    def test_messages(self):
        create = MessageAction.from_str('create')
        self.assertEqual(create, MessageAction.CREATE)
        message = Message(action=MessageAction.CREATE)
        self.assertEqual(message.action, create)
        message = Message.from_dict({
            'action':'create'
        })
        self.assertEqual(message.action, create)


if __name__=='__main__':
    unittest.main()



