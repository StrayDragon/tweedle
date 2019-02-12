import pytest


@pytest.fixture
def blog_fixture():
    pass


def test_blog_publish():
    assert Blog.publish() == True


class Blog(object):
    @classmethod
    def publish(cls):
        # import os
        # os.system('hexo clean')
        # os.system('hexo g -d')
        # os.system('hexo clean')
        print('[EXEC] hexo clean ; hexo g -d; hexo clean')
        return False

    @classmethod
    def update(cls, git_commit_msg='update blog'):
        print(f"[EXEC] git add -A;git commit -m '{git_commit_msg}';git push")
        return False
