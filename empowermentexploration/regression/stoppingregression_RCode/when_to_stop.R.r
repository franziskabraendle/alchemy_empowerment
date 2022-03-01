rm(list=ls())

library(readr)
library(plyr)
library(data.table)
library(lmerTest)

d<-read_csv('../../../empowermentexploration/resources/playerdata/data/alchemy2HumanDataMemory.csv')
emp<-read_csv('../../../empowermentexploration/data/gametree/element_empowerment/alchemy2_element_empowerment_dataframe.csv')

#d<-read_csv('../../../empowermentexploration/resources/playerdata/data/tinyalchemyHumanDataMemory.csv')
#emp<-read_csv('../../../empowermentexploration/data/gametree/element_empowerment/tinyalchemy_element_empowerment_dataframe.csv')

#d<-read_csv('../../../empowermentexploration/resources/playerdata/data/tinypixelsHumanDataMemory.csv')
#emp<-read_csv('../../../empowermentexploration/data/gametree/element_empowerment/tinypixels_element_empowerment_dataframe.csv')

d$results<-as.numeric(ifelse(d$results=='-1', '-1', gsub("\\[|\\]", "",d$results)))

#can also use predicted here. 
d$empowerment<-0
for (i in 1:nrow(emp)){
  d$empowerment[d$results==emp$index[i]]<-emp$emp_value_true[i]
}

#calculate average success of last two rounds (0, 0.5 or 1) and scale it. 
d$succ<-as.numeric(scale(ave(d$success, d$id, FUN=function(x){frollmean(x, n=2)})))

#calculate average true empowerment of last two rounds and scale it. 
d$emp<-as.numeric(scale(ave(log(d$empowerment+1), d$id, FUN=function(x){frollmean(x, n=2)})))

#set variable to 0 if player's stop after current trial, else set to 1. 
d$continue<-ifelse(d$trial==ave(d$trial, d$id, FUN=length)-1, 0, 1)

#assign uncertainty value 1 if at least one elment of combination hasn't been used before, otherwise 0

# for(i in 0:max(d$id)){
#   subsetid <- subset(d, id == i)
#   subsetid$ uncertainty <-0
#   subsetid$uncertainty[1] <- 1
#   if(nrow(subsetid)<2){
#     next
#   }
#   for(j in 2: nrow(subsetid)){
#     firstused = FALSE
#     secondused=FALSE
#     for(k in 1: (j-1)){
#       if(subsetid$first[j]==subsetid$first[k] | subsetid$first[j]==subsetid$second[k]){
#         firstused = TRUE
#       } 
#       if(subsetid$second[j]==subsetid$first[k] | subsetid$second[j]==subsetid$second[k]){
#         secondused = TRUE
#       }
#     }
#     if(secondused == FALSE | firstused == FALSE){
#       subsetid$uncertainty[j] = 1
#     }
#   }
#   if(i == 0){
#     dwithuncertainty <- subsetid
#   }
#   else{
#     dwithuncertainty <- rbind(dwithuncertainty,subsetid)
#   }
# }


m1<-glmer(continue~succ+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(m1)
AIC(m1)

m2<-glmer(continue~emp+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(m2)
AIC(m2)

m3<-glmer(continue~emp+succ+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(m3)
AIC(m3)

#m4<-glmer(continue~uncertainty+(1|id), family='binomial', data=dwithuncertainty, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
#summary(m4)
#AIC(m4)

#m5<-glmer(continue~uncertainty+emp+(1|id), family='binomial', data=dwithuncertainty, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
#summary(m5)
#AIC(m5)

#m6<-glmer(continue~uncertainty+succ+(1|id), family='binomial', data=dwithuncertainty, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
#summary(m6)
#AIC(m6)

#m7<-glmer(continue~uncertainty+emp+succ+(1|id), family='binomial', data=dwithuncertainty, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
#summary(m7)
#AIC(m7)