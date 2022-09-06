library(lmerTest)
library(ggplot2)

rm(list=ls())

imushum<-read.csv("..\\..\\..\\..\\empowermentexploration\\resources\\playerdata\\data\\dataImUs\\20220826-1805-alchemy2-immediateusageWithoutLog-Memory-human.csv") 
imusran<-read.csv("..\\..\\..\\..\\empowermentexploration\\resources\\playerdata\\data\\dataImUs\\20220826-1805-alchemy2-immediateusageWithoutLog-Memory-random.csv") # random, 1000 trials

#imushum<-read.csv("..\\..\\..\\..\\empowermentexploration\\resources\\playerdata\\data\\dataImUs\\20220826-1805-tinyalchemy-immediateusageWithoutLog-Memory-human.csv") 
#imusran<-read.csv("..\\..\\..\\..\\empowermentexploration\\resources\\playerdata\\data\\dataImUs\\20220826-1805-tinyalchemy-immediateusageWithoutLog-Memory-random.csv") # random, 1000 trials

#imushum<-read.csv("..\\..\\..\\..\\empowermentexploration\\resources\\playerdata\\data\\dataImUs\\20220826-1805-tinypixels-immediateusageWithoutLog-Memory-human.csv") 
#imusran<-read.csv("..\\..\\..\\..\\empowermentexploration\\resources\\playerdata\\data\\dataImUs\\20220826-1805-tinypixels-immediateusageWithoutLog-Memory-random.csv") # random, 1000 trials


humdf<-data.frame(emp = (c(scale(imushum$emp_raw))),
                  prob = c(scale(imushum$usage_prob)),
                  trials = c(scale(imushum$tri_ave)),
                  inventory = c(scale(imushum$inv_ave)))

randf<-data.frame(emp = (c(scale(imusran$emp_raw))),
                  prob = c(scale(imusran$usage_prob)),
                  trials = c(scale(imusran$tri_ave)),
                  inventory = c(scale(imusran$inv_ave)))

humreg_simple <- lm(prob ~ emp, data = humdf)
summary(humreg_simple)
humreg_full <- lm(prob ~ emp + trials + inventory + trials*emp + inventory*emp , data = humdf)
summary(humreg_full)

ranreg_simple <- lm(prob ~ emp, data = randf )
summary(ranreg_simple)
ranreg_full <- lm(prob ~ emp + trials + inventory  + trials*emp + inventory*emp ,data = randf )
summary(ranreg_full)
