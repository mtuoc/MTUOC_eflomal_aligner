# MTUOC_eflomal_aligner
Scripts to align parallel corpora at word or subword level using eflomal. Useful for training with guided alignment.

# Requirements

These scripts needs **eflomal** (https://github.com/robertostling/eflomal). Follow the installation instructions of eflomal:

Clone the eflomal repository or download the zip:

```
git clone https://github.com/robertostling/eflomal.git
cd eflomal
python3 -m pip install .
```

# Using the script
You can access the help of the program with the -h option:

```
python3 MTUOC_eflomal_aligner.py -h
usage: MTUOC_eflomal_aligner.py [-h] [--cL1 CL1] [--cL2 CL2] [--sL1 SL1] [--sL2 SL2] [--fwd FWD] [--rev REV]
                                [--inpriors INPRIORS] [--outpriors OUTPRIORS] [--limit LIMIT]

MTUOC_eflomal_aligner: command line tool to align a corpus or a pair of sentences using eflomal.

options:
  -h, --help            show this help message and exit
  --cL1 CL1             The corpus for language 1 (for corpus mode).
  --cL2 CL2             The corpus for language 2 (for corpus mode).
  --sL1 SL1             The sentence for language 1 (for sentence mode).
  --sL2 SL2             The sentence for language 2 (for sentence mode).
  --fwd FWD             The forward alignment.
  --rev REV             The reverse alignment.
  --inpriors INPRIORS   The input priors file to use. If not stated, not priors files will be used to start with the
                        alignment. This parameter is compulsory when aligning sentences.
  --outpriors OUTPRIORS
                        The output priors file that will be generated after the alignment. If not stated, the priors
                        files will be called eflomal.priors.
  --limit LIMIT         The limit of sentences to process.
```

If we need to align de train corpora: train.sp.en and train.sp.es, we should write`:

```python3 MTUOC_eflomal_aligner.py --cL1 train.sp.en --cL2 train.sp.es --fwd train.sp.en.es.align --rev train.sp.en.es.align --outpriors eng-spa.priors```

In train.sp.en.es.align we have the alignments if we want to train an English-Spanish system.

If we want to train the reverse system, Spanish-English, we can use the rev output, that is, the file train.sp.es.en.align. We don't need to rerun the script again.
