from types import ClassType
import unittest
import cli


class TestWorkers(unittest.TestCase):

    def test_class_wrong_name(self):
        module_list = dir(cli.workers)

        for obj_str in module_list:
            obj = getattr(cli.workers, obj_str)

            if isinstance(obj, ClassType):
                self.assertTrue(
                    obj_str.endswith('Worker'),
                    msg="Class "+obj_str+" does not end with 'Worker'"
                    )

    def test_classes_have_all_attrs(self):
        w_list = [getattr(cli.workers, x) for x in dir(cli.workers) if x.endswith('Worker')]

        for worker_class in w_list:
            self.assertTrue(
                hasattr(worker_class, 'NAME'),
                msg="Class "+worker_class.__name__+" is missing NAME"
                )
            self.assertTrue(
                hasattr(worker_class, 'NICENAME'),
                msg="Class "+worker_class.__name__+" is missing NICENAME"
                )
            self.assertTrue(
                hasattr(worker_class, 'REQUEST'),
                msg="Class "+worker_class.__name__+" is missing REQUEST"
                )
            self.assertTrue(
                hasattr(worker_class, 'is_error'),
                msg="Class "+worker_class.__name__+" is missing is_error"
                )
            self.assertTrue(
                hasattr(worker_class, 'get_error'),
                msg="Class "+worker_class.__name__+" is missing get_error"
                )
            self.assertTrue(
                hasattr(worker_class, 'print_response'),
                msg="Class "+worker_class.__name__+" is missing print_response"
                )

    def test_requests_in_valid_format(self):
        w_list = [getattr(cli.workers, x) for x in dir(cli.workers) if x.endswith('Worker')]

        # Defined seperately so it can be recursive
        def dict_of_types(d):
            for key in d:
                if isinstance(d[key], dict):
                    if not dict_of_types(d[key]):
                        return False
                elif not isinstance(d[key], type):
                    return False
            return True

        for worker_class in w_list:
            self.assertTrue(
                dict_of_types(worker_class.REQUEST),
                msg=worker_class.__name__+'.REQUEST must be a dict of types'
                )


if __name__ == '__main__':
    unittest.main()
