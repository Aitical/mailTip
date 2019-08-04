import os.path as path
import json

import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email.header import Header

import time
from getpass import getpass

import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from pygments.formatters.html import HtmlFormatter

import requests
import re
from tqdm import tqdm
import  requests


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)


class Config(object):
    """
    Basic class 
    """    
    def __init__(self,):
        """
        init the module for first time
        """
        self.config_file = './config.json'

        if not path.exists(self.config_file):
            # create empty config file for first time
            self._config = dict(
                mail={},
                task={}
            )
            print('Maybe you r start for the first time...')
            self._create_mail_config()
        else:
            self._config = self._load()

            assert self._config.get('mail', None) is not None
            assert self._config.get('task', None) is not None

        self.encoding = 'utf-8'
        self.pic_url = True

    def _get_link(self, file_path):
        with open(file_path, 'rb') as f:
            img = f.read()

        files = {
            'smfile':img
        }

        req = requests.post(url='https://sm.ms/api/upload', files=files)
        res = json.loads(req.content)
        return res['data']['url']
    
    def _update_pic_link(self, content):
        
        results = re.findall(r"!\[(.+?)\)", content)

        for pic in results:
            link = pic.split('](')[-1]
            if link.startswith('http') or link.startswith('https'):
                continue
            else:
                url_link = self._get_link(link)
                content = re.sub(link, url_link, content)

        return content

    def _get_css(self, style='default'):
        formatter = HtmlFormatter(style=style)
        css = formatter.get_style_defs('.highlight')
        return css

    def _create_mail_config(self,):
        
        print('Add a new email:...')
        from_addr = input('Using email address:').strip()
        username = input('Username for quick use[email address as default]: ').strip()
        if username == '':
            username = from_addr
        passwd = getpass('Password: ').strip()
        smtp_host = input('Smtp server address:').strip()
        smtp_port = input('Smtp port: ').strip()
        if_ssl = input('Using SSl?[Y]').strip()

        if if_ssl.lower() == 'y' or if_ssl=='':
            if_ssl = 'y'
            ssl_port = input('SSL port: ').strip()
        else:
            if_ssl = 'n'
            ssl_port = ''
        # update config file
        self._config['mail'][username] = dict(
            from_addr=from_addr,
            username=username,
            passwd=passwd,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            if_ssl=if_ssl,
            ssl_port=ssl_port
            )
        # save directly
        self._save()

    def add_email(self):
        self._create_mail_config()

    def add_task(self,):
        self._create_task_config()

    def _create_task_config(self,):
        print('Create a new task pipeline...')
        task_name = input('Task name:').strip()
        
        if self._config['task'].get(task_name, None) is not None:
            print('Current task {} is in config!'.format(task_name))

        from_addr = input('From email config name(username):').strip()
        to_addr = input('To email address: ').strip()

        # update config file
        self._config['task'][task_name] = dict(
            username=from_addr,
            to_addr=to_addr,
            )
        # save directly
        self._save()

    def _save(self,):
        print('save')
        with open(self.config_file, 'w') as f:
            json.dump(self._config, f, ensure_ascii=False)

    def _load(self,):
        with open(self.config_file, 'r', encoding='utf-8') as f:
            s = json.load(f)
        return s
    
    def _clean(self):
        """
        Clean cache files
        """

    def latex2png(self, mdstr):
        groups = re.findall('\$\$\n(.+)\n\$\$', mdstr)
        bar = tqdm(groups)
        bar.set_description('math latex2pic converting...')
        index = 1
        for tex in bar:
            req = requests.get('http://latex.codecogs.com/png.latex?{}'.format(tex))

            with open('.picturecache/{}.png'.format(index), 'wb') as f:
                f.write(req.content)

            mdstr = mdstr.replace('$$\n{}\n$$'.format(tex), '![{}](.picturecache/{}.png)'.format(index, index))
            time.sleep(0.2)
            index += 1
        return mdstr

    def md2html(self, mdstr):

        css = self._get_css()
        html = '''
    <html lang="zh-cn">
    <head>
    <meta content="text/html; charset=utf-8" http-equiv="content-type" />
    <script src="http://libs.cncdn.cn/mathjax/2.3/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
<script type="text/javascript" src="http://pkuwwt.gitcafe.com/MathJax/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
    <style type="text/css">
    {css}
    </style>

    </head>
    <body>
    {body}
    </body>
    </html>
    '''

        renderer = HighlightRenderer()
        markdown = mistune.Markdown(renderer=renderer)
        mdstr = self._update_pic_link(mdstr)
        ret = markdown(mdstr)
        return html.format(css=css, body=ret)


class Task(Config):
    """
    Struct config message for each email address
    """
    def __init__(self, task_name, file_path):
        super(Task, self).__init__()

        if self._config['task'].get(task_name, None) is None:
            print('Current task {} is not in config file, create it now...'.format(task_name))
            self._create_task_config()

        self.file_path = file_path
        self.username = self._config['task'][task_name]['username']
        self.to_addr = self._config['task'][task_name]['to_addr']

        if self._config['mail'].get(self.username, None) is None:
            print('The email {} using now is not in config file, create it now...'.format(self.username))
            self._create_mail_config()

        self.from_addr = self._config['mail'][self.username]
        
        if self.from_addr['if_ssl'] == 'y':
            self.smtp = smtplib.SMTP_SSL(self.from_addr['smtp_host'], self.from_addr['ssl_port'])
        else:
            self.smtp = smtplib.SMTP(self.from_addr['smtp_host'], self.from_addr['smtp_port'])

    def login(self):
        self.smtp.login(self.from_addr['from_addr'], self.from_addr['passwd'])
    
    def close(self):
        """
        Close and exit
        """
        self.smtp.close()

    def send(self):
        """
        Send email
        """
        content = self._parse(self.file_path)
        mail = MIMEText(content, 'html', self.encoding)
        mail['Subject'] = Header(self.subject, self.encoding)
        mail['From'] = self.from_addr['from_addr']
        mail['To'] = self.to_addr
        mail['Date'] = formatdate()

        self.login()
        self.smtp.sendmail(self.from_addr['from_addr'], self.to_addr, mail.as_string())
        self.close()
        print('sent!')

    @property
    def subject(self):
        """
        Extract subject from MD file path
        """
        return self.sbj
    
    
    def save(self,):
        """
        save message to local file not sending email
        """
        pass

    def _save(self):
        pass

    def _comment(self,):
        pass

    def _parse(self, markdown_path):
        """
        Parse markdown to html for sending
        Return: html str
        """
        sbj = markdown_path.split('/')[-1].split('.')[0]
        self.sbj = '[{strtime}] {subject}'.format(strtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())), subject=sbj)

        with open(markdown_path, 'r', encoding='utf8') as md:
            mdstr = md.read()
            if self.file_path.endswith('md'):

                mdstr = self.latex2png(mdstr)
                mdstr = self.md2html(mdstr)

        return mdstr


