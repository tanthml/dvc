import os
import shutil
import tempfile
from git import Repo
from unittest import TestCase

from dvc.system import System
from dvc.project import Project


class TestDir(TestCase):
    FOO = 'foo'
    FOO_CONTENTS = FOO
    BAR = 'bar'
    BAR_CONTENTS = BAR
    CODE = 'code.py'
    CODE_CONTENTS = 'import sys\nimport shutil\nshutil.copyfile(sys.argv[1], sys.argv[2])'

    def _pushd(self, d):
        self._saved_dir = System.realpath(os.curdir)
        os.chdir(d)

    def _popd(self):
        os.chdir(self._saved_dir)
        self._saved_dir = None

    def create(self, name, contents):
        with open(name, 'a') as f:
            f.write(contents)

    def setUp(self):
        self._root_dir = System.get_long_path(tempfile.mkdtemp())
        self._pushd(self._root_dir)
        self.create(self.FOO, self.FOO_CONTENTS)
        self.create(self.BAR, self.BAR_CONTENTS)
        self.create(self.CODE, self.CODE_CONTENTS)

    def tearDown(self):
        self._popd()
        shutil.rmtree(self._root_dir)


class TestGit(TestDir):
    def setUp(self):
        super(TestGit, self).setUp()
        self.git = Repo.init()
        self.git.index.add([self.CODE])
        self.git.index.commit('add code')


class TestDvc(TestGit):
    def setUp(self):
        super(TestDvc, self).setUp()
        self.dvc = Project.init(self._root_dir)
        self.dvc.logger.be_verbose()
