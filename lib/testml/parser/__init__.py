
import re

from grammar import Grammar

class ParserException(Exception):
    pass

class Parser(object):

    def __init__(self, receiver, start_token=None):
        self.stream = None
        self.grammar = Grammar().grammar()
        self.start_token = start_token
        self.position = 0
        self.receiver = receiver
        self.arguments = []
        self.stack = []

    def parse(self):
        self.match(self.start_token)
        if self.position < len(self.stream):
            raise ParserException("Parse document failed for some reason")

    def match(self, topic):
        _not = False
        try:
            if topic[0] == '!':
                topic = topic[1:]
                _not = True
        except (IndexError, KeyError):
            pass

        state = None
        try:
            if re.match(r'\w+$', topic):
                state = topic
                self.stack.append(state)
                topic = self.grammar[topic]
                self.callback('try', state)
        except TypeError:
            pass

        method = None
        times = '1'
        if isinstance(topic, basestring) and topic.startswith('/'):
            method = 'match_regexp'
        elif isinstance(topic, list):
            method = 'match_all'
        elif isinstance(topic, dict):
            if topic.has_key('^'):
                times = topic['^']
            if topic.has_key('='):
                topic = topic['=']
                method = 'match'
            elif topic.has_key('/'):
                topic = topic['/']
                method = 'match_one'
            elif topic.has_key('_'):
                self.throw_error(topic['_'])
            else:
                raise ParserException("Unable to match dict topic: %s" % topic)
        else:
            raise ParserException("Unknown topic type")

        position = self.position
        count = 0

        while getattr(self, method)(topic):
            count += 1
            if times == '1' or times == '?':
                break
        result = (count or times == '?' or times == '*') ^ _not
        if result:
            status = 'got'
        else:
            status = 'not'

        if state:
            self.callback(status, state)
            self.stack.pop()

        if not result:
            self.position = position

        return result

    def match_all(self, list):
        for elem in list:
            if not self.match(elem):
                return False
        return True

    def match_one(self, list):
        for elem in list:
            if self.match(elem):
                return True
        return False

    def match_regexp(self, pattern):
        regexp = self.get_regexp(pattern)

        match = regexp.search(self.stream, self.position)
        if not match:
            return False
        self.arguments = list(match.groups())
        self.position = match.end()
        return True

    def get_regexp(self, pattern):
        print 'patterna #########\n', pattern, "\n#############"
        pattern = pattern.lstrip('/').rstrip('/')

        match = re.search(r'\$(\w+)', pattern)
        while match:
            try:
                matched = match.group(1)
                replacement = self.grammar[matched]
            except KeyError:
                raise ParserException('%s not in grammar' % matched)
            replacement = replacement.lstrip('/').rstrip('/')
            pattern = re.sub(r'\$\w+', replacement, pattern, 1)
            match = re.search(r'\$(\w+)', pattern)
        print 'patternb #########\n', pattern, "\n#############"
        return re.compile(pattern)

    def callback(self, type, state):
        method = '%s_%s' % (type, state)

        try:
            getattr(self.receiver, method)(self.arguments)
        except AttributeError:
            pass

    def open(self, file):
        self.stream = open(file).read()

    def throw_error(self, message):
        line = 42
        raise ParserException('%s:%s' % (line, message))


