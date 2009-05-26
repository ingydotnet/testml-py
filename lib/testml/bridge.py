
class Bridge(object):

    def transform_classes(self):
        return [
            'testml.standard'
        ]

    def get_transform_function(self, name):
        classes = self.transform_classes()
        function = None
        function_name = 'testml_%s' % name
        for klass in classes:
            try:
                module = __import__(klass, {}, {}, [function_name])
                function = getattr(module, function_name)
                break
            except ImportError:
                pass
        return function
