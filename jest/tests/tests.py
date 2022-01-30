import unittest
from ..magic import update_request_body


class JestCases(unittest.TestCase):

    def test_body_field_injection(self):
        request_body = dict(query="@original_keyword", total=1)
        feeding_list = [
            dict(original_keyword='iphone'),
            dict(original_keyword='phone')
        ]
        feeding_item = feeding_list[0]
        actual_request_body = update_request_body(request_body, feeding_item)

        expected_request_body = dict(query='iphone', total=1)
        self.assertEqual(actual_request_body, expected_request_body)

    def test_inner_body_field(self):
        request_body = dict(geo=True, data=dict(query="@original_keyword"), total="@total_count")
        feeding_list = [
            dict(original_keyword='iphone', total_count=3),
            dict(original_keyword='phone', total_count=6)
        ]
        feeding_item = feeding_list[0]
        actual_request_body = update_request_body(request_body, feeding_item)

        expected_request_body = dict(geo=True, data=dict(query="iphone"), total=3)
        self.assertEqual(actual_request_body, expected_request_body)


if __name__ == '__main__':
    unittest.main()
