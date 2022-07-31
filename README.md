# Home assignment for rightbound interview - part 1

Number of rows that have duplicates: 299

Number of rows that have a null functions column: 0

Number of rows that have a null function group column: 1

The number of appearances of each function group:

```uppercase_group
BENEFITS          1
CEO              15
CREATIVE         51
CUSTOMER        136
DESIGN            1
DEV             114
DIGITAL         333
ECOMMERCE       207
ENGINEERING      78
FINANCE          21
HR              161
IT              370
LEGAL            26
MARKETING      1422
OPERATION        21
OPERATIONS       82
OTHER           572
PRODUCT          28
REAL ESTATE       1
RETAIL            3
SALES           282
SECURITY        157
SUPPORT           1
TECHNOLOGY       82
TRAINING         80
dtype: int64
```

The functions mapped to more than one function group are:

```              uppercase_functions uppercase_group
275                   (CREATIVE,)       MARKETING
480                   (CREATIVE,)        CREATIVE
617       (MARKETING, OPERATIONS)       MARKETING
621       (MARKETING, OPERATIONS)      OPERATIONS
910           (CONTENT, CREATIVE)        CREATIVE
1453          (CONTENT, CREATIVE)       MARKETING
1704  (BRAND MARKETING, CREATIVE)        CREATIVE
2567  (BRAND MARKETING, CREATIVE)       MARKETING
```

There are 1.0 functions which appear throughout in different forms (different cases or different order).

There are 0 function groups which appear throughout in different forms (different cases).

The following are the counts of each of the functions that are mapped to the function group Other:

```uppercase_functions
(BI,)                    8
(CLAIMS,)                1
(CONTENT,)              99
(CONTENT, PRODUCER)      3
(DIGITAL ASSETS,)        1
(OTHER,)               457
(PRODUCER,)              3
dtype: int64
```

The following functions appear at times as duplicates within the same row:

```
{'BUSINESS DEVELOPMENT', 'TECHNOLOGY', 'CUSTOMER EXPERIENCE', 'CREATIVE', 'IT', 'INFO SECURITY', 'IT SERVICE', 'FINANCE', 'CONTENT', 'ACCOUNT MANAGER', 'DIGITAL', 'SALES', 'OPERATIONS', 'ECOMMERCE', 'BRAND MARKETING'}
```