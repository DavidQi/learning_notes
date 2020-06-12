# 一、基础知识

1、**创建数据库**
```sql
CREATE DATABASE database-name
```

2、**删除数据库**
```sql
drop database dbname
```

3、**备份sql server**
```sql
--- 创建 备份数据的 device
USE master
EXEC sp_addumpdevice 'disk', 'testBack', 'c:mssql7backupMyNwind_1.dat'
--- 开始 备份
BACKUP DATABASE pubs TO testBack 
```

4、**创建新表**
```sql
create table tabname (col1 type1 [not null] [primary key],col2 type2 [not null],..) 
```
   从已有的表创建新表： 
   
A：
```sql
create table tab_new like tab_old 
```

B：
```sql
create table tab_new as select col1,col2… from tab_old definition only
```

5、**删除新表**
```sql
drop table tabname 
```

6、**增加一个列**
```sql
Alter table tabname add column col type
```
注：列增加后将不能删除。DB2中列加上后数据类型也不能改变，唯一能改变的是增加varchar类型的长度。

7、**添加/删除主键** 
```sql
Alter table tabname add primary key(col) 
Alter table tabname drop primary key(col) 
```

8、**创建/删除索引**
```sql
create [unique] index idxname on tabname(col….) 
drop index idxname
```
注：索引是不可更改的，想更改必须删除重新建。

9、**创建/删除视图**
```sql
create view viewname as select statement 
drop view viewname
···

10、**几个简单的基本的sql语句**
选择：
```sql
select * from table1 where ...
```

插入：
```sql
insert into table1(field1,field2) values(value1,value2)
```

删除：
```sql
delete from table1 where ...
```

更新：
```sql
update table1 set field1=value1 where ...
```

查找：
```
select * from table1 where field1 like ’%value1%’
```

排序：
```sql
select * from table1 order by field1,field2 [desc]
```

总数/求和/平均/最大/最小：
```sql
select count as totalcount from table1
select sum(field1) as sumvalue from table1
select avg(field1) as avgvalue from table1
select max(field1) as maxvalue from table1
select min(field1) as minvalue from table1
```

11、**几个高级查询运算词**

A： UNION 运算符 

UNION 运算符通过组合其他两个结果表（例如 TABLE1 和 TABLE2）并消去表中任何重复行而派生出一个结果表。当 ALL 随 UNION 一起使用时（即 UNION ALL），不消除重复行。两种情况下，派生表的每一行不是来自 TABLE1 就是来自 TABLE2。 

B：EXCEPT 运算符 

EXCEPT运算符通过包括所有在 TABLE1 中但不在 TABLE2 中的行并消除所有重复行而派生出一个结果表。当 ALL 随 EXCEPT 一起使用时 (EXCEPT ALL)，不消除重复行。

C：INTERSECT 运算符

INTERSECT运算符通过只包括 TABLE1 和 TABLE2 中都有的行并消除所有重复行而派生出一个结果表。当 ALL随 INTERSECT 一起使用时 (INTERSECT ALL)，不消除重复行。 

注：使用运算词的几个查询结果行必须是一致的。 

12、**使用外连接**

A、left （outer） join： 

左外连接（左连接）：结果集几包括连接表的匹配行，也包括左连接表的所有行。

```sql
select a.a, a.b, a.c, b.c, b.d, b.f from a LEFT OUT JOIN b ON a.a = b.c
```

B：right （outer） join: 

右外连接(右连接)：结果集既包括连接表的匹配连接行，也包括右连接表的所有行。 

C：full/cross （outer） join： 

全外连接：不仅包括符号连接表的匹配行，还包括两个连接表中的所有记录。


13、**Group by**

一张表，一旦分组 完成后，查询后只能得到组相关的统计信息: count, sum, max, min, avg  

在SQLServer中分组时：不能以text, ntext, image类型的字段作为分组依据

在selecte统计函数中的字段，不能和普通的字段放在一起； 


14、**对数据库进行操作**

分离数据库： sp_detach_db;

附加数据库：sp_attach_db 后接表明，附加需要完整的路径名

15.**修改数据库的名称**
```sql
sp_renamedb 'old_name', 'new_name'
```

# 二、提升
by default: 源表名：a 新表名：b

1、**复制表**

只复制结构 (Access可用)
```sql
select * into b from a where 1<>1  ---仅用于SQlServer
--- or
select top 0 * into b from a
```

2、**拷贝表**

拷贝数据 (Access可用)
```sql
insert into b(a, b, c) select d,e,f from b; 
```

3、**跨数据库之间表的拷贝**

具体数据使用绝对路径 (Access可用)
```sql
insert into b(a, b, c) select d,e,f 
from b in '"&Server.MapPath(".")&"data.mdb" &"' where...
```

4、**子查询**
```sql
select a,b,c from X where a IN (select d from Y ) 
```

5、**显示文章、提交人和最后回复时间**
```sql
select a.title, a.username, b.adddate from table a, (select max(adddate) adddate from table where table.title=a.title) b 
```

6、**外连接查询**
```sql
select x.a, x.b, x.c, y.c, y.d, y.f from x LEFT OUT JOIN y ON x.a = y.c 
```

7、**在线视图查询**
```sql
select * from (SELECT a,b,c FROM a) T where t.a > 1; 
```

8、**between的用法**

between限制查询数据范围时包括了边界值, not between不包括
```sql
select * from table1 where time between time1 and time2
select a,b,c, from table1 where a not between 数值1 and 数值2 
```

9、**in 的使用方法**
```sql
select * from table1 where a [not] in (‘值1’,’值2’,’值4’,’值6’) 
```

10、**两张关联表，删除主表中已经在副表中没有的信息**
```sql
delete from table1 where not exists ( select * from table2 where table1.field1=table2.field1 ) 
```
11、**四表联查**
```sql
select * from a left inner join b on a.x=b.y right inner join c on a.x=c.z inner join d on a.x=d.xx where ..... 
```

12、**日程安排提前五分钟提醒**
```sql
select * from 日程安排 where datediff('minute',f开始时间,getdate()) > 5 
```

13、**数据库分页**
```sql
select top 10 b.* from (select top 20 主键字段,排序字段 from 表名 order by 排序字段 desc) a,表名 b where b.主键字段 = a.主键字段 order by a.排序字段
```
具体实现：关于数据库分页： 
```sql
 declare @start int,@end int
  @sql  nvarchar(600)
  set @sql=’select top’+str(@end-@start+1)+’+from T where rid not in(select top’+str(@str-1)+’Rid from T where Rid>-1)’
  exec sp_executesql @sql
