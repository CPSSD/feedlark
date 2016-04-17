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
                    msg="All classes in workers.py must end with 'Worker'"
                    )

    def test_classes_have_all_attrs(self):
        w_list = [getattr(cli.workers, x) for x in dir(cli.workers) if x.endswith('Worker')]

        for worker_class in w_list:
            self.assertTrue(hasattr(worker_class, 'NAME'))
            self.assertTrue(hasattr(worker_class, 'NICENAME'))
            self.assertTrue(hasattr(worker_class, 'REQUEST'))
            self.assertTrue(hasattr(worker_class, 'is_error'))
            self.assertTrue(hasattr(worker_class, 'get_error'))
            self.assertTrue(hasattr(worker_class, 'print_response'))

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
            self.assertTrue(dict_of_types(worker_class.REQUEST))


if __name__ == '__main__':
    unittest.main()
