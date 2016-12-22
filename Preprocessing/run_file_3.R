
install.packages("TTR")
install.packages("base")
install.packages("caTools")

library(caTools)
library(TTR)

## set directory
rm(list=ls())
user_home <- "/Users/angela/Desktop/project"
setwd(user_home)

##create folders for different data
data <- list.files(file.path(user_home, data))
data_sets <- c(list.files(file.path(user_home, data)))

setwd(user_home)

source(file.path(user_home, "bda_project_code","high_low_close_open_1.r"))
source(file.path(user_home, "bda_project_code","indicator_return_generate_2.r"))

for (dataname in data1){
    data1_HOLC_askbidVol(dataname)
    
    EMApara_list<-c(20)
    RMpara_list<-c(3)
    setwd(file.path(user_home,"result",dataname))
    load(file="HLOC_askbidVol_perminute.Rda")
    load(file="minute_date_levels.Rda")
    

    generate_indicator()
    
    duration_list <- c(5)
    delay_list <- c(1)
    generate_return()
    
}


write.csv(indicator_set$ask_vol,indicator_set$bid_vol,indicator_set$BSP_Smooth_EMA20_RunMean3, file = "features_add.csv")
test=data.frame(df$amt,df$open,df$close,df$low,df$high, return$ret_duration_5_TimeDelay_1)
write.csv(test, file = "HI1_test.csv")
write.csv(test, file = "IFB1_test.csv")
write.csv(test, file = "XU1_test.csv")

load("/Users/angela/Desktop/project/result_to_use/HC1_JulAug.txt/indicator_set.Rda")
setwd("/Users/angela/Desktop/columbia_life/big_data_analytics/project")
write.csv(indicator_set$BSP_Smooth_EMA20_RunMean3, file = "HC1_BSP.csv")



load("/Users/angela/Desktop/project/result_to_use/HC1_JulAug.txt/indicator_set.Rda")
setwd("/Users/angela/Desktop/columbia_life/big_data_analytics/project")
write.csv(indicator_set$BSP_Smooth_EMA20_RunMean3, file = "HC1_BSP.csv")


load("/Users/angela/Desktop/project/result_to_use/HI1_JulAug.txt/indicator_set.Rda")
setwd("/Users/angela/Desktop/columbia_life/big_data_analytics/project")
write.csv(indicator_set$BSP_Smooth_EMA20_RunMean3, file = "HI1_BSP.csv")


load("/Users/angela/Desktop/project/result_to_use/IFB1_JulAug.txt/indicator_set.Rda")
setwd("/Users/angela/Desktop/columbia_life/big_data_analytics/project")
write.csv(indicator_set$BSP_Smooth_EMA20_RunMean3, file = "IFB1_BSP.csv")


