library(lmerTest)
library(ggplot2)

rm(list=ls())

tp<-read.csv('..\\..\\..\\empowermentexploration\\data\\regression\\20211011-1434-tinypixels-valuedifferences-human-1.csv')

tpdf<-data.frame(trial=scale(tp$trial),
                  id=paste(tp$id), 
                  cbu=scale(tp$delta_cbu),
                  emp=scale(tp$delta_emp),
                  bin=scale(tp$delta_bin),
                  cbv=scale(tp$delta_cbv),
                  decision=tp$decision)

tpdf_fullregression<-glmer(decision~-1+cbu+emp+trial+trial*cbu+trial*emp+(1|id), family='binomial', data=tpdf, nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
tpdf_fullregression_summary<-summary(tpdf_fullregression)
tpdf_fullregression_summary
tpdf_fullregression_m<-tpdf_fullregression_summary$coefficients[1:2,1]
tpdf_fullregression_se<-tpdf_fullregression_summary$coefficients[1:2,2]

dataforplot_tpdf_fullregression<-data.frame(mu=tpdf_fullregression_m, ci=1.96*tpdf_fullregression_se, 
               model=rep(c('Uncertainty', 'Empowerment')))


#limits with 95% CIs
limits <- aes(ymax = mu + ci, ymin= mu - ci)

#plot
plot_tpdf_fullregression <- ggplot(dataforplot_tpdf_fullregression, aes(x=model, y=mu)) + 
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
  #labs
  xlab("Model")+
  ylab(expression(beta))+
  #title
  ggtitle("")+
  #adjust text size
  theme(text = element_text(size=21,  family="sans"))+
  #no legend
  theme(legend.position = "none")

plot_tpdf_fullregression


# 
# 
# ## BOTTOM UP ANALYSIS
# # get model with single models as fixed effect
# me <- glmer(decision ~ -1 + emp + trial + trial*emp + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(me)
# 
# mv <- glmer(decision ~ -1 + cbv + trial + trial*cbv + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(mv)
# 
# mb <- glmer(decision ~ -1 + bin + trial + trial*bin + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(mb)
# 
# mu <- glmer(decision ~ -1 + cbu + trial + trial*cbu + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(mu)
# 
# # get model with empowerment and binary as fixed effect
# meb <- glmer(decision ~ -1 + emp + bin + trial + trial*emp + trial*bin + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(meb)
# 
# # get model with empowerment and CBU as fixed effect
# meu <- glmer(decision ~ -1 + emp + cbu + trial + trial*emp + trial*cbu + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(meu)
# 
# # get model with binary and CBU as fixed effect
# mub <- glmer(decision ~ -1 + bin + cbu + trial + trial*bin + trial*cbu + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
# summary(mub)
# 
# # get model with empowerment and binary and CBU as fixed effect
# meub <- glmer(decision ~ -1 + emp + bin + cbu + trial + trial*emp + trial*bin + trial*cbu + (1 | id), data=tpdf, family="binomial", nAGQ=0, control=glmerControl(optimizer = "nloptwrap"))
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
# 
# emponbin <- lmer(emp ~ -1 + bin + (1|id), data = tpdf)
# summary(emponbin)

