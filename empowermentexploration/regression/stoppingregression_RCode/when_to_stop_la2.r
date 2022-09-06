rm(list=ls())

library(readr)
library(plyr)
library(data.table)
library(lmerTest)

#uncomment to recreate whentostopdataframe, leave uncommented for the analysis

# d<-read_csv('../../../empowermentexploration/resources/playerdata/data/alchemy2HumanDataMemory.csv')
# emp<-read_csv('../../../empowermentexploration/data/gametree/element_empowerment/alchemy2_element_empowerment_dataframe.csv')
# 
# #d$results<-as.numeric(ifelse(d$results=='-1', '-1', gsub("\\[|\\]", "",d$results)))
# d$results<-ifelse(d$results=='-1', '-1', gsub("\\[|\\]", "",d$results))
# #can also use predicted here. 
# 
# d$numberelements <- 1 + nchar(gsub("[^,]", "", d$results))
# d$numberelements[d$results==-1]<-0 
# 
# d$empowerment<- -1
# 
# 
# for (i in 1:nrow(d)){
#   if(i %%100000 ==0){
#     print(i)
#   }
#   
#   if(d$numberelements[i] == 0){
#     d$empowerment[i] <- 0
#   
#   } else if(d$numberelements[i] == 1){
#     d$empowerment[i] <- emp$emp_value_true[emp$index == as.numeric(d$results[i])]
#   
#   } else if(d$numberelements[i] == 2){
#     element1 <- sapply(strsplit(d$results[i], ","), "[", 1)
#     element2 <- sapply(strsplit(d$results[i], ", "), "[", 2)
#     d$empowerment[i] <- emp$emp_value_true[emp$index == as.numeric(element1)] + emp$emp_value_true[emp$index == as.numeric(element2)]
#   } else if(d$numberelements[i] == 3){
#     element1 <- sapply(strsplit(d$results[i], ","), "[", 1)
#     element2 <- sapply(strsplit(d$results[i], ", "), "[", 2)
#     element3 <- sapply(strsplit(d$results[i], ", "), "[", 3)
#     d$empowerment[i] <- emp$emp_value_true[emp$index == as.numeric(element1)] + emp$emp_value_true[emp$index == as.numeric(element2)] + emp$emp_value_true[emp$index == as.numeric(element3)]
#   } else if(d$numberelements[i] == 4){
#     element1 <- sapply(strsplit(d$results[i], ","), "[", 1)
#     element2 <- sapply(strsplit(d$results[i], ", "), "[", 2)
#     element3 <- sapply(strsplit(d$results[i], ", "), "[", 3)
#     element4 <- sapply(strsplit(d$results[i], ", "), "[", 4)
#     d$empowerment[i] <- emp$emp_value_true[emp$index == as.numeric(element1)] + emp$emp_value_true[emp$index == as.numeric(element2)] + emp$emp_value_true[emp$index == as.numeric(element3)] + emp$emp_value_true[emp$index == as.numeric(element4)]
#   } else if(d$numberelements[i] == 5){
#     element1 <- sapply(strsplit(d$results[i], ","), "[", 1)
#     element2 <- sapply(strsplit(d$results[i], ", "), "[", 2)
#     element3 <- sapply(strsplit(d$results[i], ", "), "[", 3)
#     element4 <- sapply(strsplit(d$results[i], ", "), "[", 4)
#     element5 <- sapply(strsplit(d$results[i], ", "), "[", 5)
#     d$empowerment[i] <- emp$emp_value_true[emp$index == as.numeric(element1)] + emp$emp_value_true[emp$index == as.numeric(element2)] + emp$emp_value_true[emp$index == as.numeric(element3)] + emp$emp_value_true[emp$index == as.numeric(element4)] + emp$emp_value_true[emp$index == as.numeric(element5)]
#   } else if(d$numberelements[i] == 6){
#     element1 <- sapply(strsplit(d$results[i], ","), "[", 1)
#     element2 <- sapply(strsplit(d$results[i], ", "), "[", 2)
#     element3 <- sapply(strsplit(d$results[i], ", "), "[", 3)
#     element4 <- sapply(strsplit(d$results[i], ", "), "[", 4)
#     element5 <- sapply(strsplit(d$results[i], ", "), "[", 5)
#     element6 <- sapply(strsplit(d$results[i], ", "), "[", 6)
#     d$empowerment[i] <- emp$emp_value_true[emp$index == as.numeric(element1)] + emp$emp_value_true[emp$index == as.numeric(element2)] + emp$emp_value_true[emp$index == as.numeric(element3)] + emp$emp_value_true[emp$index == as.numeric(element4)] + emp$emp_value_true[emp$index == as.numeric(element5)] + emp$emp_value_true[emp$index == as.numeric(element6)]
#   }
# }

