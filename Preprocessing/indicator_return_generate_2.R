

#filepath <- file.path(user_home,"result", dataname)
#setwd(filepath)
#load("HLOC_askbidVol_perminute.Rda")


#generate BSP indicator set

generate_indicator <- function(){



    # for test EMApara <- 20
    indicator_name <- paste("BSP_Raw","_EMA", EMApara, sep="")
    
    EMA.para<- function(x) EMA(x, EMApara, ratio=0.1, na.rm=T)
    runmean.para <- function(x) runmean(x, RMpara, align="right")
    
    sp  =(df$high- df$close)+1e-6
    bp =(df$close -df$low)+1e-6
    
    df<-data.frame(df,sp,bp,bpavg=rep(0,length(minute)), spavg=rep(0,length(minute)),vavg=rep(0,length(minute)),nbp= rep(0,length(minute)), nsp=rep(0,length(minute)), nv=rep(0,length(minute)), diff=rep(0,length(minute)), nbfraw = rep(0,length(minute)),nsfraw = rep(0,length(minute)), bspressureRaw = rep(0,length(minute)), bspressureSmooth = rep(0,length(minute)))
    
        rownames(df) <- NULL
        
        
    for(i in c(1 :length(date.level)) )
    {
        #for test  i <- 1
        rows<-which(df$date==date.level[i])
        try(bpavg<-as.vector(EMA.para(df$bp[rows])))
        try(spavg<-as.vector(EMA.para(df$sp[rows])))
        try(vavg <-as.vector(EMA.para(df$amt[rows])))
        nbp <-df$bp[rows]/bpavg
        nsp <- df$sp[rows]/spavg
        nv <-df$amt[rows]/vavg
        diff <- nbp-nsp
        nbfraw <- nbp*nv
        nsfraw <- - nsp * nv
        bspressureRaw <- nbfraw+nsfraw
        
        df$bpavg[rows]<-bpavg
        df$spavg[rows]<-spavg
        df$vavg[rows]<-vavg
        df$nbp[rows]<-nbp
        df$nsp[rows]<-nsp
        df$nv[rows]<-nv
        df$diff[rows]<-diff
        df$nbfraw[rows]<-nbfraw
        df$nsfraw[rows]<-nsfraw
        df$bspressureRaw[rows]<-bspressureRaw
    }
    
    assign(indicator_name, df$bspressureRaw)
    
    indicator_set <- data.frame(get(indicator_name))
    
  
        indicator_name <- paste("BSP_Smooth","_EMA", EMApara, "_RunMean" ,RMpara, sep="")
        
        for(i in c(1 :length(date.level)) )
        {
            rows<-which(df$date==date.level[i])
            bspressureSmooth <-runmean.para(c(df$bspressureRaw[rows]))
            df$bspressureSmooth[rows]<-bspressureSmooth
        }
        assign(indicator_name, df$bspressureSmooth)
        indicator_set <- data.frame(indicator_set,get(indicator_name))
        
    


save(indicator_set,file="indicator_set.Rda")

}

#generate return
generate_return <- function(){
setwd(file.path(user_home,"result", dataname))

#duration of return : x



    ret_name  <- paste("ret_","duration_",duration, sep="")


    for(i in c(1 :length(date.level)))
    {
    
    rows<-which(df$date==date.level[i])
    
    ret_name <- paste("ret_","duration_",duration, sep="")
    
    if (i==1){
        if (duration == duration_list[1]){
            
    return <- data.frame(rep(NA,length(df$minute)))
    volume <- data.frame(rep(NA,length(df$minute)))
    names(return) <- c(ret_name)
    names(volume) <- names(return)


    } else {
        return <- data.frame(return,rep(NA,length(df$minute)))
        volume <-  data.frame(volume,rep(NA,length(df$minute)))
        names(return) <- c(names(return)[-length(names(return))], ret_name)}
        names(volume) <- names(return)

    }
    
    close<-df$close[rows]
    close_p = c(close[-(1:duration)],rep(NA, duration))
    ret <- close_p /close -1
    return[[ret_name]][rows]<- ret
    
    vol_temp <- rep(NA,length(rows))
    for (t in 1:(length(rows)-duration))
    {
        vol_temp[t]<- sum(df$amt[rows][(t+1):(duration+t)], na.rm= TRUE)

        }
    
    volume[[ret_name]][rows]<- vol_temp

    
   
        ret_name  <- paste("ret_","duration_", duration, "_TimeDelay_", delay, sep="")
 
        return <- data.frame(return, rep(NA,length(df$minute)))
        volume <-  data.frame(volume,rep(NA,length(df$minute)))
        names(return) <- c(names(return)[-length(names(return))],ret_name)
        names(volume) <- names(return)



        open_delay<-c(df$open[rows][-(1:(delay+1))], rep(NA,delay+1))
    open_delay_end = c(open_delay[-(1:duration)],rep(NA, duration))
    ret_delay<- open_delay_end/open_delay -1
    
    return[[ret_name]][rows]<- ret_delay
    




}

save(return,file="return.Rda")

}

