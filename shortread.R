library(ShortRead)

Args <- commandArgs()
Args

fastqPath<-list.files(Args[6],pattern="trimmomatic_2P.fastq.gz$",full=TRUE)
fastqPath 
# read file
reads_s<-readFastq(fastqPath)


# filered low complexity reads (< 20 non-sequentially repeated nucleotides)
reads_s = reads_s[which(dustyScore(reads_s)>=20)]
reads_s

# # ShortRead::trimTailw(fq, 2, "4", 2)" to remove low-quality tails when 2 consecutive bases from the right of a 5-nucleotide window fall lower than "4", correspoding to Q=19
# reads_s <- trimTailw(reads_s, 2, "4", 2)
# reads_s

# ## drop reads that are less than 36nt
# reads_s <- reads_s[width(reads_s) >= 20]


# remove duplicated reads
reads_s <- reads_s[!srduplicated(reads_s)]
reads_s


file_a = "./shortread_clean_2.fastq.gz"
ShortRead::writeFastq(reads_s, file_a)