# [zb组件库（zbWidgetLib）](https://ianzb.github.io/project/zbWidgetLib.html)

zb组件库（zbWidgetLib）是一个PyQt5/PyQt6/PySide2/PySide6组件库，提供了一些便捷组件，目前主要用于Ianzb的个人Python项目中。

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
2025-11-20：2.9.2.1：修复无边框窗口库窗口最大化后模糊效果消失的Bug。  
2025-11-21：2.9.3：ZBF图标支持自定义颜色。  
2025-11-22：2.9.4.1：ZBF图标支持设置使用程序主题色，新增路径批量导入图标，优化图标路径处理，新增图标支持单独输入文件名。  
2025-11-23：3.0.0：优化项目路径，将不同组件分开，优化导出文件按钮写法，并新增导入文件按钮，优化文件导入信号触发条件。  
2025-11-25：3.0.1：紧急修复FileChooser误删除的Bug。  
2025-11-30：3.1.0：新增BasicEmptyPage，优化页面代码。  
2025-12-03：3.1.1.1：滚动区域支持触屏（实验性）。  
2025-12-27：3.2.0：新增NewFlyoutAnimationType和NewInfoBadgePosition。  
2026-01-02：3.3.0.2：独立WindowEffectBase，优化CardGroup方法，支持WidgetGroup系列别名，新增FlowCardGroup，优化各处wid支持默认根据id生成。  
2026-01-06：3.3.1：新增不强制置顶的SimpleSplashScreen。  
2026-01-11：3.3.2：新增LineEditWithLabel，取消使用AcrylicComboBox。  
2026-01-18：3.4.0.1：加入三个新增的进度条组件，支持随机和固定值状态切换，背景、大小、粗细等设置。修复窗口启动时窗口效果迟钝出现的Bug。  
2026-01-19：3.4.1：修复窗口效果背景在showEvent后恢复为Mica的Bug。  
2026-01-20：3.4.2：修复FlowCardGroup的addWidget接口错误的Bug。  
2026-02-07：3.4.3：由于无边框窗口库更新，取消2.9.2.1版本对组件库Bug的修复。  
2026-02-13：3.5.0.1：新增单独的内置图标接口，PageSpliter新增总数显示，首页尾页按钮。  
2026-02-14：3.5.1：修复打包内置图标错误的Bug。  