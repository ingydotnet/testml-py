
TRANSFORM_CLASSES = [
            'testml.standard'
        ]

class Bridge(object):

    def get_transform_function(self, name):
        function = None
        function_name = 'testml_%s' % name
        for klass in TRANSFORM_CLASSES:
            try:
                module = __import__(klass, {}, {}, [function_name])
                function = getattr(module, function_name)
                break
            except (ImportError, AttributeError):
                pass
        return function
