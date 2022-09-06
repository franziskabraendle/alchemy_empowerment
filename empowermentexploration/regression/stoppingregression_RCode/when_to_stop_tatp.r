rm(list=ls())

library(readr)
library(plyr)
library(data.table)
library(lmerTest)

#uncomment for Tiny Alchemy
d<-read_csv('../../../empowermentexploration/resources/playerdata/data/tinyalchemyHumanDataMemory.csv')
emp<-read_csv('../../../empowermentexploration/data/gametree/element_empowerment/tinyalchemy_element_empowerment_dataframe.csv')

#uncomment for Tiny Pixels
#d<-read_csv('../../../empowermentexploration/resources/playerdata/data/tinypixelsHumanDataMemory.csv')
#emp<-read_csv('../../../empowermentexploration/data/gametree/element_empowerment/tinypixels_element_empowerment_dataframe.csv')


d$results<-ifelse(d$results=='-1', '-1', gsub("\\[|\\]", "",d$results))

d$numberelements <- 1 + nchar(gsub("[^,]", "", d$results))
d$numberelements[d$results==-1]<-0 

d$empowerment<- -1
for (i in 1:nrow(emp)){
  d$empowerment[d$results==emp$index[i]]<-emp$emp_value_true[i]
}

d$empowerment[d$results == -1] <- 0

numberofrounds <-2

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

m1a<-glmer(continue~succ+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(m1a)
AIC(m1a)

m2a<-glmer(continue~emp+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(m2a)
AIC(m2a)

m3a<-glmer(continue~emp+succ+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(m3a)
AIC(m3a)

m1b<-glmer(continue~succ+inventoryScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(m1b)
AIC(m1b)

m2b<-glmer(continue~emp+inventoryScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(m2b)
AIC(m2b)

m3b<-glmer(continue~emp+succ+inventoryScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(m3b)
AIC(m3b)

m1c<-glmer(continue~succ+inventoryScaled+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(m1c)
AIC(m1c)

m2c<-glmer(continue~emp+inventoryScaled+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(m2c)
AIC(m2c)

m3c<-glmer(continue~emp+succ+inventoryScaled+trialScaled+(1|id), family='binomial', data=d, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(m3c)
AIC(m3c)
