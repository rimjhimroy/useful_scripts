library(ggplot2)
library(grid)
theme_set(theme_bw())
library(extrafont)

args<-commandArgs(TRUE)

dat1<-read.csv(file=args[1],sep='\t',header=FALSE)
colnames(dat1)<-c("ID","ID1","Scaf","IDN","IDN_G","QRANGE")


plot_plot<-function(dat1,out_file,qseq_length)
{
###############
# Growth Rate
###############
# Preprocess for annotation text
a <- unique(dat1$Scaf)

pos <- as.integer(as.integer(qseq_length)/2)

##########################################################
#
#########################################################
c2 <- ggplot(dat1,aes(x=QRANGE,y=ID,colour=IDN_G,group=ID1))
c2 <- c2 + geom_line(size=3)

#for (i in 1:length(a))
#{
# N1 <- unique(dat1$ID[dat1$Scaf==a[i]])
# N1 <- N1 + 0.2
# c2 <- c2 + annotate("text", label = a[i] , x = 5000, y = N1, size = 4, colour = "black")
#}


c2 <- c2 + xlab("Query sequence") + ylab("Best BLAST Hits")
c2 <- c2 + xlim(1,as.integer(qseq_length))

#########################################################
# Annotation text
#########################################################
for (i in 1:length(a))
{
N1 <- unique(dat1$ID[dat1$Scaf==a[i]])
N1 <- N1 + 0.2
#c2 <- c2 + annotate("text",label = "Scaffold", x =)
c2 <- c2 + annotate("text", label = a[i] , x = pos, y = N1, size = 4, colour = "black")
}  

#c2 <- c2 + annotate("text", label = a[1] , x = pos, y = N1, size = 4, colour = "black")
#c2 <- c2 + annotate("text", label = a[2] , x = pos, y = N2, size = 4, colour = "black")
#c2 <- c2 + annotate("text", label = a[3] , x = pos, y = N3, size = 4, colour = "black")
#c2 <- c2 + annotate("text", label = a[4] , x = pos, y = N4, size = 4, colour = "black")

##############
# Other Plotting options
##############
c2 <- c2 +  theme(axis.title.x = element_text(size=25,face = "bold")) 
c2 <- c2 +  theme(axis.title.y = element_text(size=25,face = "bold",angle = 90))

c2 <- c2 + theme(axis.text.x=element_text(size=25,face = "bold"))
c2 <- c2 + theme(axis.text.y=element_blank()) #element_text(size=25,face = "bold"))
c2 <- c2 + scale_colour_discrete("Identity",breaks=c("<80%","81-90%","91-94%","95-98%",">=98%"))

c2 <- c2 + theme(legend.title=element_text(size=20,face = "bold"))
c2 <- c2 + theme(legend.text = element_text(size = 16))
c2 <- c2 + theme(legend.key.size = unit(0.8, "cm"))
c2 <- c2 + theme(legend.text.align=0)
#c2 <- c2 + opts(legend.position= c(0.05,0.80))

#out_file <- paste("BLAST_Summary_Images/",args[2],".png",sep="")

#print("HELLLO IAM HERE I")

png(out_file,width=1200)
print(c2)
dev.off()

}

out_file <- paste("BLAST_Summary_Images/",args[2],".png",sep="")

qseq_length <- args[3]

plot_plot(dat1,out_file,qseq_length)


quit(save="no",status=0)