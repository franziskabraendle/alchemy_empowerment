library(lmerTest)
library(ggplot2)

rm(list=ls())

la2<-read.csv("\\LittleAlchemyCode_clean_2022_02\\empowerment-main\\empowermentexploration\\data\\gametree\\element_empowerment\\alchemy2_element_empowerment_dataframe.csv") #original dataset
ta<-read.csv("\\LittleAlchemyCode_clean_2022_02\\empowerment-main\\empowermentexploration\\data\\gametree\\element_empowerment\\tinyalchemy_element_empowerment_dataframe.csv") #original dataset
hist(la2$emp_value_true, 20)
hist(ta$emp_value_true, 20)

la2_comb <- read.csv("\\LittleAlchemyCode_clean_2022_02\\empowerment-main\\empowermentexploration\\resources\\littlealchemy\\data\\trueemp_table_la2.csv")
ta_comb <- read.csv("\\LittleAlchemyCode_clean_2022_02\\empowerment-main\\empowermentexploration\\resources\\littlealchemy\\data\\trueemp_table_ta.csv")
hist(la2_comb$Trueemp, 20)
hist(ta_comb$Trueemp, 20)

length(which(la2_comb$Trueemp==-1)) #256252 combinations unsuccessfull
la2_comb_clean<-la2_comb[!la2_comb$Trueemp==-1,] # 3308 remaining
length(which(la2_comb_clean$Trueemp==0)) #669 combinations producing only final elements. (~20%)

length(which(ta_comb$Trueemp==-1)) #145207 combinations unsuccessfull
ta_comb_clean<-ta_comb[!ta_comb$Trueemp==-1,] # 863 remaining
length(which(ta_comb_clean$Trueemp==0)) #389 combinations producing only final elements. (~45%)

hist(la2_comb_clean$Trueemp, breaks = 100)
hist(ta_comb_clean$Trueemp, breaks = 65) #way steeper
#Probably the cause for the different amounts of loss when training the new emp model