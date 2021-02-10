# fact-checker
Automated fact verification system. Uses lucene (pylucene and lupyne) for text retrieval and a RoBERTa model trained by Facebook on the MNLI corpus to check for textual entailment.

### Initial Setup

1. [Recommended] Download and run pylucene docker image:
```
docker pull coady/pylucene
docker run -it --name lucene coady/pylucene bash
```

2. Install required libraries inside the container:
```
pip install torch
pip install transformers
pip install spacy
pip install lupyne
python -m spacy download en_core_web_sm
```
3. Download the dataset folder:\
`https://www.dropbox.com/s/pgc7pt3rszj25y5/wiki.zip?dl=0`

4. In a new terminal window, copy the scripts and the data folder to the running container:
```
docker cp wiki lucene:/usr/src
docker cp indexer.py lucene:/usr/src
docker cp src.py lucene:/usr/src
```

* [Note]: The `roberta-large-mnli` model used in the code requires a large amount of memory to run. The process will be killed by the OS if your system does not have enough free RAM.

### Usage Examples

```
root@674db38ea4df:/usr/src# python3 src.py "Nicholas Brody is a character on Homeland."
---------------------------------------------------
Artile:  Nicholas_Brody  ; File:  wiki-070.txt  ; Verdict:  ENTAILMENT   0.9863802194595337

1 Nicholas `` Nick '' Brody , played by actor Damian Lewis , is a fictional character on the American television series Homeland on Showtime , created by Alex Gansa and Howard Gordon .
---------------------------------------------------
```
```
root@674db38ea4df:/usr/src# python3 src.py "Brad Wilk helped co-found Rage in 1962."
---------------------------------------------------
Artile:  Brad_Wilk  ; File:  wiki-016.txt  ; Verdict:  CONTRADICTION   0.9871947765350342

4 Wilk started his career as a drummer for Greta in 1990 , and helped co-found Rage with Tom Morello and Zack de la Rocha in August 1991 .
---------------------------------------------------
```
```
root@674db38ea4df:/usr/src# python3 src.py "Bermuda Triangle is in the western part of the Himalayas."
---------------------------------------------------
Artile:  Bermuda_Triangle  ; File:  wiki-015.txt  ; Verdict:  CONTRADICTION   0.9992691874504089

0 The Bermuda Triangle , also known as the Devil 's Triangle , is a loosely-defined region in the western part of the North Atlantic Ocean , where a number of aircraft and ships are said to have disappeared under mysterious circumstances .
---------------------------------------------------
---------------------------------------------------
Artile:  Bermuda_Triangle  ; File:  wiki-015.txt  ; Verdict:  CONTRADICTION   0.9634113311767578

2 The vicinity of the Bermuda Triangle is one of the most heavily traveled shipping lanes in the world , with ships frequently crossing through it for ports in the Americas , Europe , and the Caribbean islands .
---------------------------------------------------
```
