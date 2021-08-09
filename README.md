# hex2array-c
Creates a C array from a hex-string.

## Usage
```
Usage: python3 hex2array_c.py HEX_STRING [-h|--help]
Use '-' to read the hex string from STDIN.

Examples:
    python3 hex2array_c.py '0x9d35 0x3f19 0xcf12 0xcd72 0x7f4f 0xa035 0xb307 0x8f07'
    python3 hex2array_c.py '9d-3f-cf-cd-7f-a0-b3-8f' -w4
    python3 hex2array_c.py '538aedc060db31f2d708893526817f619d909526906c1c3a2dca7c242cd0e433' -n 'some_data' -w16
    cat ./afilewithbinarydata | python3 hex2array_c.py - -s4 -w4
    head -c 32 /dev/urandom | python3 hex2array_c.py -

Options:
    -n, --array-name NAME       The name to give to the generated array. The default is 'data'.
    -a, --array-type TYPE       The data type of the generated array. The default is 'const char'.
    -w, --array-width WIDTH     The number of array elements per row. The default is '8'.
    -s, --byte-length LENGTH    The byte length of each array element. The default is '1'.
    -t, --size SIZE             Trim the input to the specified size.
    -e, --swap-endianness       Swap the byte ordering of the generated array. The default is 'False'.

https://github.com/neosophaux
```

## Examples
Pass '-' to the program to read the hex string from stdin.

```
$ python3 hex2array_c.py '8eb3a4eca0cf603086e9791ca8b1b4ee67038cb96243b18fe43b86dd9a20c18a' -n 'test' -w2 -s4 -e
const char test[8] = {
    0xeca4b38e, 0x3060cfa0, // 0x00000000
    0x1c79e986, 0xeeb4b1a8, // 0x00000008
    0xb98c0367, 0x8fb14362, // 0x00000010
    0xdd863be4, 0x8ac1209a  // 0x00000018
};
```

```
$ python3 hex2array_c.py '8eb3a4eca0cf603086e9791ca8b1b4ee67038cb96243b18fe43b86dd9a20c18a' -w4 -a 'uint32_t'
uint32_t data[8] = {
    0x8eb3a4ec, 0xa0cf6030, 0x86e9791c, 0xa8b1b4ee, // 0x00000000
    0x67038cb9, 0x6243b18f, 0xe43b86dd, 0x9a20c18a  // 0x00000010
};
```

```
$ echo '0x9e 6b' | python3 hex2array_c.py - -n 'test' -e -s2 -a 'const uint16_t'
const uint16_t test[1] = {
    0x6b9e // 0x00000000
};
```

```
$ head -c 32 /dev/urandom | python3 hex2array_c.py -
const char data[32] = {
    0xbb, 0x70, 0xa1, 0x06, 0x1a, 0xe3, 0x85, 0x25, // 0x00000000
    0x6d, 0xbd, 0xeb, 0x73, 0x4d, 0x4b, 0x36, 0x85, // 0x00000008
    0x13, 0xb0, 0x61, 0xbc, 0x5f, 0x33, 0x68, 0x47, // 0x00000010
    0x2f, 0x6f, 0x37, 0x98, 0xce, 0xe4, 0x1c, 0x2b  // 0x00000018
};
```
