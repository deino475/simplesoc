# simplesoc

simplesoc is a simple Python library for attaching Standard Occupation Classification (SOC) codes to 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install simplesoc.

```bash
pip install simplesoc
```

## Usage

```python
from simplesoc import find_soc_code
soc_code_predictions = find_soc_code('Softwear Enginer', year = 'US.2018', n_socs = 3)

```
