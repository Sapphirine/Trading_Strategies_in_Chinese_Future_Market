
###load the data for data1
###function data1
data1_HOLC_askbidVol <- function(dataname){
    #for test: dataname <- data1[2]
data_source <- file.path(user_home,"data1",dataname)
read.table(data_source,sep = ",", header=FALSE,fill=TRUE)-> total
names(total)<- c('type','price','volume','time')


# decompose the data, generate the type of 'ask', 'trade', 'bid;. the whole data set is defined as 'total'

##total
time<-as.character(total$time)
#replace Jun July to 06 07 in order to use strptime()
time1<-gsub("Jun", "06", time)
time2<-gsub("Jul", "07", time1)
#time string
time3<-gsub("Aug", "08", time2)
#minute string format unchanged
time4<-substr( time3, 0, 16)
#time_POSIXt
time5<-strptime(time3,"%d-%m-%Y  %H:%M:%S")
#minute_POSIXt
time6<-strptime(time4,"%d-%m-%Y  %H:%M")
#data_POSIXt
time7<-strptime(substr(time6,1,10),"%Y-%m-%d")
total<- data.frame(total, time5, time6, time7)
names(total)<- c('type','price','volume','time','time_POSIXt', 'minute_POSIXt', 'date_POSIXt')
ask<-total[which(total$type=="ASK"),]
trade<-total[which(total$type=="TRADE"),]
bid<-total[which(total$type=="BID"),]



###save minute and date levels for furthur use
dir.create(path=file.path(user_home,"result",dataname))
setwd(file.path(user_home,"result",dataname))
total_minutelevel <- sort(unique(total$minute_POSIXt))
trade_minutelevel <- sort(unique(trade$minute_POSIXt))
total_datelevel <- sort(unique(total$date_POSIXt))
trade_datelevel <- sort(unique(trade$date_POSIXt))


ask_date <- as.character(ask$date_POSIXt)
trade_date <- as.character(trade$date_POSIXt)
bid_date <- as.character(bid$date_POSIXt)
total_date <- as.character(total$date_POSIXt)


ask_minute <- as.character(ask$minute_POSIXt)
trade_minute <- as.character(trade$minute_POSIXt)
bid_minute <- as.character(bid$minute_POSIXt)
total_minute <- as.character(total$minute_POSIXt)
date.level<-trade_datelevel
minute <- as.character(trade_minutelevel)

save(total_minutelevel,trade_minutelevel,total_datelevel,trade_datelevel,ask_minute,trade_minute,bid_minute,total_minute,ask_date,trade_date,bid_date,total_date, date.level, minute, file="minute_date_levels.Rda")




##generate HLOC， volumn, and ask_vol, bid_vol
date=strptime(substr(minute, 1,10), "%Y-%m-%d")
df <- data.frame(minute,date, amt= rep(NA,length(minute)),open=rep(NA,length(minute)), close=rep(NA,length(minute)))

#find max and min (for "trade")
high<-tapply(trade$price, trade$minute_POSIXt, max)
high <- data.frame(names(high), high)
names(high) <- c('minute','high')
rownames(high) <- NULL

low<-tapply(trade$price, trade$minute_POSIXt, min)
low <- data.frame(names(low), low)
names(low) <- c('minute','low')
rownames(low) <- NULL
#amt

for(i in c(1:length(minute)) )
{
		
    rows<-which(trade$minute_POSIXt==minute[i])
	Vol<-0
	for(k in rows)
	{
    Vol<-trade$volume[k]+Vol
	}
    df$amt[i]<-Vol
}



#open

#whether minte

for(i in c(1 :length(minute)) )
{
		
rows<-which(trade$minute_POSIXt==minute[i])
k<-which.min(trade$time_POSIXt[rows])
df$open[i]<-trade$price[rows][k]
}


#close

for(i in c(1 :length(minute)) )
{
rows<-which(trade$minute_POSIXt==minute[i])
k<-which.max(trade$time_POSIXt[rows])
df$close[i]<-trade$price[rows][k]
}


df1 <- merge(df, high, by="minute")
df2 <- merge(df1, low, by="minute")


df <- df2


save(df,file = "HLOC_askbidVol_perminute.Rda")


return
}




