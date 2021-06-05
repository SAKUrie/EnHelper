--表建立

--1.单词模块
create table Words(
	Wno char(6) primary key,
	Word varchar(50) not null,
	Wpos nchar(4) not null,
	Wpara nvarchar(20) not null,
)
create table WS(
	Wno char(6),
	Sno char(6),
	primary key(Wno,Sno),
	foreign key(Wno) references Words(Wno),
	foreign key(Sno) references Sentences(Sno),
)
create table Sentences(
	Sno char(6) primary key,
	Sentence varchar(max) not null,
	Sch varchar(max) not null
)
create table DS(
	Wno char(6),
	Dno char(2),
	primary key(Wno,Dno),
	foreign key(Wno) references Words(Wno),
	foreign key(Dno) references Diff(Dno),
)
create table Diff(
	Dno char(2) primary key,
	Dlevel varchar(10) not null
)
go

--2.用户模块
create table Users(
	UserName nvarchar(7),
	ID char(7) primary key,
	Passwd nvarchar(16) not null,
	Pno char(2),
	Icon_url varchar(max)
)
go
create table [Permissions](
	Pno char(2) primary key,
	Pget nvarchar(6)
)
go
--3.词汇背诵模块
create table MemoryRecord(
	Mno char(9) primary key,
	ID char(7) not null,
	Cno char(9)not null,
	Wno char(6) not null,
	Mtime date default getdate(),
	Mok bit,
	Misno char(9),
	foreign key(Wno) references Words(Wno),
	foreign key(Cno) references CustomsLibrary(Cno),
	foreign key(ID) references Users(ID),
	foreign key(Misno) references Mistakes(Misno)
)
create table Notes(
	ID char(7),
	Nno char(6),
	Nnote_url varchar(max),
	CreateTime date	 default getdate(),
	UpdateTime date	
	primary key(ID,Nno),
	foreign key(ID) references Users(ID)
)
create table Mistakes(
	ID char(7),
	Misno char(9),
	primary key(Misno),
	foreign key(ID) references Users(ID)
)
create table MistakesInfo(
	Misno char(9) primary key,
	Wno char(6) not null,
	Mtime smalldatetime default getdate()
)

--4.个人词库模块
create table NormalLibrary(
	Cno char(9) primary key,
	Totalnum smallint default 0,
)
create table CustomsLibrary(
	ID char(7),
	Cno char(9),
	OKnum smallint default 0,
	Totalnum smallint default 0,
	CreateTime date,
	Finish bit,
	primary key(Cno),
	foreign key(ID) references Users(ID)
)

create table LibraryInfo(
	Cno char(9),
	Wno char(6),
	primary key(Wno,Cno),
	foreign key(Cno) references CustomsLibrary(Cno),
	foreign key(Wno) references Words(Wno)
)
go

--视图建立

--1.普通用户信息展示视图
create view UserView(ID,用户名,头像)
as
select ID,UserName,Icon_url
from Users
go
--2.词汇信息全展示视图
create view FullWord(Wno,Word,Wpos,Wpara,Sno,Sentence,Sch)
as
select WS.Wno,Word,Wpos,Wpara,WS.Sno,Sentence,Sch
from Words,Sentences,WS
where  Words.Wno=WS.Wno and Sentences.Sno=WS.Sno
go
--3.用户个人背诵记录视图
create view UserMemory
as
select ID,Mno,Words.Wno,Word,Wpara,Mok,Cno,Mtime
from MemoryRecord,Words
where MemoryRecord.Wno=Words.Wno
go
--4.用户个人错题展示视图
create view UserMistake
as
select ID,Mistakes.Misno,Words.Wno,Word,Wpara,Wtime
from Words,Mistakes,MistakesInfo
where Words.Wno=MistakesInfo.Wno and MistakesInfo.Misno=Mistakes.Misno
go

--完整性约束
--1.约束

--1.1 密码约束
--密码位于8-16位之间，必须包含数字和字母（不区分大小写）
ALTER TABLE Users
ADD CONSTRAINT pswdCheck CHECK ((len(Passwd) between 8 and 16) and patindex('%[0-9]%',Passwd)>0 and (patindex('%[a-z]%',Passwd)>0 or patindex('%[A-Z]%',Passwd)>0 ))
--1.2 用户名约束
--只能包括汉字和单个下划线
ALTER TABLE Users
ADD CONSTRAINT NameCheck CHECK ( len(UserName)>=2 and (patindex('%[^吖-座]%',UserName)=0 or (SUBSTRING(UserName,patindex('%[^吖-座]%',UserName),1) = '_')))
--1.3 单词英文约束
--只能包括字母和单个连接线
ALTER TABLE Words
ADD CONSTRAINT WordCheck CHECK ((patindex('%[^a-zA-z]%',Word)=0 or (SUBSTRING(Word,patindex('%[^a-zA-z]%',Word),1) = '-')))
--（保证以服务器时间为准）
--1.4 背诵记录时间约束
ALTER TABLE MemoryRecord
ADD CONSTRAINT TimeCheck1 CHECK (Mtime>=getdate())
--1.5 错误记录时间约束
ALTER TABLE MistakasInfo
ADD CONSTRAINT TimeCheck2 CHECK (Mtime>=getdate())
--1.6 词库建立时间约束
ALTER TABLE CustomsLibrary
ADD CONSTRAINT TimeCheck3 CHECK (CreateTime>=getdate())
--1.7 词库完成标记约束
ALTER TABLE CustomsLibrary
ADD CONSTRAINT FinishCheck CHECK((Finish=1 and OKnum = Totalnum and OKnum != 0)or (Finish=0 and ((OKnum=Totalnum and Totalnum=0 ) or (OKnum!=Totalnum))))

