## 关于DjangoUeditor配置
python3.8.2+Django3.0.3环境下用富文本编辑DjangoUEditor，DjangoUEditor中关于six的引用会报错，摸索了一下发现：

1、Django3.0.3移除了six。

2.six可以单独安装：pip install six。另外，urllib 好像也独立出来了，引用时不需有前缀。

3.安装完six之后，将DjangoUEditor中有关的引用路径修改一下。包括如下三个文件的修改。

（1）DjangoUEditor目录下的views.py文件中有如下行
from django.utils import six
from django.utils.six.moves.urllib.request import urlopen
from django.utils.six.moves.urllib.parse import urljoin

改为：
import six
from six.moves.urllib.request import urlopen
from six.moves.urllib.parse import urljoin
（2）widgets.py文件中有如下一行：

from django.utils.six import string_types  
修改为：
from six import string_types
（3）urllib似乎已从six之中独立出来，故commands.py文件中的如下一行：

from django.utils.six.moves.urllib.parse import urljoin
改为：
from urllib.parse import urljoin

（4）DjangoUeditor目录下utils.py
from django.utils import six
修改成
import six
