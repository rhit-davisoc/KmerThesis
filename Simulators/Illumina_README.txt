=========================================================================================================
                                          ART (Q Version 1.1.5)                             
  		 Copyright(c) 2008-2011, Weichun Huang, Jason Myers. All Rights Reserved.   
=========================================================================================================

DESCRIPTION

	ART (art_Illumina Q version) is a simulation program to generate sequence read data of Illumina
       	sequencers. ART generates reads according to the empirical read quality profile summarized from
       	large real read data. ART has been using for testing or benchmarking a variety of methods or tools
       	for next-generation sequencing data analysis, including read alignment, de novo assembly, detection
        of SNP, CNV, or other structure variation.
       	
COMPILATION AND INSTALLATION

	./configure --prefix=$HOME
	make
	make install

EXAMPLES

	In the "examples" subdirectory, the shell script "run_test_examples.sh" gives four examples of using
       	ART for read simulation.  To test these four examples, just run the script "run_test_examples.sh"

USAGE

	art_illumina [options] -i <DNA_reference_file> -l <read_length> -f <fold_coverage> -o <outFile_prefix>

	 Examples:

	 1) single-end read simulation

	 art_illumina -i reference.fa -l 50 -f 10 -o single_end_data


	 2) paired-end read simulation
	
	 art_illumina -i reference.fa -p -l 50 -f 20 -m 200 -s 10 -o outFile_prefix

	Parameters

	  -p   --paired   indicate a paired-end read simulation
	  -q   --quiet    turn off end of run summary
	  -h   --help     print out usage information for ART
	  -sp  --sepProf  indicate the use of separate quality profiles for different bases (ATGC)
	
	  -i   --in       the filename of input DNA reference
	  -o   --out      the prefix of output files
	  -l   --len      the length of reads to be simulated
	  -f   --fcov     the fold of read coverage to be simulated
	  -m   --mflen    the mean size of DNA fragments for paired-end simulations
	  -s   --sdev     the standard deviation of DNA fragment size for paired-end simulations.
	  -ir  --insRate  the first-read insertion rate (default: 0.00009)
	  -dr  --delRate  the first-read deletion rate (default:  0.00011)
	  -ir2 --insRate2 the second-read insertion rate (default: 0.00015)
	  -dr2 --delRate2 the second-read deletion rate (default: 0.00023)
	  -qs  --qShift   the amount to shift every first-read quality score by
	  -qs2 --qShift2  the amount to shift every second-read quality score by
	  -1   --qprof1   the first-read quality profile
	  -2   --qprof2   the second-read quality profile
	  -d   --id       the prefix identification tag for read ID
	
	* The default quality score profiles are determined based on the length
	  of read specified for the run and were derived from re-calibrated data.
	
	* To simulate single-end reads one must provide the ART program with at least an input file,
	   output file prefix, the read length and the fold coverage.
	
	  Example: art --in reference_DNA.fa --out sim1 --len 35 --fcov 2
	
	* To simulate paired-end reads one must use the parameters above as
	  well as the mean fragment length, standard deviation, and --paired tag.
	
	  Example: art --paired --in reference_DNA.fa --out sim2 --len 35 --fcov 2 --mflen 200 --sdev 3.5
	
		
READ QUALITY PROFILE

	FORMAT 
	A valid quality score profile is tab-delimited and has no specific header line. Headers can be included
       	if each line of extraneous information begins with a number sign(#). Each line of actual quality profile
       	information must begin with an identifier that indicates where the data comes from for the remainder of
       	the line. Identifiers include:

		.	The identifier for the combination of all base information.
		
		A	The identifier for quality scores associated with A calls only.

		T	The identifier for quality scores associated with T calls only.

		G	The identifier for quality scores associated with G calls only.

		C	The identifier for quality scores associated with C calls only.


	Following the identifier on a given line must be the position number indicating where the rest of the
       	information on that line applies within a given fragment. The data must be arrayed in pairs such that each
       	line in the pair has the same identifier and position number. The first line in a pair must be a list of 
	quality scores in ascending order and the second line must be the empirical distribution of frequency
       	associated with the list of quality scores. 


	EXAMPLE:


	.       0       3       6       7       8       9       10      11      12	13      14      15
	.       0       39375   355755  395136  415685  1227131 1338634 1522001	1851208 2165909 2436839 2608538
	...
	.       35      4       5       6       7       8       9       10      11	12      13      14
	.       35      434262  1341151 1725690 2979293 3478620 3592624 3672807	3873754 4096922 4983957 6111261
	A       0       3       6       7       8       9       10      11      12	13      14      15
	A       0       560     99637   111485  119727  389899  412150  458066  572958	665153  745916  793532

	BUILT-IN PROFILES 

	Under subfolder "Illumina_GAII_profiles" are the built-in read profiles of Illumina GAII sequencers. These profiles were summerized from
	sample data of recalibrated Illumina reads from the 1000 genomes project. 

	    36bp reads
		1st: EmpR36R1
		2nd: EmpR36R2

	    44bp reads
		1st: EmpR44R1
		2nd: EmpR44R2

	    50bp reads
		1st: EmpR50R1
		2nd: EmpR50R2

	    75 reads
		1st: EmpR75R1
		2nd: EmpR75R2

OUTPUT FILES

	*.fq   - FASTQ read data files. For paired‐read simulation, *1.fq contains data of the first reads, and *2.fq for the second reads.
	*.aln  - read alignment files. For paired‐read simulation, *1.aln has read alignments for the first reads and *2.aln for the second reads.

	FASTQ FILE format 
		A FASTQ file contains both sequence bases and quality scores of sequencing reads and is in the following format:  
			@read_id 
			sequence_read 
			+ 
			base_quality_scores 
	
		A base quality score is coded by the ASCII code of a single character, where the quality score is equal to ASCII code of the
       		character minus 33.    

		Example: 
		@refid-4028550-1 
		caacgccactcagcaatgatcggtttattcacgat...
		+ 
		????????????7?????<??>??=&?<<?-<?0?...

	ALN format 
		>ref_seq_id	read_id	aln_start_pos	ref_seq_strand
	       	ref_seq_aligned
	       	read_seq_aligned 
	
		aln_start_pos is the alignment start position of reference sequence. aln_start_pos is always relative to the strand of reference
       		sequence. That is, aln_start_pos 10 in the plus (+) strand is different from aln_start_pos 10 in the minus (‐) stand.  
	
		ref_seq_aligned is the aligned region of reference sequence, which can be from plus strand or minus strand of the reference sequence.  
		read_seq_aligned is the aligned sequence read, which always in the same orientation of the same read in the corresponding fastq file. 

