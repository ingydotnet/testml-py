class Bridge(object):

    def get_transform_function(self, name):
        function = None
        function_name = name
        for klass in TRANSFORM_CLASSES:
            try:
                module = __import__(klass, {}, {}, [function_name])
                function = getattr(module, function_name)
                break
            except (ImportError, AttributeError):
                pass
        if not function:
            raise ImportError('unable to import function: %s' % function_name)
        return function

TRANSFORM_CLASSES = [
    'testml.standard'
]
