## SQLtest ：考研论坛数据管理系统

### 需求分析：

2021考研将近，学长学姐们都在夜以继日地学习以求考上自己梦寐的学校。但考研不仅仅是单纯的学习比拼，考研相关信息的获取也同样重要。同学们获取考研信息的主要渠道有人际交流、搜索引擎、通讯软件、考研论坛等。而考研论坛因其信息密度高，数据流量大，专业定向明确等多项优势，占据了考研信息获取的很大一部分。

但论坛信息流量大而结构复杂，有价值的帖子容易被错过，而往往会花费大量时间在无意义的信息上，浪费宝贵的学习复习时间。因此考研论坛资讯管理系统应运而生。

### 功能设计：

考研论坛资讯管理系统使用B/S架构，基于Python，应用Flask框架完成前后端的设计和连接，使用SQL Server作为后端的数据库管理系统，并使用sqlalchemy进行连接和数据库操纵。用户只需要打开浏览器就能快速获取到论坛中最有价值的信息，查看统计信息，使用关键字进行查询与统计查询。而作为管理员同时能够对帖子、用户、管理员实现增删改查等功能。

### 任务分工：

独立完成

### 系统中每张表的说明

POST表

| 列名         | 数据类型      | 约束                  | 备注         |
| ------------ | ------------- | --------------------- | ------------ |
| ID           | int           | primary key           | 标识符       |
| url          | nvarchar(50)  | not null              | 来源网址     |
| postTime     | nvarchar(50)  | not null              | 发帖时间     |
| postTitle    | nvarchar(50)  | not null              | 标题         |
| postContent  | nvarchar(MAX) | null                  | 内容         |
| watches      | int           | >=0                   | 浏览数       |
| replies      | int           | >=0                   | 回复数       |
| favorites    | int           | >=0                   | 收藏数       |
| likes        | int           | >=0                   | 点赞数       |
| dislikes     | int           | >=0                   | 点踩数       |
| additions    | int           | >=0                   | 附件数       |
| writerName   | nvarchar(50)  | foreign key（WRITER） | 作者昵称     |
| writerYear   | int           | null                  | 作者考研年份 |
| writerSchool | nvarchar(50)  | null                  | 作者学习     |
| writerTarget | nvarchar(50)  | null                  | 作者目标     |

WRITER表

| 列名         | 数据类型     | 约束        | 备注         |
| ------------ | ------------ | ----------- | ------------ |
| writerName   | nvarchar(50) | primary key | 作者昵称     |
| writerYear   | int          | null        | 作者考研年份 |
| writerSchool | nvarchar(50) | null        | 作者学习     |
| writerTarget | nvarchar(50) | null        | 作者目标     |

ROOT表

| 列名     | 数据类型     | 约束        | 备注     |
| -------- | ------------ | ----------- | -------- |
| ID       | nvarchar(50) | primary key | 管理员ID |
| password | nvarchar(50) | not null    | 登录密码 |

### 系统运行环境配置

在ODBC（32位）中设置数据源，名称：sqltest，服务器：localhost，登录id：testServer，登录密码：123456

### 安装操作说明

从github克隆源码，并在本地服务器上运行。之后用浏览器打开http://127.0.0.1:5000/

```
git install https://github.com/ArComet/SQLtest.git
python app.py
```

### 实验结果总结

系统美观大方，运行较流畅。界面友好、使用方便，对用户有良好的可操作性。对功能性需求全部完成了实现，且实现了大部分非功能性需求。本系统能为广大计算机考研学生提供了快速便捷的论坛信息获取功能，提高了考研信息的获取效率，有效节约出了考生们的学习时间。但因为时间紧迫且独立完成项目，部分非功能性需求暂未实现，管理员登录及密码修改。

在未来的改进方向上，一、可以添加超级管理员实体替代现有的管理员实体，管理员只能管理作者和帖子，超级管理员只能管理管理员，提高系统的安全性。二、可以将帖子的时效性加入考虑，在价值计算中为发布时间较近的帖子增加数值，提高其出现的权重。

### 编程工作总结

考研论坛资讯管理系统的最大创新点在于它有一个自主设计的价值算法，能够将最有价值的帖子从茫茫数据中筛选而出，并将其推送给用户，从而有效节约考研学生的学习时间，帮助他们找到有用的考研资讯。而数据库中的触发器能够有效节约项目的工程量，少写了很多前端后端的代码，在系统提高了数据库的自动化水平。
