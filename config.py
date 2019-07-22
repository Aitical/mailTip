import os.path as path
import os 
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
    def __init__(self, comment):
        """
        init the module for first time
        """
        if not path.exists('./config/'):
            os.mkdir('./config')
        if not path.exists('./config/mailTip'):
            os.mkdir('./config/mailTip')
        self.config_file = './config/mailTip/{}.json'.format(comment)
        self.comment = comment

        if not path.exists(self.config_file):
            self.from_addr, self.username, self.passwd, self.to_addr, self.smtp_host, \
            self.smtp_port, self.if_ssl, self.ssl_port =  self._create_config()
        else:
            self.from_addr, self.username, self.passwd, self.to_addr, self.smtp_host, \
            self.smtp_port, self.if_ssl, self.ssl_port =  self._load()
        self.encoding = 'utf-8'


    def _get_css(self, style='default'):
        formatter = HtmlFormatter(style=style)
        css = formatter.get_style_defs('.highlight')
        return css

    def _create_config(self,):

        print('Init for the first time...')
        from_addr = input('Using email address:').strip()
        username = input('Username[email address as default]: ').strip()
        if username == '':
            username = from_addr
        passwd = getpass('Password: ').strip()
        to_addr = input('Aim email address: ').strip()
        smtp_host = input('Smtp server address:').strip()
        smtp_port = input('Smtp port: ').strip()
        if_ssl = input('Using SSl?[Y]').strip()

        if if_ssl.lower() == 'y' or if_ssl=='':
            if_ssl = 'y'
            ssl_port = input('SSL port: ').strip()
        else:
            if_ssl = 'n'
            ssl_port = ''

        config = dict(
            from_addr=from_addr,
            username=username,
            passwd=passwd,
            to_addr=to_addr,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            if_ssl=if_ssl,
            ssl_port=ssl_port
            )
        with open(self.config_file, 'w') as f:
            json.dump(config, f, ensure_ascii=False)

        return list(config.values())

    def _save(self, dict):
        
        pass
    def _load(self,):
        with open(self.config_file, 'r', encoding='utf-8') as f:
            s = json.load(f)
        return list(s.values())
        
    def _clean(self):
        """
        Clean cache files
        """
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
        ret = markdown(mdstr)
        return html.format(css=css, body=ret)


class Mail(Config):
    """
    Struct config message for each email address
    """
    def __init__(self, comment, file_path):
        super(Mail, self).__init__(comment)
        
        self.file_path = file_path

        if self.if_ssl == 'y':
            self.smtp = smtplib.SMTP_SSL(self.smtp_host, self.ssl_port)
        else:
            self.smtp = smtplib.SMTP(self.smtp_host, self.smtp_port)

    def edit(self):
        """
        Edit message
        """

        pass
    def login(self):
        self.smtp.login(self.username, self.passwd)
    
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
        mail['From'] = self.from_addr
        mail['To'] = self.to_addr
        mail['Date'] = formatdate()

        self.login()
        self.smtp.sendmail(self.from_addr, self.to_addr, mail.as_string())
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
        self.sbj = '[{strtime}] {subject}'.format(strtime= time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())), subject=sbj) 

        with open(markdown_path, 'r') as md:
            mdstr = md.read()
            if self.file_path.endswith('md'):
                mdstr = self.md2html(mdstr)

        return mdstr


