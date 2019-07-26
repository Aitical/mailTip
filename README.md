# mailTip
### 简介

项目产生背景：

- 正在实习，需要做一些日常的记录，需要整理用于记录和汇报
- 需要与导师进行组会汇报，但在研究院实习没时间参加组会，采用邮件方式发送汇报内容

平时记录使用Markdown文件，这个小工具就是自动发送指定Markdown文件内容，在邮件内预览，避免下载附件

实现思路：

- Markdown语法完全兼容html所以就md转html然后发送邮件html主体即可，实现邮件内打开即可预览到主体

现有进度：

- `md`和`html`文件直接自动发送，邮件内预览
- 自动检测文本中图片内容，使用公共图床(sm.ms)获取图片外链

下一步计划：

- 公式显示问题
- 使用git仓库作为图床，实现对以往图片管理

### 特点

- jupyter导出html后也可以一键发送，邮件内看代码！

![1564125213212.png](https://i.loli.net/2019/07/26/5d3ab9759faf558435.png)

- 本地图片自动转换图床链接

  使用截图本地截图时，产生本地图片或者直接粘贴到md文本中，都是本地图片路径，避免手动转换成图床链接，实现自动检测、上传、获取图床链接，直接提交含有本地图片的markdown内容，邮件中也可直接预览图片！(**图床使用sm.ms公共图床，注意图片的隐私性**)

### 使用

```shell
git clone https://github.com/Aitical/mailTip.git
cd mailTip
python mailTip -h

#Using mailTip pipeline!

#optional arguments:
#  -h, --help    show this help message and exit
#  -c            create a task pipeline
#  -s S          task pipeline name to send
#  --file FILE   file path
```

- `-c`主动创建任务信息
- `-s`按照任务配置自动化提交
- `--file`提交文件(`md`或`html`格式)

```shell
python mailTip -s hello --file test.md
```

直接使用，这样创建一个`hello`任务，按照提示填写自己邮件的配置信息即可。

**注意**配置邮件的username，用于快速选中邮件配置内容填写时请唯一(本地使用username，不影响发送账号信息)。