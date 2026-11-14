前置需求：
- Latex
- Pandoc

0. 使用前复制整个脚本文件夹。双击“删除示例文件.sh”脚本清空所有示例文件。

1. 修改配置文件config.yaml，包括参数：

input-files:  
输入文件，将需要生成的md文件放在对应的inputs夹中
【自带4个sample供参考，默认为“sample3_科技文章”。可在“samples_preview”中预览】

resource-path:
图片资源路径，主要修改“md内容中的图片资源”，一般同input目录

template: 
模版文件，选择templates文件夹中对应的模版
【自带4个template供参考，默认为“template_科技文章20260408”】

filters: 
过滤器，选择filters文件夹中对应的过滤器模版
【默认为不用过滤器】

2. 双击运行“#md2pdf.bat”。
