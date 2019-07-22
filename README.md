# mailTip
项目产生背景：

- 正在实习，需要做一些日常的记录，需要整理用于交流和组会
- 需要与导师进行组会汇报，但实习不能直接交流，采用邮件方式

基本平时记录md文件，避免添加附件导致再次下载的麻烦，发邮件汇报要自己手动copy正文到邮件内容，实现预览，所以这里花小半天时间做了一个自动化发送Markdown文档的pipeline工具。

- 将邮箱空间当做云笔记
- jupyter转html导出后邮件内也可以正常预览
- 因为邮件不能加载js所以数学公示无望了，很难受

实现思路：

- Markdown语法完全兼容html所以就md转html然后发送邮件html主体即可，实现邮件内打开即可预览到主体

现有进度：

- 对`md`和`html`文件直接发送，邮件内预览即可


### 使用

```shell
git clone https://github.com/Aitical/mailTip.git
cd mailTip
python mailTip -h

#Using mailTip pipeline!

#optional arguments:
#  -h, --help    show this help message and exit
#  -t COMMENT    Task name
#  -f FILE_PATH  Path to the Markdown file
```

- `-t`选择任务,直接创建任务名，按提示信息创建配置文件即可

- `-f`提交文件(`md`或`html`格式)

