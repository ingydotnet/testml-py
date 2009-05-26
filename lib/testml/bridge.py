# This is bogus ingy code...
class Bridge(object):
    def __init__(self):
        pass

    def transform_classes(self):
        return [
            'testml.standard'
        ]

    def get_transform_function(self, name):
        classes = self.transform_classes()
        function = None
        for klass in classes
            import klass
