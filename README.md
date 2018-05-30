# Auto Tally Sheet

Automatically parse a tally list using image processing.

## Generate Sheet

Adapt `names.yaml` and see `drinks.yaml` for how to specifiy your items.
Then run:

```bash
$ make
```

or run the command directly:
```bash
$ ./ats/main.py --placeholders 7 names.yaml items.yaml
```
where `--placeholders` specifies the number of blank lines.


## Readout the tally sheet

See the notebook `decode.ipynb`.
There is some bug that I have to fix. So currently the parsing does not work.
I will fix it as soon as our tally sheet has to be parsed (maybe a month from now).


## Missing features

- Automatically export to google docs
- Allow user to verify parsing and correct it
- Connect it to an e-mail mailbox such that any image recieved is automatically parsesd
