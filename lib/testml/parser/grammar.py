class Grammar(object):
    def grammar(self):
        return  {'comment': '/$HASH$line/', 'transform_name': {'/': ['user_transform', 'core_transform']}, 'BACK': '\\', 'EOL': '\\r?\\n', 'blank_line': '/$SPACE*$EOL/', 'meta_statement': '/%($meta_keyword):$SPACE+($meta_value)(?:$SPACE+$comment|$EOL)/', 'double_quoted_string': '/(?:$DOUBLE(([^$BREAK$BACK$DOUBLE]|$BACK$DOUBLE|$BACK$BACK|$BACK$ESCAPE)*?)$DOUBLE)/', 'DOT': '\\.', 'WORD': '\\w', 'test_section': [{'/': ['ws', 'test_statement'], '^': '*'}], 'point_phrase': '/($NON_BREAK*)/', 'assertion_name': '/EQ/', 'assertion_operator': '/(==)/', 'block_label': ['/([^$SPACES$BREAK]($NON_BREAK*[^SPACES$BREAK])?)/'], 'HASH': '#', 'meta_section': ['/(?:$comment|$blank_line)*/', {'/': ['meta_testml_statement', {'_': 'No TestML meta directive found'}]}, {'/': ['meta_statement', 'comment', 'blank_line'], '^': '*'}], 'lines_point': ['/$point_marker$SPACE+/', 'user_point_name', '/$SPACE*$EOL/', 'point_lines'], 'ESCAPE': '[0nt]', 'line': '/$NON_BREAK*$EOL/', 'user_point_name': '/($LOWER$WORD*)/', 'quoted_string': {'/': ['single_quoted_string', 'double_quoted_string']}, 'meta_value': '/(?:$single_quoted_string|$double_quoted_string|$unquoted_string)/', 'UPPER': '[A-Z]', 'block_point': {'/': ['lines_point', 'phrase_point']}, 'DOUBLE': '"', 'call_indicator': '/(?:$DOT$ws*|$ws*$DOT)/', 'assertion_operation': ['/$ws+/', 'assertion_operator', '/$ws+/', 'test_expression'], 'BREAK': '\\n', 'assertion_expression': {'/': ['assertion_operation', 'assertion_call']}, 'test_expression': ['sub_expression', {'/': [['!assertion_call_start', 'call_indicator', 'sub_expression']], '^': '*'}], 'core_meta_keyword': '/(?:Title|Data|Plan|BlockMarker|PointMarker)/', 'single_quoted_string': '/(?:$SINGLE(([^$BREAK$BACK$SINGLE]|$BACK$SINGLE|$BACK$BACK)*?)$SINGLE)/', 'LOWER': '[a-z]', 'constant': '/($UPPER$WORD*)/', 'test_statement': ['test_expression', {'=': 'assertion_expression', '^': '?'}, {'/': ['/;/', {'_': 'You seem to be missing a semicolon'}]}], 'data_block': ['block_header', {'/': ['blank_line', 'comment'], '^': '*'}, {'=': 'block_point', '^': '*'}], 'argument': ['sub_expression'], 'SINGLE': "'", 'SPACES': '\\ \\t', 'point_lines': '/((?:(?!$block_marker|$point_marker)$line)*)/', 'user_meta_keyword': '/$LOWER$WORD*/', 'assertion_call_start': ['/$call_indicator$assertion_name\\($ws*/'], 'sub_expression': [{'/': ['transform_call', 'data_point', 'quoted_string', 'constant']}], 'meta_testml_statement': '/%TestML:$SPACE+($testml_version)(?:$SPACE+$comment|$EOL)/', 'meta_keyword': '/(?:$core_meta_keyword|$user_meta_keyword)/', 'argument_list': {'=': ['argument', {'=': ['/$ws*,$ws*/', 'argument'], '^': '*'}], '^': '?'}, 'NON_BREAK': '.', 'phrase_point': ['/$point_marker$SPACE+/', 'user_point_name', '/:$SPACE/', 'point_phrase', '/$EOL/', '/(?:$comment|$blank_line)*/'], 'document': ['meta_section', 'test_section', {'/': ['data_section'], '^': '?'}], 'SPACE': '[\\ \\t]', 'testml_version': '/($DIGIT$DOT$DIGIT+)/', 'DOLLAR': '\\$', 'transform_call': ['transform_name', '/\\($ws*/', 'argument_list', '/$ws*\\)/'], 'block_marker': '/===/', 'point_marker': '/---/', 'ws': '/(?:$SPACE|$EOL|$comment)/', 'core_transform': '/($UPPER$WORD*)/', 'data': {'=': 'data_block', '^': '*'}, 'assertion_call': ['assertion_call_start', 'test_expression', '/$ws*\\)/'], 'DIGIT': '[0-9]', 'block_header': ['block_marker', {'=': ['/$SPACE+/', 'block_label'], '^': '?'}, '/$SPACE*$EOL/'], 'data_section': '/($block_marker(?:$SPACE|$EOL)$ANY+|\\Z)/', 'data_point': '/($DOLLAR$LOWER$WORD*)/', 'ALPHANUM': '[A-Za-z0-9]', 'unquoted_string': '/[^$SPACES$BREAK$HASH](?:[^$BREAK$HASH]*[^$SPACES$BREAK$HASH])?/', 'ANY': '[\\s\\S]', 'user_transform': '/($LOWER$WORD*)/'}
