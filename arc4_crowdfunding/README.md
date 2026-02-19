# ARC-4 Crowdfunding Smart Contract

A production-ready Algorand smart contract implementing a decentralized crowdfunding platform following the ARC-4 standard.

## Overview

This smart contract enables:

- Campaign Creation: Creators can launch crowdfunding campaigns with specific goals and deadlines
- Pledging: Backers can contribute funds using Box storage for unlimited scalability
- Automatic Distribution: Funds are automatically distributed to creators when goals are met
- Refund Mechanism: Backers can reclaim funds if campaigns fail to meet their goals

## Features

- Rekey Protection: All inner transactions include rekey_to=ZeroAddress
- Fee Pooling: Uses fee=0 on inner transactions (caller provides extra fees)
- Double Claim Prevention: Boolean flag prevents multiple claims
- Input Validation: Comprehensive assertion checks on all inputs

## Files

- `contract.py` — Main ARC-4 contract implementation
- `deployment.py` — Deployment helper script
- `test_crowdfunding.py` — Unit tests
- `requirements.txt` — Python dependencies

## Deployment

Set your mnemonic and run:

```bash
export ALGO_MNEMONIC="your 25 word mnemonic..."
python deployment.py
```

## Tests

```bash
pytest test_crowdfunding.py -v
```

## License

MIT
