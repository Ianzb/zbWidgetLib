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