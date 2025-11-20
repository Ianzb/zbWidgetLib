# [zb组件库（zbWidgetLib）](https://ianzb.github.io/project/zbWidgetLib.html)

zb组件库（zbWidgetLib）是一个PyQt5组件库，提供了一些便捷组件，目前用于zb小程序等个人Python项目中。

## 链接

[Github](https://github.com/Ianzb/zbWidgetLib/)  
[PyPi](https://pypi.org/project/zbWidgetLib/)

## 历史

2024-11-02：0.0.1：随着zb小程序5.0.0版本的重构，zbWidgetLib相关功能独立。  
2025-02-18：0.1.3：独立发布，重写CardGroup组件，优化docstring。  
2025-02-19：0.1.4：优化Image组件，删除fixed_size参数，修复信号重复绑定的Bug，针对下载过程中切换图片的场景进行处理。对线程池参数命名和类型声明进行整体优化。  
2025-02-21：0.1.5b1：删除无用的StyleSheet代码。  
2025-03-01：1.0.0b1：大规模优化代码，完善方法，修改名称。  
2025-04-13：1.0.0：更新页面图标设置方式。  
2025-04-13：1.1.0：退回到PyQt5。  
2025-04-20：1.1.0.1：修复SmallInfoCard文本处理的问题。  
2025-04-21：1.1.1：更新BasicTabPage，新增大量实用方法，并修复首个标签页设置不正确的Bug。  
2025-05-17：2.0.0b2：大规模优化代码，添加大量方法和方法别名，新增Image和Window组件。  
2025-05-23：2.0.0b4：修改GrayCard的QSS，新增文件选择器组件。  
2025-05-24：2.0.0b5：优化GrayCard的QSS。  
2025-05-31：2.0.0：修复GrayCard的QSS。  
2025-07-17：2.0.1：优化添加标签页。  
2025-07-19：2.1.0.1：新增LoadingMessageBox。  
2025-07-20：2.1.1：添加LoadingMessageBox退出后自动删除自身。  
2025-07-26：2.1.2：添加允许复制相关选项，LoadingMessageBox新增随机进度条支持。  
2025-08-01：2.1.3：修复进度条判断错误的Bug并完善接口，LoadingCard新增随机进度条支持。
2025-08-02：2.2.0.1：新增SaveFilePrimaryPushButton和SaveFilePushButton，删除BigInfoCard的Tag的固定大小，LoadingMessageBox添加默认文本。  
2025-08-06：2.2.2：setToolTip现在为亚克力样式，修复TabPage类变量错误。  
2025-08-06：2.3.0：新增PageSpliter，CardGroup支持横向排列。  
2025-08-07：2.3.1.1：PageSpliter新增7个参数和相关接口，并大规模优化代码。  
2025-08-08：2.3.2：修复修改total_count时翻页按钮响应不及时的Bug。  
2025-08-08：2.4.0.3：新增FlowGrayCard，优化GrayCard间距，新增ComboBoxWithLabel，完善PageSpliter信号阻止机制，完善total_count小于等于0时的逻辑，SaveFilePushButton新增自动创建目录。  
2025-08-20：2.5.0：新增setSelectable函数，并尝试替换原函数，新增ScrollMessageBoxBase和ScrollMessageBox，优化右键菜单样式。  
2025-09-03：2.5.1：尝试修复快速开关LoadingMessageBox可能导致无法关闭。  
2025-09-14：2.5.2：修复删除BasicTabPage最后一个页面时崩溃的Bug。  
2025-09-23：2.5.3：添加pyi文件。  
2025-09-24：2.6.0.1：新增ScrollDialog。  
2025-09-25：2.6.1：优化ScrollDialog高度判定。  
2025-09-27：2.7.0：新增ZBF类，支持两款图标。  
2025-10-02：2.7.2：修复LoadingMessageBox显示异常的Bug，Image支持FIF图标。  
2025-10-23：2.7.3：修复setNewToolTip重复运行导致多个提示重叠的Bug，新增removeNewToolTip方法。  
2025-10-26：2.7.4：修复FileChooser返回文件有空字符串的Bug。  
2025-10-26：2.8.0：ZBF添加实时新增图标的接口，取消内置图标。  
2025-11-16：2.9.0.4：Window新增各种模糊效果设置功能。  
2025-11-19：2.9.1.1：适配不同版本的PyQt/PySide。  
2025-11-20：2.9.2：修复无边框窗口库窗口最大化后模糊效果消失的Bug。  