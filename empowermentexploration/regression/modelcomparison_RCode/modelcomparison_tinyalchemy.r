library(lmerTest)
library(ggplot2)

rm(list=ls())

ta<-read.csv('..\\..\\..\\empowermentexploration\\data\\regression\\20211011-1425-tinyalchemy-valuedifferences-human-1.csv') #original dataset

tadf<-data.frame(trial=scale(ta$trial),
                  id=paste(ta$id), 
                  cbu=scale(ta$delta_cbu),
                  emp=scale(ta$delta_emp),
                  bin=scale(ta$delta_bin),
                  cbv=scale(ta$delta_cbv),
                  truebin=scale(ta$delta_truebin),
                  trueemp=scale(ta$delta_trueemp),
                  decision=ta$decision)


## BOTTOM UP ANALYSIS
# get model with single models as fixed effect
me <- glmer(decision ~ -1 + emp + trial + trial*emp + (1 | id), data=tadf, family="binomial")
summary(me)

mv <- glmer(decision ~ -1 + cbv + trial + trial*cbv + (1 | id), data=tadf, family="binomial")
summary(mv)

mb <- glmer(decision ~ -1 + bin + trial + trial*bin + (1 | id), data=tadf, family="binomial")
summary(mb)

mu <- glmer(decision ~ -1 + cbu + trial + trial*cbu + (1 | id), data=tadf, family="binomial")
summary(mu)

# get model with empowerment and binary as fixed effect
meb <- glmer(decision ~ -1 + emp + bin + trial + trial*emp + trial*bin + (1 | id), data=tadf, family="binomial")
summary(meb)

# get model with empowerment and CBU as fixed effect
meu <- glmer(decision ~ -1 + emp + cbu + trial + trial*emp + trial*cbu + (1 | id), data=tadf, family="binomial")
summary(meu)

# get model with binary and CBU as fixed effect
mub <- glmer(decision ~ -1 + bin + cbu + trial + trial*bin + trial*cbu + (1 | id), data=tadf, family="binomial")
summary(mub)

# get model with empowerment and binary and CBU as fixed effect
meub <- glmer(decision ~ -1 + emp + bin + cbu + trial + trial*emp + trial*bin + trial*cbu + (1 | id), data=tadf, family="binomial")
summary(meub)


trueemp_regression <-glmer(decision ~ -1 + trueemp + trial + trial*trueemp + (1|id), data=tadf, family="binomial")
summary(trueemp_regression)

trueemp_regression_wot <-glmer(decision ~ -1 + trueemp + (1|id), data=tadf, family="binomial")
summary(trueemp_regression_wot)

truebin_regression <-glmer(decision ~ -1 + truebin + trial + trial*truebin + (1|id), data=tadf, family="binomial")
summary(truebin_regression)

truecomb_regression <-glmer(decision ~ -1 + truebin + trueemp + trial + trial*truebin + trial*trueemp + (1|id), data=tadf, family="binomial")
summary(truecomb_regression)

truecomb_regression_wot <-glmer(decision ~ -1 + trueemp + truebin + (1|id), data=tadf, family="binomial")
summary(truecomb_regression_wot)