```

注意：在top后不能直接跟一个变量，所以在实际应用中只有这样的进行特殊的处理。Rid为一个标识列，如果top后还有具体的字段，这样做是非常有好处的。因为这样可以避免 top的字段如果是逻辑索引的，查询的结果后实际表中的不一致（逻辑索引中的数据有可能和数据表中的不一致，而查询时如果处在索引则首先查询索引） 

14、**前10条记录**
```sql
select top 10 * form table1 where 范围 
```

15、**选择在每一组b值相同的数据中对应的a最大的记录的所有信息(类似这样的用法可以用于论坛每月排行榜,每月热销产品分析,按科目成绩排名,等等.)**
```sql
select a,b,c from tablename ta where a=(select max(a) from tablename tb where tb.b=ta.b) 
```

16、**包括所有在 Table A中但不在 Table B和Table C中的行并消除所有重复行而派生出一个结果表**
```sql
(select a from tableA ) except (select a from tableB) except (select a from tableC) 
```

17、**随机取出10条数据**
```sql
select top 10 * from tablename order by newid() 
```

18、**随机选择记录**
```sql
select newid() 
```

19、**删除重复记录**

Way I:
```sql
delete from tablename where id not in (select max(id) from tablename group by col1,col2,...)
```
Way II:
```sql
select distinct * into temp from tablename
delete from tablename
insert into tablename select * from temp
```
评价：这种操作牵连大量的数据的移动，这种做法不适合大容量但数据操作

Way III:

例如：在一个外部表中导入数据，由于某些原因第一次只导入了一部分，但很难判断具体位置，这样只有在下一次全部导入，这样也就产生好多重复的字段，怎样删除重复字段 alter table tablename
```sql
--添加一个自增列
add  column_b int identity(1,1)
delete from tablename where column_b not in(
select max(column_b)  from tablename group by column1,column2,...)
alter table tablename drop column column_b 
```

20、**列出数据库里所有的表名**
```sql
select name from sysobjects where type='U' // U代表用户 
```

21、**列出表里的所有的列名**
```sql
select name from syscolumns where id=object_id('TableName') 
```

22、**列示type、vender、pcs字段，以type字段排列，case可以方便地实现多重选择，类似select 中的case。**
```sql
select type,sum(case vender when 'A' then pcs else 0 end),sum(case vender when 'C' then pcs else 0 end),sum(case vender when 'B' then pcs else 0 end) FROM tablename group by type
```

显示结果：
type vender pcs
电脑 A 1
电脑 A 1
光盘 B 2
光盘 A 2
手机 B 3
手机 C 3 

23、**初始化表table1**
```sql
TRUNCATE TABLE table1 
```

24、**选择从10到15的记录**
```sql
select top 5 * from (select top 15 * from table order by id asc) table_别名 order by id desc
```


#三、技巧

1、**1=1，1=2的使用**

在SQL语句组合时用的较多 “where 1=1” 是表示选择全部    “where 1=2”全部不选，
如：
```sql
if @strWhere != '' 
  begin
    set @strSQL = 'select count(*) as Total from [' + @tblName + '] where ' + @strWhere 
  end
