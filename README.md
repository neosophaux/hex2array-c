# hex2array-c
Creates a C array from a hex-string.

```
usage: python3 hex2array_c.py <hex string> <array width> [-h|--help] [array name]
```

## Examples
Pass '-' to the program to read the hex string from stdin.

```
$ python3 hex2array_c.py '8eb3a4eca0cf603086e9791ca8b1b4ee67038cb96243b18fe43b86dd9a20c18a' 8 test
const char test[32] = {
    0x8e, 0xb3, 0xa4, 0xec, 0xa0, 0xcf, 0x60, 0x30, // 0x00000000
    0x86, 0xe9, 0x79, 0x1c, 0xa8, 0xb1, 0xb4, 0xee, // 0x00000008
    0x67, 0x03, 0x8c, 0xb9, 0x62, 0x43, 0xb1, 0x8f, // 0x00000010
    0xe4, 0x3b, 0x86, 0xdd, 0x9a, 0x20, 0xc1, 0x8a  // 0x00000018
};
```

```
$ python3 hex2array_c.py '8eb3a4eca0cf603086e9791ca8b1b4ee67038cb96243b18fe43b86dd9a20c18a' 4
const char data[32] = {
    0x8e, 0xb3, 0xa4, 0xec, // 0x00000000
    0xa0, 0xcf, 0x60, 0x30, // 0x00000004
    0x86, 0xe9, 0x79, 0x1c, // 0x00000008
    0xa8, 0xb1, 0xb4, 0xee, // 0x0000000c
    0x67, 0x03, 0x8c, 0xb9, // 0x00000010
    0x62, 0x43, 0xb1, 0x8f, // 0x00000014
    0xe4, 0x3b, 0x86, 0xdd, // 0x00000018
    0x9a, 0x20, 0xc1, 0x8a  // 0x0000001c
};
```

```
$ echo '0x9e 6b' | python3 hex2array_c.py - 8 test
const char test[2] = {
    0x9e, 0x6b  // 0x00000000
};
```

```
$ head -c 32 /dev/urandom | python3 hex2array_c.py - 8
const char data[32] = {
    0xbb, 0x70, 0xa1, 0x06, 0x1a, 0xe3, 0x85, 0x25, // 0x00000000
    0x6d, 0xbd, 0xeb, 0x73, 0x4d, 0x4b, 0x36, 0x85, // 0x00000008
    0x13, 0xb0, 0x61, 0xbc, 0x5f, 0x33, 0x68, 0x47, // 0x00000010
    0x2f, 0x6f, 0x37, 0x98, 0xce, 0xe4, 0x1c, 0x2b  // 0x00000018
};
```
