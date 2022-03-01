library(lmerTest)
library(ggplot2)

rm(list=ls())


dta<-read.csv('..\\..\\..\\empowermentexploration\\data\\regression\\20211011-1425-tinyalchemy-valuedifferences-human-1.csv')
dtp<-read.csv('..\\..\\..\\empowermentexploration\\data\\regression\\20211011-1434-tinypixels-valuedifferences-human-1.csv')


dat<-data.frame(trial=scale(c(dta$trial, dtp$trial)),
                id=paste(c(dta$id, dtp$id+1000)), 
                cbu=scale(c(dta$delta_cbu, dtp$delta_cbu)),
                emp=scale(c(dta$delta_emp, dtp$delta_emp)),
                bin=scale(c(dta$delta_bin, dtp$delta_bin)),
                decision=c(dta$decision, dtp$decision),
                game=c(rep('alchemy', nrow(dta)) ,rep('pixel', nrow(dtp))))


mfull1<-glmer(decision~-1+cbu+emp+game+game*emp+game*cbu+trial+trial*emp+trial*cbu+(1|id), family='binomial', data=dat)
ms<-summary(mfull1)
alechmym<-ms$coefficients[1:2,1]
alchemyse<-ms$coefficients[1:2,2]
ms

dat$game<-relevel(dat$game, ref='pixel')

mfull2<-glmer(decision~-1+cbu+emp+game+game*emp+game*cbu+trial+trial*emp+trial*cbu+(1|id), family='binomial', data=dat)
ms<-summary(mfull2)
pixelm<-ms$coefficients[1:2,1]
pixelmse<-ms$coefficients[1:2,2]
dp<-data.frame(mu=c(alechmym, pixelm), ci=1.96*c(alchemyse, pixelmse),
               game=rep(c('Tiny Alchemy', 'Tiny Pixels'), each=2),
               model=rep(c('Uncertainty', 'Empowerment'), 2))

ms

#limits with 95% CIs
limits <- aes(ymax = mu + ci, ymin= mu - ci)

#plot
p <- ggplot(dp, aes(x=model, y=mu)) +
  #bars
  geom_bar(position="dodge", stat="identity", width=0.6)+
  #error bars
  geom_errorbar(limits, position="dodge", width=0.25)+
  #points
  geom_point(size=3)+
  #color
  #scale_fill_manual(values = c(cbPalette))+
  #theme
  theme_minimal() +
  #limits
  #scale_y_continuous(limits = c(0,100), expand = c(0, 0)) +
  #two facets
  facet_wrap(~game, nrow=2)+
  #labs
  xlab("Model")+
  ylab(expression(beta))+
  #title
  ggtitle("")+
  #adjust text size
  theme(text = element_text(size=21,  family="sans"))+
  #no legend
  theme(legend.position = "none")

#png('modelcomparison.png', width=350, height=450)
p
dp

# 
# 
# ## BOTTOM UP ANALYSIS - uncomment when more detailed analyses needed
# # get model with single models as fixed effect
# me <- glmer(decision ~ -1 + emp + trial + trial*emp +game+game*emp+game*trial+ (1 | id), data=dat, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(me)
# 
# mb <- glmer(decision ~ -1 + bin + trial + trial*bin +game+game*bin+game*trial+ (1 | id), data=dat, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(mb)
# 
# mu <- glmer(decision ~ -1 + cbu + trial + trial*cbu +game+game*cbu+game*trial+ (1 | id), data=dat, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(mu)
# 
# # get model with empowerment and binary as fixed effect
# meb <- glmer(decision ~ -1 + emp + bin + trial + trial*emp + trial*bin +game+game*emp+game*bin+game*trial+ (1 | id), data=dat, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(meb)
# 
# # get model with empowerment and CBU as fixed effect
# meu <- glmer(decision ~ -1 + emp + cbu + trial + trial*emp + trial*cbu +game+game*emp+game*cbu+game*trial+ (1 | id), data=dat, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(meu)
# 
# # get model with binary and CBU as fixed effect
# mub <- glmer(decision ~ -1 + bin + cbu + trial + trial*bin + trial*cbu +game+game*bin+game*cbu+game*trial+ (1 | id), data=dat, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(mub)
# 
# # get model with empowerment and binary and CBU as fixed effect
# meub <- glmer(decision ~ -1 + emp + bin + cbu + trial + trial*emp + trial*bin + trial*cbu +game+game*emp+game*bin+game*cbu+game*trial+ (1 | id), data=dat, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(meub)
# 
# # compare models
# anova(me, meb)
# anova(mb, meb)
# anova(me, meu)
# anova(mu, meu)
# anova(mb, mub)
# anova(mu, mub)
# anova(mub, meub)
# anova(meu, meub)
# anova(meb, meub)

