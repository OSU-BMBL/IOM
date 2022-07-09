# Pipeline for mining microbial data from single-cell RNA sequencing (scRNA-seq) data #
## Brief Description: ##
This pipeline can help researchers obtain microbial data from existing scRNA-seq datasets without conducting additional wet-lab experiments. 
## Environment: ##
This pipeline requires a basic **UNIX/Linux environment**. The computational tools required in this pipeline include [Kraken2](https://github.com/DerrickWood/kraken2), [Shortread](https://bioconductor.org/packages/release/bioc/html/ShortRead.html), [Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic), and [umi-tools](https://github.com/CGATOxford/UMI-tools). 
# Usage: #
## 1. Candidate microbial reads and taxonomic profiling identification ##
First, install [Kraken2](https://github.com/DerrickWood/kraken2) and download a Kraken2 database. Here,  Kraken2 database is downloaded to /database_path/kraken2_database. Second, download scRNA-seq datasets. Here, [CRR034524](https://ngdc.cncb.ac.cn/gsa/browse/CRA001160/CRR034524), containing two scRNA-seq datasets (CRR034524_f1.fastq.gz and CRR034524_r2.fastq.gz), is downloaded to /path/data/CRR034524. Third, run Kraken2 using the code below:
 
    cd /path/
    mkdir p15 
    mkdir result
	kraken2 --db /database_path/kraken2_database --threads 56 --paired ./data/CRR034524/CRR034524_f1.fastq.gz ./data/CRR034524/CRR034524_r2.fastq.gz --classified-out ./p15/p15_classified#.fastq --unclassified-out ./p15/p15_unclassified#.fastq --report ./result/CRR034524.report --output ./result/CRR034524.output

## 2. Barcode extraction ##
In this step, each candidate microbial read is given a barcode.
Install [umi-tools](https://github.com/CGATOxford/UMI-tools), then run umi_tools using the code below:

	mkdir ./p15/filter_reads
	mkdir ./p15/filter_reads/re
	umi_tools whitelist --stdin ./p15/p15_classified_1.fastq --bc-pattern=CCCCCCCCCCCCCCCCNNNNNNNNNN --log2stderr > ./p15/filter_reads/whitelist.txt
	umi_tools extract --bc-pattern=CCCCCCCCCCCCCCCCNNNNNNNNNNNN --stdin ./p15/p15_classified_1.fastq --stdout ./p15/filter_reads/re/p15_classified_1_extracted.fastq --read2-in ./p15/p15_classified_2.fastq --read2-out=./p15/filter_reads/re/p15_classified_2_extracted.fastq --filter-cell-barcode --whitelist=./whitelist.txt

## 3. Quality control ##
In this step, reads with low quality are removed. 
Install [Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic) (Trimmomatic is downloaded to /trimmomatic_path/trimmomatic.jar) and [Shortread](https://bioconductor.org/packages/release/bioc/html/ShortRead.html), then run Trimmonatic and Shortread using the code below:

	java -jar /trimmomatic_path/trimmomatic.jar PE –threads 56 ./p15/filter_reads/re/p15_classified_1_extracted.fastq ./p15/filter_reads/re/p15_classified_2_extracted.fastq -baseout ./p15/filter_reads/re/p15_trimmomatic.fastq.gz SLIDINGWINDOW:4:20 MINLEN:40
	Rscript ./shortread.R ./p15/filter_reads/re
	
## 4. Microbial-cell matrix construction ##
 Run the code below:
```
gunzip ./p15/filter_reads/re/shortread_clean_2.fastq.gz
python ./matrix.py -input ./p15/filter_reads/re/shortread_clean_2.fastq
```
Finally, the output file ./p15/filter_reads/re/read_count_label.tsv is the microbal-cell matrix file.
# Contact #
Any questions, problems, or bugs are welcome and should be dumped to [Qin Ma](mailto:Qin.Ma@osumc.edu).