else 
  begin
    set @strSQL = 'select count(*) as Total from [' + @tblName + ']' 
  end
```

我们可以直接写成 错误！未找到目录项。
```sql
set @strSQL = 'select count(*) as Total from [' + @tblName + '] where 1=1 安定 '+ @strWhere 
```

2、**收缩数据库**
```sql
--重建索引
DBCC REINDEX
DBCC INDEXDEFRAG
--收缩数据和日志
DBCC SHRINKDB
DBCC SHRINKFILE 
```

3、**压缩数据库**
```sql
dbcc shrinkdatabase(dbname) 
```

4、**转移数据库给新用户以已存在用户权限**
```sql
exec sp_change_users_login 'update_one','newname','oldname'
go 
```

5、**检查备份集**
```sql
RESTORE VERIFYONLY from disk='E:dvbbs.bak' 
```

6、**修复数据库**
```sql
ALTER DATABASE [dvbbs] SET SINGLE_USER
GO
DBCC CHECKDB('dvbbs',repair_allow_data_loss) WITH TABLOCK
GO
ALTER DATABASE [dvbbs] SET MULTI_USER
GO 
```

7、**日志清除**
```sql
SET NOCOUNT ON
DECLARE @LogicalFileName sysname,
 @MaxMinutes INT,
 @NewSize INT 
USE tablename -- 要操作的数据库名
SELECT  @LogicalFileName = 'tablename_log', -- 日志文件名
@MaxMinutes = 10, -- Limit on time allowed to wrap log.
 @NewSize = 1  -- 你想设定的日志文件的大小(M) Setup / initialize
DECLARE @OriginalSize int
SELECT @OriginalSize = size 
 FROM sysfiles
 WHERE name = @LogicalFileName
SELECT 'Original Size of ' + db_name() + ' LOG is ' + 
 CONVERT(VARCHAR(30),@OriginalSize) + ' 8K pages or ' + 
 CONVERT(VARCHAR(30),(@OriginalSize*8/1024)) + 'MB'
 FROM sysfiles
 WHERE name = @LogicalFileName
CREATE TABLE DummyTrans
 (DummyColumn char (8000) not null) 

DECLARE @Counter    INT,
 @StartTime DATETIME,
 @TruncLog   VARCHAR(255)
SELECT @StartTime = GETDATE(),
 @TruncLog = 'BACKUP LOG ' + db_name() + ' WITH TRUNCATE_ONLY' DBCC SHRINKFILE (@LogicalFileName, @NewSize)
