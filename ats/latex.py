import os
import re
import subprocess
from subprocess import Popen, PIPE

import hashlib

import jinja2


_this_dir = os.path.dirname(__file__)
_template_dir = os.path.join(_this_dir, 'templates')


class LatexTemplate:
    LATEX_SUBS = (
        (re.compile(r'\\'), r'\\textbackslash'),
        (re.compile(r'([{}_#%&$])'), r'\\\1'),
        (re.compile(r'~'), r'\~{}'),
        (re.compile(r'\^'), r'\^{}'),
        (re.compile(r'"'), r"''"),
        (re.compile(r'\.\.\.+'), r'\\ldots'),
    )

    @staticmethod
    def escape_tex(value):
        newval = value
        for pattern, replacement in LatexTemplate.LATEX_SUBS:
            newval = pattern.sub(replacement, newval)
        return newval

    _env = jinja2.Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=True,
        loader=jinja2.FileSystemLoader(os.path.abspath(_template_dir))
    )

    @staticmethod
    def isoformat(dt, second=True, microsecond=False):
        if not second:
            dt = dt.replace(second=0)
        if not microsecond:
            dt = dt.replace(second=0, microsecond=0)
        return dt.isoformat()

    def __init__(self, template_filename):
        self._env.filters['te'] = self.escape_tex
        self._env.filters['isoformat'] = self.isoformat
        self.template = self._env.get_template(template_filename)  # type: jinja2.Template
        self.template_filename = template_filename

    def template_sha256(self):
        m = hashlib.sha256()
        with open(self.template.filename) as f:
            content = f.read()
        m.update(content.encode('utf-8'))
        return m.hexdigest()

    def compile(self, output, **kwargs):
        kwargs['enumerate'] = enumerate
        latex_str = self.template.render(**kwargs)

        tpl_basename = os.path.basename(self.template_filename)
        if os.path.isdir(output):
            tpl_name, tpl_ext = os.path.splitext(tpl_basename)
            tex_output_name = os.path.join(output, tpl_basename)
        else:
            tex_output_name = output
        output_dir = os.path.dirname(tex_output_name)

        with open(tex_output_name, 'w') as f:
            f.write(latex_str)

        tex_output_basename = os.path.basename(tex_output_name)
        cmd = ['latexmk', '-f', '-pdf', '-halt-on-error', tex_output_basename]
        print(" ".join(cmd))
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=output_dir)
        stdin, stderr = p.communicate()
        ret_code = p.wait()
        if ret_code != 0:
            print("!" * 100)
            print(" COMPILING LATEX FILE FAILED: {}".format(tex_output_name))
            print(" Command was: {}".format(" ".join(cmd)))
            print("!" * 100)
            print("-" * 40 + " LATEX FILE " + "-" * 40)
            print(latex_str)
            print("-" * 40 + " END LATEX FILE " + "-" * 40)
            print("-" * 40 + " STDERR " + "-" * 40)
            print(stderr.decode('utf-8'))
            print("-" * 40 + " END STDERR " + "-" * 40)
            print("-" * 40 + " STDIN " + "-" * 40)
            print(stdin.decode('utf-8'))
            print("-" * 40 + " END STDIN " + "-" * 40)

        subprocess.run(['latexmk', '-c', tex_output_basename], cwd=output_dir)
