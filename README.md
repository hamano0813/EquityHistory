# 股权沿革辅助整理工具

本工具的主要功能为根据所输入的企业历史股权变动过程，自动计算生成历次股权变动后的股权结构比例，并提供输出到Word文件功能

## 股权沿革界面

### 常规操作

- <新增>按钮可以用于增加股权变动的记录
- <删除>按钮可以删除不需要的股权变动记录行
- <编辑>按钮可以编辑已经存在的记录行
- <插入>按钮可以在当前选中行的上方插入记录行
- <复制>按钮可以将当前选中行进行完整复制并添加在选中行的下方
- <排序>按钮会按照：日期与事件两列对已经存在的记录行进行正序自动排列
- <上移>按钮可以将当前选中行上移一行
- <下移>按钮可以将当前选中行下移一行
- <载入>按钮可以读取已经保存的股权沿革文件
- <保存>按钮可以将当前所有股权沿革保存到文件

### 快捷操作

- 在窗口的空白处双击鼠标可以<新增>
- 在窗口内的记录行上左键双击鼠标可以<编辑>
- 在窗口内的记录行上右键双击鼠标可以<删除>
- <新增>的键盘快捷键为 Ctrl + N
- <删除>的键盘快捷键为 Ctrl + D
- <编辑>的键盘快捷键为 Ctrl + M
- <插入>的键盘快捷键为 Ctrl + I
- <复制>的键盘快捷键为 Ctrl + C

### 其他特征

- 上下相邻的行如果日期和事件相同，会被视为同一经济行为，自动合并部分单元格
- 同一经济行为仅支持一条备注，为该经济行为的第一行记录所包含的文字

## 预览导出界面

### 常规操作

- 当股权沿革界面内有了增删改动相关操作后，会自动刷新预览导出界面中左侧的列表
- 点击列表项目，右侧会根据所点击项目对应的经济行为，显示股权变更的描述文字以及变更完成后的股权结构比例
- <导出>按钮可以将当前历史沿革导出到Word文件（*.docx文件）

## 股权变更事件对话框

### 常规操作

- 根据股权变更的具体情况，填写相关内容，确定后新增/编辑
- 变更记录中的备注文字会插入在预览界面的描述文字中，应留意语句通顺情况
- 当事件为转让时，支持三种情况：
    - 入资方和退资方都填写了内容，则为退资方将股权转让给入资方
    - 仅入资方填写内容，退资方为空，则视同随股权转让同时进行的增资
    - 仅退资方填写内容，入资方为空，则视同随股权转让同时进行的减资
- 认缴资本不用于计算股权比例，将根据对应注册资本的情况写入预览界面的描述文字中

### 核对机制

- 日期不能为2000年01月01日，如有当天或当月发生的变更，需要选择当月其他日期
- 所有变更必须填写对应的注册资本
- 当事件为成立或增资时，入资方不可为空
- 当事件为减资时，退资方不可为空
- 当事件为转让时，入资方和退资方不可同时为空