EXEC (@TruncLog)
-- Wrap the log if necessary.
WHILE @MaxMinutes > DATEDIFF (mi, @StartTime, GETDATE()) -- time has not expired
 AND @OriginalSize = (SELECT size FROM sysfiles WHERE name = @LogicalFileName)  
 AND (@OriginalSize * 8 /1024) > @NewSize  
 BEGIN -- Outer loop.
SELECT @Counter = 0
 WHILE   ((@Counter < @OriginalSize / 16) AND (@Counter < 50000))
 BEGIN -- update
 INSERT DummyTrans VALUES ('Fill Log') DELETE DummyTrans
 SELECT @Counter = @Counter + 1
 END
 EXEC (@TruncLog)  
 END
SELECT 'Final Size of ' + db_name() + ' LOG is ' +
 CONVERT(VARCHAR(30),size) + ' 8K pages or ' + 
 CONVERT(VARCHAR(30),(size*8/1024)) + 'MB'
 FROM sysfiles 
 WHERE name = @LogicalFileName
DROP TABLE DummyTrans
SET NOCOUNT OFF 
```

8、**更改某个表**
```sql
exec sp_changeobjectowner 'tablename','dbo' 
```

9、**存储更改全部表** 
```sql
CREATE PROCEDURE dbo.User_ChangeObjectOwnerBatch
@OldOwner as NVARCHAR(128),
@NewOwner as NVARCHAR(128)
AS DECLARE @Name    as NVARCHAR(128)
DECLARE @Owner   as NVARCHAR(128)
DECLARE @OwnerName   as NVARCHAR(128) DECLARE curObject CURSOR FOR 
select 'Name'    = name,
   'Owner'    = user_name(uid)
from sysobjects
where user_name(uid)=@OldOwner
order by name OPEN   curObject
FETCH NEXT FROM curObject INTO @Name, @Owner
WHILE(@@FETCH_STATUS=0)
BEGIN     
if @Owner=@OldOwner 
begin
   set @OwnerName = @OldOwner + '.' + rtrim(@Name)
   exec sp_changeobjectowner @OwnerName, @NewOwner
end
-- select @name,@NewOwner,@OldOwner FETCH NEXT FROM curObject INTO @Name, @Owner
END close curObject
deallocate curObject
GO 
```

10、**SQL SERVER中直接循环写入数据**
```sql
declare @i int
set @i=1
while @i<30
begin
    insert into test (userid) values(@i)
    set @i=@i+1
end
```
案例：
有如下表，要求就裱中所有沒有及格的成績，在每次增長0.1的基礎上，使他們剛好及格: 

| Name  |   score |
| ------------- |:-------------:|
| Zhangshan |  80 |
| Lishi     |  59 |
| Wangwu    |  50 |
| Songquan  |  69 |

```sql
while((select min(score) from tb_table)<60)
begin
update tb_table set score =score*1.01
where score<60
if  (select min(score) from tb_table)>60
    break 
else
    continueend
```

# 数据开发-经典

1.**按姓氏笔画排序**
```sql
Select * From TableName Order By CustomerName Collate Chinese_PRC_Stroke_ci_as //从少到多 
```

2.**数据库加密**
```sql
select encrypt('原始密码')
select pwdencrypt('原始密码')
select pwdcompare('原始密码','加密后密码') = 1--相同；否则不相同 encrypt('原始密码')
select pwdencrypt('原始密码')
select pwdcompare('原始密码','加密后密码') = 1--相同；否则不相同 
```

3.**取回表中字段**
```sql
declare @list varchar(1000),
@sql nvarchar(1000) 
select @list=@list+','+b.name from sysobjects a,syscolumns b where a.id=b.id and a.name='表A'
set @sql='select '+right(@list,len(@list)-1)+' from 表A' 
exec (@sql) 
```

4.**查看硬盘分区**
```sql
EXEC master..xp_fixeddrives 
```

5.**比较A,B表是否相等**
```sql
if (select checksum_agg(binary_checksum(*)) from A)
     =
    (select checksum_agg(binary_checksum(*)) from B)