--2.触发器
--完成标志设置
go
create trigger finish_tag on CustomsLibrary
for update
as
declare @newOK int,@Total int,@now char(9)
select @newOK = OKnum,@Total = Totalnum,@now = Cno
from inserted
if @newOK = @Total and @newOK>0
	update CustomsLibrary
	set finish = 1
	where @now=Cno
--错题记录补全
--实现级联更新
go
create trigger MemoryUpdate on MemoryRecord
for update,insert
as
declare @ID char(7),@Cno char(9),@Wno char(6),@Mtime date,@ok bit,@Misno char(9)
select @ID=ID,@cno=Cno,@Wno=Wno,@Mtime=Mtime,@ok=Mok
from inserted
if @ok=0
begin
	insert into Mistakes
	values(@ID,@Misno)
	insert into MistakesInfo
	values(@Misno,@Wno,@Mtime)
end
else
begin
	update CustomsLibrary
	set OKnum=OKnum+1
	where Cno=@Cno
end

--函数与存储过程设计
--存储过程
--1.获取用户背诵记录
go
create proc get_user_memory @ID char(7)
as
begin
select *
from UserMemory
where ID=@ID
end
go
--2.根据背诵记录生成考试词单
create proc generate_test @ID char(7)
as
begin
	declare @Word varchar(50),@Cno char(9)
	declare i scroll cursor
	for
	select distinct top 30 u.Cno,u.Mok,u.Wno,u.Word,u.Mtime,u.ID
	from UserMemory as u
	where ID=@ID
	order by Mtime

	open i
	fetch next from i into @Word,@Cno
	while @@FETCH_STATUS = 0
	begin
		print 'Word: '+@Word+' \n'
		fetch next from i into @Word,@Cno
	end
	close i
	deallocate i
end
go
--3.根据用户需求与记录生成当日背诵词单
create proc gererate_Memo @ID char(7)
as
begin
	--错误单词复习
	declare @Word varchar(50),@Wpos char(4),@Wpara nvarchar(20),@Sentence varchar(max)
	declare i scroll cursor
	for
	select distinct top 10 u.Word,Wpos,u.Wpara,Sentence,Wtime
	from UserMistake as u,FullWord
	where ID=@ID and FullWord.Wno=u.Wno
	order by u.Wtime 

	open i
	fetch next from i into @Word,@Wpos,@Wpara,@Sentence
	while @@FETCH_STATUS = 0
	begin
		print 'Recently Wrong Word: '+@Word+'词性：'+@Wpos+'汉语释义： '+@Wpara+'例句：'+@Sentence+'\n'
		fetch next from i into @Word,@Wpos,@Wpara,@Sentence
	end
	close i
	deallocate i

	--新单词背诵
	declare i scroll cursor
	for
	select top 20 Word,Wpos,Wpara,Sentence
	from  CustomsLibrary as c,LibraryInfo as l,FullWord
	where @ID=c.ID and l.Cno=c.Cno and l.Wno=FullWord.Wno and c.Finish=0
		and not exists(	select *
						from UserMemory
						where Wno = l.Wno and Mok = 1
					)
	order by c.CreateTime

	open i
	fetch next from i into @Word,@Wpos,@Wpara,@Sentence
	while @@FETCH_STATUS = 0
	begin
		print 'New Word: '+@Word+'词性：'+@Wpos+'汉语释义： '+@Wpara+'例句：'+@Sentence+'\n'
		fetch next from i into @Word,@Wpos,@Wpara,@Sentence
	end
	close i
	deallocate i

	--背诵单词复习
	declare i scroll cursor
	for
	select distinct top 10 u.Word,Wpos,u.Wpara,Sentence,Mtime
	from UserMemory as u,FullWord
	where ID=@ID and FullWord.Wno=u.Wno
	order by u.Mtime

	open i
	fetch next from i into @Word,@Wpos,@Wpara,@Sentence
	while @@FETCH_STATUS = 0
	begin
		print 'Reviewing Word: '+@Word+'词性：'+@Wpos+'汉语释义： '+@Wpara+'例句：'+@Sentence+'\n'
		fetch next from i into @Word,@Wpos,@Wpara,@Sentence
	end
	close i
	deallocate i
end
go
--函数
--1.获取用户定制词库表(只显示当前最新活跃记录)
create function UserLib (@ID char(7))
returns table
return
select c.Cno,c.ID,Word,Wpara
from CustomsLibrary as c,LibraryInfo as l,FullWord
where c.Finish=0 and c.CreateTime = (select top 1 CreateTime from CustomsLibrary as i where i.ID=@ID order by CreateTime asc)
and FullWord.Wno=l.Wno
go
--2.查询单词函数
create function WordSearch(@word varchar(50)) 
returns table
as
return 
select *
from Words
where Word=@word
go
--3.查询例句函数
create function SentenceSearch(@sentence varchar(max))
returns table
as
return
select *
from Sentences
where Sentence=@sentence

--聚簇设计
