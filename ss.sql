select 
	port as 端口, 
	concat(format(u/1024/1024, 2)," M") as 上传, 
	concat(format(d/1024/1024,2)," M") as 下载, 
	concat(format((u+d)/1024/1024,2)," M") as 本月已使用流量, 
	concat(format((transfer_enable-u-d)/1024/1024/1024, 2)," G") as  本月剩余流量 
from 
	user 
where 
	port=55566;

select 
	port as 端口, 
	concat(format(u/1024/1024, 2)," M") as 上传, 
	concat(format(d/1024/1024,2)," M") as 下载, 
	concat(format((u+d)/1024/1024,2)," M") as 本月已使用流量, 
	concat(format((transfer_enable-u-d)/1024/1024/1024, 2)," G") as  本月剩余流量 
from 
	user 
;

select 
	port as 端口, 
	concat(format(u/1024/1024, 2)," M") as 上传, 
	concat(format(d/1024/1024,2)," M") as 下载, 
	concat(format((u+d)/1024/1024,2)," M") as 本月已使用流量, 
	concat(format((transfer_enable-u-d)/1024/1024/1024, 2)," G") as  本月剩余流量 
from 
	user 
where 
	port <> 55555;