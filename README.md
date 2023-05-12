# Manga Toolkit

### 介绍
想自己下载漫画到ipad上看，故建此仓库。目前只支持漫画柜，以后会支持其他漫画网址的爬取。

### 工具
1. 从[漫画柜](https://www.manhuagui.com)下载漫画
   使用文件: `main.py`: 找到想要下载的漫画的第一张第一页的网址，修改`name`和`url`(name随意取即可),脚本会自动把整个漫画分章节下载到`./imgs/{name}/`下。

2. 合订下载下来的章节
   使用文件`combiner.py`: 修改`root_folder`和`k`。该脚本会把每k个章节合并，并且储存在`./combined_folders`目录下。这么做是为了合并文件夹用于转换epub。

3. 下载[Kindle Comic Converter](https://kcc.iosphe.re/)对每个combined文件夹转换即可。记得选epub格式。