print '相等'
else
print '不相等' 
```

6.**杀掉所有的事件探察器进程**
```sql
DECLARE hcforeach CURSOR GLOBAL FOR SELECT 'kill '+RTRIM(spid) FROM master.dbo.sysprocesses
WHERE program_name IN('SQL profiler',N'SQL 事件探查器')
EXEC sp_msforeach_worker '?' 
```

7,**记录搜索**

开头到N条记录
```sql
Select Top N * From 表
```

N到M条记录(要有主索引ID)
```sql
Select Top M-N * From 表 Where ID in (Select Top M ID From 表) Order by ID   Desc
```

N到结尾记录
```sql
Select Top N * From 表 Order by ID Desc
```

案例:

例如1：一张表有一万多条记录，表的第一个字段 RecID 是自增长字段， 写一个SQL语句， 找出表的第31到第40个记录。 
```sql
select top 10 recid from A where recid not  in(select top 30 recid from A) 
```

分析：如果这样写会产生某些问题，如果recid在表中存在逻辑索引。 
```sql
select top 10 recid from A where……是从索引中查找，而后面的select top 30 recid from A则在数据表中查找，这样由于索引中的顺序有可能和数据表中的不一致，这样就导致查询到的不是本来的欲得到的数据。 
```
解决方案

1，	用order by select top 30 recid from A order by ricid 如果该字段不是自增长，就会出现问题 
2，	在那个子查询中也加条件：select top 30 recid from A where recid>-1 

例2：查询表中的最后以条记录，并不知道这个表共有多少数据,以及表结构。
```sql
set @s = 'select top 1 * from T   where pid not in (select top ' + str(@count-1) + ' pid  from  T)' 
print @s      exec  sp_executesql  @s 
```

8, **获取当前数据库中的所有用户表**
```sql
select Name from sysobjects where xtype='u' and status>=0 
```

9, **获取某一个表的所有字段**
```sql
select name from syscolumns where id=object_id('表名') 
select name from syscolumns where id in (select id from sysobjects where type = 'u' and name = '表名') 
```
两种方式的效果相同

10,**查看与某一个表相关的视图、存储过程、函数**
```sql
select a.* from sysobjects a, syscomments b where a.id = b.id and b.text like '%表名%' 
```

11,**查看当前数据库中所有存储过程**
```sql
select name as 存储过程名称 from sysobjects where xtype='P' 
```

12,**查询用户创建的所有数据库**
```sql
select * from master..sysdatabases D where sid not in(select sid from master..syslogins where name='sa')
```
或者
```sql
select dbid, name AS DB_NAME from master.sysdatabases where sid <> 0x01 
```

14,**查询某一个表的字段和数据类型**
```sql
select column_name, data_type from information_schema.columns where table_name = '表名' 
```

15,**list table foreign keys (Postgres)**
[Ref](https://stackoverflow.com/questions/1152260/postgres-sql-to-list-table-foreign-keys)

```sql
SELECT
    tc.table_schema, 
    tc.constraint_name, 
    tc.table_name, 
    kcu.column_name, 
    ccu.table_schema AS foreign_table_schema,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM 
    information_schema.table_constraints AS tc 
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
      AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
      AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name='mytable';```

16,**不同服务器数据库之间的数据操作**
 ```sql
--创建链接服务器 
exec sp_addlinkedserver   'ITSV ', ' ', 'SQLOLEDB ', '远程服务器名或ip地址 ' 
exec sp_addlinkedsrvlogin  'ITSV ', 'false ',null, '用户名 ', '密码 ' 
--查询示例 
select * from ITSV.数据库名.dbo.表名 
--导入示例 
select * into 表 from ITSV.数据库名.dbo.表名 
--以后不再使用时删除链接服务器 
exec sp_dropserver  'ITSV ', 'droplogins ' 
--连接远程/局域网数据(openrowset/openquery/opendatasource)
   --1、openrowset
     --查询示例 
         select * from openrowset( 'SQLOLEDB ', 'sql服务器名 '; '用户名 '; '密码 ',数据库名.dbo.表名)
     --生成本地表
