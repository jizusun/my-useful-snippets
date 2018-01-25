import unittest

def group_same(list):
	# if (len(list) == 1 or not list):
	# 	return list
	if (len(list) >1 and (list[1] == list[0] or list[1] == list[0][:1]) ): 
		return [list[1] + list[0]] + group_same(list[2:])
	else:
		return list

class MyTest(unittest.TestCase):
    # def test_should_group_one_a(self):
    #     self.assertEqual(group_same('a'), ['a'])

    def test_should_handle_empty_list(self):
    	self.assertEqual(group_same([]), [])
    def test_should_group_two_a(self):
        self.assertEqual(group_same(['a', 'a']), ['aa'])
    def test_should_group_two_a_with_one_a(self):
        self.assertEqual(group_same(['aa', 'a']), ['aaa'])
    def test_should_group_three_a(self):
        self.assertEqual(group_same(['a', 'a', 'a']), ['aaa'])
    def test_should_group_three_a_and_leave_one_b(self):
        self.assertEqual(group_same(['a', 'a', 'a', 'b']), ['aaa', 'b'])
    def test_should_group_three_a_and_two_b(self):
        self.assertEqual(group_same(['a', 'a', 'a', 'b', 'b']), ['aaa', 'bb'])
    # def test_should_leave_b_and_group_three_a(self):
    #     self.assertEqual(group_same(['b', 'a', 'a', 'a']), ['b', 'aaa'])

if __name__ == '__main__':
    unittest.main()