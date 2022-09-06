
rm(list=ls())


humdata<-read.csv("..\\..\\..\\..\\empowermentexploration\\resources\\playerdata\\data\\alchemy2HumanDataMemory.csv")
#humdata<-read.csv("..\\..\\..\\..\\empowermentexploration\\resources\\playerdata\\data\\tinyalchemyHumanDataMemory.csv")
#humdata<-read.csv("..\\..\\..\\..\\empowermentexploration\\resources\\playerdata\\data\\tinypixelsHumanDataMemory.csv")

sortedhumdata<-humdata[order(humdata$id,-humdata$trial),]
maxvalues <- sortedhumdata[!duplicated(sortedhumdata$id),]                  

#check how many people play over certain number of trials and find over a certain number of elements. 
# numbers in comments are results for la2

sum(maxvalues$trial>10)  #24719 
sum(maxvalues$trial>50)   #15622
sum(maxvalues$trial>100)   #9949
sum(maxvalues$trial>500)   #1785
sum(maxvalues$trial>1000)   #563
sum(maxvalues$trial>10000) #16
sum(maxvalues$trial>50000) #1 #person19567

sum(maxvalues$inventory>4) #all #meaning everybody, even when playing only 1 trial, found at least one element
sum(maxvalues$inventory>10) #24317
sum(maxvalues$inventory>20) #18167
sum(maxvalues$inventory>50) #7845
sum(maxvalues$inventory>100) #3206
sum(maxvalues$inventory>200) #1247
sum(maxvalues$inventory>300) #628
sum(maxvalues$inventory>400) #352
sum(maxvalues$inventory>500) #177
sum(maxvalues$inventory>600) #88
sum(maxvalues$inventory>700) #33
which(maxvalues$inventory>719) #9 #meaning 9 people found all 720 elements. 

mean(maxvalues$trial)
sd(maxvalues$trial)

mean(maxvalues$inventory)
sd(maxvalues$inventory)
var(maxvalues$inventory)