select * into 表 from openrowset( 'SQLOLEDB ', 'sql服务器名 '; '用户名 '; '密码 ',数据库名.dbo.表名) 
     --把本地表导入远程表 
        insert openrowset( 'SQLOLEDB ', 'sql服务器名 '; '用户名 '; '密码 ',数据库名.dbo.表名) 
        select *from 本地表 
     --更新本地表 
     update b 
     set b.列A=a.列A  from openrowset( 'SQLOLEDB ', 'sql服务器名 '; '用户名 '; '密码 ',数据库名.dbo.表名) as a inner join 本地表 b on a.column1=b.column1 
        --openquery用法需要创建一个连接 
            --首先创建一个连接创建链接服务器 
               exec sp_addlinkedserver   'ITSV ', ' ', 'SQLOLEDB ', '远程服务器名或ip地址 ' 
           --查询 select * FROM openquery(ITSV,  'SELECT *  FROM 数据库.dbo.表名 ') 
    --把本地表导入远程表 
        insert openquery(ITSV,  'SELECT *  FROM 数据库.dbo.表名 ') select * from 本地表 
    --更新本地表 
        update b 
        set b.列B=a.列B FROM openquery(ITSV,  'SELECT * FROM 数据库.dbo.表名 ') as a  
        inner join 本地表 b on a.列A=b.列A 

  --3、opendatasource/openrowset 
    SELECT   * FROM   opendatasource( 'SQLOLEDB ',  'Data Source=ip/ServerName;User ID=登陆名;Password=密码 ' ).test.dbo.roy_ta 
      --把本地表导入远程表 
        insert opendatasource( 'SQLOLEDB ',  'Data Source=ip/ServerName;User ID=登陆名;Password=密码 ').数据库.dbo.表名 
       select * from 本地表 
```


# SQL Server基本函数

字符串函数 长度与分析用

1,datalength (Char_expr) 返回字符串包含字符数,但不包含后面的空格

2,substring (expression,start,length) 取子串，字符串的下标是从“1”，start为起始位置，length为字符串长度，实际应用中以len(expression)取得其长度

3,right (char_expr,int_expr) 返回字符串右边第int_expr个字符，还用left于之相反

4,isnull ( check_expression , replacement_value )如果check_expression為空，則返回replacement_value的值，不為空，就返回check_expression字符操作类

5, Sp_addtype自定義數據類型

例如：
```sql
EXEC sp_addtype birthday, datetime, 'NULL' 
```
6,set nocount {on|off}

使返回的结果中不包含有关受 Transact-SQL 语句影响的行数的信息。如果存储过程中包含的一些语句并不返回许多实际的数据，则该设置由于大量减少了网络流量，因此可显著提高性能。SET NOCOUNT 设置是在执行或运行时设置，而不是在分析时设置。

SET NOCOUNT 为 ON 时，不返回计数（表示受 Transact-SQL 语句影响的行数）。

SET NOCOUNT 为 OFF 时，返回计数


常识
在SQL查询中：from后最多可以跟多少张表或视图：256
在SQL语句中出现 Order by,查询时，先排序，后取
在SQL中，一个字段的最大容量是8000，而对于nvarchar(4000),由于nvarchar是Unicode码。 
       
       
# PostgreSQL & JSON

1, Create JSON type column

```sql
create table test (col_json json, col_array varchar []);
```

2, Query data in JSON column

```sql
-- Select col_json.name (text) from the table
select col_json->>'name' from test;

-- Get only with a specific name
select * from test where col_json->>'name' = 'Bill Gates';

-- Fetch the first index of a JSON array
select col_json->ids->0 from events;

-- Find those col_json.testing is true (boolean)
-- This need casting col_json->'testing' from json(text) to boolean
select col_json->'testing' from test where (col_json->>'testing')::boolean is true;
```

  The short arrow -> keeps the type as JSON, and the long arrow ->> returns text.
