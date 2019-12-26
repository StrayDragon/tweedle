from ..utils import shell
from ..utils.terminal import log


class Blog(object):
    PASS = '[Ok]'
    NOT_PASS = '[Fail]'
    BASED_CMD = 'hexo'

    publish_commands = ('hexo clean', 'hexo g -d', 'hexo clean', 'rm .deploy_git -rf')

    @staticmethod
    def publish():
        for command in Blog.publish_commands:
            log(f"Current Running Command: '{command}' ... ", font_color='green', bold=True)
            completed_process = shell.run(command)

    finish_commands = ('git add -A', 'git commit -m "update blog"', 'git push')

    @staticmethod
    def finish():
        for command in Blog.finish_commands:
            log(f"Current Running Command: '{command}' ... ", font_color='green', bold=True)
            completed_process = shell.run(command)