# write.csv(d,'../../../empowermentexploration/regression/stoppingregression_RCode/whentostopdataframe.csv', row.names = FALSE)

d<-read_csv('../../../empowermentexploration/data/regression/whentostopdataframe.csv')

  numberofrounds <-1

  #calculate average success of last two rounds (0, 0.5 or 1) and scale it. 
  d$succ<-as.numeric(scale(ave(d$success, d$id, FUN=function(x){frollmean(x, n=numberofrounds)})))

  #calculate average true empowerment of last two rounds and scale it. 
  d$emp<-as.numeric(scale(ave(log(d$empowerment+1), d$id, FUN=function(x){frollmean(x, n=numberofrounds)})))

  #set variable to 0 if player's stop after current trial, else set to 1. 
  d$continue<-ifelse(d$trial==ave(d$trial, d$id, FUN=length)-1, 0, 1)

  d$trialScaled<-scale(d$trial)
  d$inventoryScaled<-scale(d$inventory)

  m1<-glmer(continue~succ+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
  summary(m1)
  AIC(m1)

  m2<-glmer(continue~emp+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
  summary(m2)
  AIC(m2)

  m3<-glmer(continue~emp+succ+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
  summary(m3)
  AIC(m3)
  
  m3a<-glmer(continue~emp+succ+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
  summary(m3a)
  AIC(m3a)
  
  m3b<-glmer(continue~emp+succ+inventoryScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
  summary(m3b)
  AIC(m3b)
  
  m3c<-glmer(continue~emp+succ+inventoryScaled+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
  summary(m3c)
  AIC(m3c)

#uncomment for additional analyses
 
# m1a<-glmer(continue~succ+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(m1a)
# AIC(m1a)
# 
# #m2a<-glmer(continue~emp+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "Nelder_Mead"))
# m2a<-glmer(continue~emp+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(m2a)
# AIC(m2a)
# 
# #m3a<-glmer(continue~emp+succ+trialScaled+(1|id), family='binomial', data=d, nAGQ=1, control=glmerControl(optimizer = "Nelder_Mead"))
# m3a<-glmer(continue~emp+succ+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(m3a)
# AIC(m3a)
# 
# m1b<-glmer(continue~succ+inventoryScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(m1b)
# AIC(m1b)
# 
# m2b<-glmer(continue~emp+inventoryScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(m2b)
# AIC(m2b)
# 
# m3b<-glmer(continue~emp+succ+inventoryScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(m3b)
# AIC(m3b)
# 
# m1c<-glmer(continue~succ+inventoryScaled+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "Nelder_Mead")) #DOES NOT WORK FOR LA2, even with other optimizers.
# #m1c<-glmer(continue~succ+inventoryScaled+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap")) #DOES NOT WORK FOR LA2, even with other optimizers.
# summary(m1c)
# AIC(m1c)
# 
# m2c<-glmer(continue~emp+inventoryScaled+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(m2c)
# AIC(m2c)
# 
# m3c<-glmer(continue~emp+succ+inventoryScaled+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(m3c)
# AIC(m3c)
# 


