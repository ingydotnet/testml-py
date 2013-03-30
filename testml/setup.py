import yaml
import re
import glob
import os.path
import shutil

DEFAULT_TESTML_CONF = './test/testml.yaml'

class Setup():
    def setup(self, testml_conf = DEFAULT_TESTML_CONF):
        if not os.path.exists(testml_conf):
            raise Exception("TestML conf file '%s' not found" % testml_conf)
        if not re.match('.*\.ya?ml$', testml_conf):
            raise Exception("TestML conf file must be .yaml")
        base = os.path.dirname(testml_conf)
        conf = yaml.load(open(testml_conf))
        source = conf.get('source_testml_dir')
        if not source:
            raise Exception("expected 'source_testml_dir' key in '%s'" % testml_conf)
        target = conf.get('local_testml_dir')
        if not target:
            raise Exception("expected 'local_testml_dir' key in '%s'" % testml_conf)
        tests = conf.get('test_file_dir') or '.'

        # XXX best guess for simulating Ruby's File.expand_path was:
        #  source = os.path.abspath(os.path.relpath(source, os.path.abspath(base)))
        # But no. So we're forcing the leading '../' out manually:
        source = source[3:]

        source = os.path.abspath(source)

        # XXX same issue as above:
        target = os.path.abspath(base+'/'+target)

        # XXX same issue as above:
        tests = os.path.abspath(base+'/'+tests)

        if not os.path.exists(source):
            raise Exception("source_testml_dir, '%s', not found" % source)
        if not os.path.exists(target):
            os.mkdir(target)
        if not os.path.exists(tests):
            os.mkdir(tests)
        template = conf['test_file_template']
        skip = conf.get('exclude_testml_files') or []
        files = conf.get('include_testml_files')
        if not files:
            files = glob.glob(source+'/*.tml')
        for file_ in sorted(files):
            filename = re.sub(r'.*/', '', file_)
            if filename in skip:
                continue
            s = source+'/'+filename
            t = target+'/'+filename
            if not os.path.exists(t) or open(s).read() != open(t).read():
                print("Copying '%s' to '%s'" % (s, t))
                shutil.copyfile(s, t)
            if template:
                test = re.sub(r'.tml$', '.py', filename)
                if conf.get('test_file_prefix'):
                    test = conf('test_file_prefix') + test
                test = tests+'/'+test
                hash = {
                    'file': 'testml/'+filename, # XXX another shortcut
                }
                code = template % hash
                if not os.path.exists(test) or code != open(test).read():
                    action = 'Updating' if os.path.exists(test) else 'Creating'
                    print("%s test file '%s'" % (action, filename))
                    open(test, 'w').write(code)

    # def rel path, base='.'
    #     base = Pathname.new(File.absolute_path(base))
    #     Pathname.new(path).relative_path_from(base).to_s

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 1:
        Setup().setup(sys.argv[1])
    else:
        Setup().setup()
