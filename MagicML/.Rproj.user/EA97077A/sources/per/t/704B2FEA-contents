
if(!require(installr)) {
  install.packages("installr"); require(installr)} #load / install+load installr

# using the package:
updateR() # this will start the updating process of your R installation.  It will check for newer versions, and if one is available, will guide you through the decisions you'd need to make.


install.packages("rjson")
# Load the package required to read JSON files.
library("rjson")

# Give the input file name to the function.
default <- fromJSON(file = "C:/Users/Jane/source/repos/MagicCMCPredictor/data/scryfall-default-cards.json")

rm(result)
names(default[[2]])
filtered<-c("mana_cost","cmc","name","released_at","type_line","oracle_text","colors",
            "color_identity","reserved","rarity","set_name","set_type","set","reprint","story_spotlight")
            
legal<-"legality"
seq5<-seq(from=1,to=5,by=1)
filtered2<-default[[2]][filtered]
filtered2DF<-data.frame(t(filtered2))
filteredDF<-data.frame()
smallList<-default[filtered]
install.packages("microbenchmark")
library(microbenchmark)

namesOfFilteredInitial<-names(filtered2)
sum(namesOfFiltered2 %in% namesOfFilteredInitial)

filtered2FaceNames<-c("mana_cost","cmc","name","released_at","type_line","card_face","colors",
                      "color_identity","reserved","rarity","set_name","set_type","set","reprint","story_spotlight",
                      "power","toughness")

namesOfFilteredInitial<-c("mana_cost","cmc","name","released_at","type_line","oracle_text","colors",
            "color_identity","reserved","rarity","set_name","set_type","set","reprint","story_spotlight",
            "power","toughness")

filtered2Face<-NULL
filtered2DF<-NULL
j<-1

for(i in 30001:46923){
  filtered2<-default[[i]][filtered]
  namesOfFiltered2<-names(filtered2)
  if (sum(namesOfFiltered2 %in% namesOfFilteredInitial)==17){
    filtered2DF<-rbind(filtered2DF,data.frame(t(filtered2)))
  }
}

?saveRDS
saveRDS(filtered2DF,file="filtered2DF.rds")
saveRDS(filtered2Face,file="filtered2Face.rds")

##try it the tidyverse way
install.packages("tidyverse")
library(tidyverse)
#tibbleDefault<-as_tibble(default,.name_repair = "minimal")
#tibbleDefault<-as_tibble(filtered2DF)


dim(filtered2DF)
#converted mana cost vs ypower and toughness?
#add power and tougness

powerAndToughnessNames<-c("power","toughness")
#land cards with no power and toughness
landcards<-filtered2DF[1:5,]

#check how cmc vs power and toughness

save(filtered2DF,file="filtered2DFwithPowerToughness.RData")

library(ggplot2)
filtered2Tib<-as_tibble(filtered2DF)

sum(is.numeric(filtered2DF$power))
str(filtered2DF$power)
filtered2DF$powerNum<-as.numeric(filtered2DF$power)

filtered2DFpowerNA<-filtered2DF[!is.na(filtered2DF$power),]
filtered2DFpowerNA<-filtered2DF[!is.na(filtered2DF$power),]
filtered2DFpowerNA2<-filtered2DF[!is.na(filtered2DF$powerNum),]

#look at the power Num>25's
index25<-filtered2DFpowerNA2$power>25
head(filtered2DFpowerNA[nas,]       )
sum(index25)
nas<-(is.na(index25))

ggplot(filtered2DFpowerNA2,aes(x=as.numeric(cmc),y=powerNum))+geom_point()
ggplot(filtered2DFpowerNA2,aes(x=as.numeric(cmc),y=as.numeric(toughness)))+geom_point()


as_tibble(filtered2DFpowerNA2)
