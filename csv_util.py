import unittest

def split_list(list, limit_bytes):
    begin_index = 0
    end_index = 0
    new_list = []
    while begin_index < len(list):
	    new_elem = ""
	    while end_index < len(list) and len(new_elem) <= limit_bytes :
	        print("nested while", new_elem, end_index, list[end_index])
	        new_elem += list[end_index]
	        end_index += 1
	    # great, now we have new_elem
	    if not(begin_index == len(list)-1 and end_index == len(list)):
	    	end_index -= 1
	    new_elem =  "".join(list[begin_index:end_index])
	    new_list += [new_elem]
	    print(new_elem, len(new_elem), begin_index, end_index)
	    begin_index = end_index
	    end_index = begin_index
    return new_list


class MyTest(unittest.TestCase):
    # def test_should_group_two_a(self):
    #     self.assertEqual(split_list(['aa|', 'bb|', 'b|'], 7), ['aa|bb|', 'b|'])
    # def test_larger_limit(self):
    #     self.assertEqual(split_list(['aa|', 'bb|', 'cc|', 'dd|', 'e|'], 7), ['aa|bb|', 'cc|dd|', 'e|'])
    # def test_equal_limit(self):
    #     self.assertEqual(split_list(['aa|', 'bb|', 'cc|', 'dd|', 'e|'], 6), ['aa|bb|', 'cc|dd|', 'e|'])
    def test_equal_limit_2(self):
        self.assertEqual(split_list(['aa|', 'bb|', 'cc|', 'dd|', 'e|'], 9), ['aa|bb|cc|', 'dd|e|'])

if __name__ == '__main__':
    unittest.main()