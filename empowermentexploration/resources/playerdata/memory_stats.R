library(lmerTest)
library(ggplot2)
library(dplyr)

rm(list=ls())

#stats for the different datasets how many trials were excluded because we assume full memory

tp_raw<-read.csv("\\LittleAlchemyCode_clean_2022_02\\empowerment-main\\empowermentexploration\\resources\\playerdata\\data\\tinypixelsHumanData.csv") #original dataset
tp_memory<-read.csv("\\LittleAlchemyCode_clean_2022_02\\empowerment-main\\empowermentexploration\\resources\\playerdata\\data\\tinypixelsHumanDataMemory.csv") #dataset with duplicates excluded

numberexcluded <- nrow(tp_raw) - nrow(tp_memory)
numberexcluded
tp_raw_trialsperid <- tapply(tp_raw$trial, tp_raw$id, max)
tp_memory_trialsperid <- tapply(tp_memory$trial, tp_memory$id, max)

tp_deleted_rows <- tp_raw_trialsperid - tp_memory_trialsperid
tp_deleted_rows_proportion <- tp_deleted_rows / tp_raw_trialsperid
hist(tp_deleted_rows_proportion)
mean(tp_deleted_rows_proportion)
sd(tp_deleted_rows_proportion)

###

ta_raw<-read.csv("\\LittleAlchemyCode_clean_2022_02\\empowerment-main\\empowermentexploration\\resources\\playerdata\\data\\tinyalchemyHumanData.csv") #original dataset
ta_memory<-read.csv("\\LittleAlchemyCode_clean_2022_02\\empowerment-main\\empowermentexploration\\resources\\playerdata\\data\\tinyalchemyHumanDataMemory.csv") #dataset with duplicates excluded

numberexcluded <- nrow(ta_raw) - nrow(ta_memory)
numberexcluded
ta_raw_trialsperid <- tapply(ta_raw$trial, ta_raw$id, max)
ta_memory_trialsperid <- tapply(ta_memory$trial, ta_memory$id, max)

ta_deleted_rows <- ta_raw_trialsperid - ta_memory_trialsperid
ta_deleted_rows_proportion <- ta_deleted_rows / ta_raw_trialsperid
hist(ta_deleted_rows_proportion)
mean(ta_deleted_rows_proportion)
sd(ta_deleted_rows_proportion)

###

la2_raw<-read.csv("\\LittleAlchemyCode_clean_2022_02\\empowerment-main\\empowermentexploration\\resources\\playerdata\\data\\alchemy2HumanData.csv") #original dataset
la2_memory<-read.csv("\\LittleAlchemyCode_clean_2022_02\\empowerment-main\\empowermentexploration\\resources\\playerdata\\data\\alchemy2HumanDataMemory.csv") #original dataset

numberexcluded <- nrow(la2_raw) - nrow(la2_memory)
numberexcluded
la2_raw_trialsperid <- tapply(la2_raw$trial, la2_raw$id, max)
la2_memory_trialsperid <- tapply(la2_memory$trial, la2_memory$id, max)

la2_deleted_rows <- la2_raw_trialsperid - la2_memory_trialsperid
la2_deleted_rows_proportion <- la2_deleted_rows / la2_raw_trialsperid
la2_deleted_rows_proportion
hist(la2_deleted_rows_proportion)
mean(la2_deleted_rows_proportion, na.rm = TRUE)
sd(la2_deleted_rows_proportion, na.rm = TRUE)
