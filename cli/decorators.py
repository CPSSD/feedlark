def standard_error(in_class):
    @staticmethod
    def is_error(response):
        return 'status' not in response or response['status'] == 'error'

    @staticmethod
    def get_error(response):
        return response['description']

    in_class.is_error = is_error
    in_class.get_error = get_error
    return in_class


def standard_response(in_class):
    @classmethod
    def print_response(cls, response, indent=4):
        for key in response:
            if type(response[key]) == dict:
                print ' '*indent + str(key) + ': '
                cls.print_dict(response[key], indent + 4)
                continue

            print ' '*indent + str(key) + ': ' + str(response[key])

    in_class.print_response = print_response
    return in_class
