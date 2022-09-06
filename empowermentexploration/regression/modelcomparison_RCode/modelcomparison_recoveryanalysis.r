library(lmerTest)
library(ggplot2)

rm(list=ls())

la2<-read.csv("..\\..\\..\\empowermentexploration\\data\\regression\\20220901-1115-alchemy2-valuedifferences-emp-1.csv")
#la2<-read.csv("..\\..\\..\\empowermentexploration\\data\\regression\\20220901-1237-alchemy2-valuedifferences-cbu-1.csv")
#la2<-read.csv("..\\..\\..\\empowermentexploration\\data\\regression\\20220901-1207-alchemy2-valuedifferences-base-1.csv")

la2small<-subset(la2, trial<200)

# la2df<-data.frame(trial=scale(la2$trial),
#                   id=paste(la2$id), 
#                   cbu=scale(la2$delta_cbu),
#                   emp=scale(la2$delta_emp),
#                   bin=scale(la2$delta_bin),
#                   cbv=scale(la2$delta_cbv),
#                   decision=la2$decision)

la2dfsmall<-data.frame(trial=scale(la2small$trial),
                  id=paste(la2small$id), 
                  cbu=scale(la2small$delta_cbu),
                  emp=scale(la2small$delta_emp),
                  bin=scale(la2small$delta_bin),
                  cbv=scale(la2small$delta_cbv),
                  decision=la2small$decision)

#important for cbu dataset, also change cbu to cbu2 in regression when using the cbu dataset
set.seed(1234) #only relevant for the noise we are adding to the cbu model. 
la2dfsmall$cbu2 <- la2dfsmall$cbu + rnorm(nrow(la2dfsmall),0,0.05)

## BOTTOM UP ANALYSIS
# get model with single models as fixed effect
me <- glmer(decision ~ -1 + emp + (1 | id), data=la2dfsmall, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(me)

mu <- glmer(decision ~ -1 + cbu + (1 | id), data=la2dfsmall, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(mu)

# get model with empowerment and CBU as fixed effect
meu <- glmer(decision ~ -1 + emp + cbu + (1 | id), data=la2dfsmall, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
summary(meu)




