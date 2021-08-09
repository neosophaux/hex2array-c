import io
import re
import sys

from argparse import ArgumentParser
from math import ceil

# opening brace convention - adjust as you please.
if True:
    # data[] = {
    opening_brace = ' = {\n'
else:
    # data[] =
    # {
    opening_brace = ' =\n{\n'

body_indent = 4
usage_examples = [
    "python3 hex2array_c.py '0x9d35 0x3f19 0xcf12 0xcd72 0x7f4f 0xa035 0xb307 0x8f07'",
    "python3 hex2array_c.py '9d-3f-cf-cd-7f-a0-b3-8f' -w4",
    "python3 hex2array_c.py '538aedc060db31f2d708893526817f619d909526906c1c3a2dca7c242cd0e433' -n 'some_data' -w16",
    "cat ./afilewithbinarydata | python3 hex2array_c.py - -s4 -w4",
    "head -c 32 /dev/urandom | python3 hex2array_c.py -"
]
output_code = {
    'header': '%s %s[%d]',
    'rows': [{
        'offset': 0,
        'data': []
    }]
}

class HexStream(object):
    def __init__(self, buf, datasz, swap_bytes):
        self._stream = io.BufferedReader(io.BytesIO(buf), len(buf))
        self._swap = swap_bytes

        self.bufsz = ceil(len(buf) / datasz)
        self.datasz = datasz

    def read(self):
        while len(self._stream.peek()) != 0:
            read_data = self._stream.read(self.datasz)

            if self._swap:
                read_data = read_data[::-1] # python just makes it so easy, lol.

            yield (self._stream.tell() - 1, read_data.hex().zfill(self.datasz * 2))

def main(hex_stream):
    for offset, data in hex_stream.read():
        last_row = output_code['rows'][-1]

        if len(last_row['data']) == owidth:
            output_code['rows'].append({
                'offset': offset - (hex_stream.datasz - 1),
                'data': []
            })

            last_row = output_code['rows'][-1]

        last_row['data'].append(data)

    if hex_stream.bufsz > (2 ** 32):
        offset_width = 16
    else:
        offset_width = 8

    formatted_code = output_code['header'] % (
        extra_args.array_type,
        extra_args.array_name,
        hex_stream.bufsz
    )
    formatted_code += opening_brace
    previous_row_len = 0

    for row_idx, row in enumerate(output_code['rows']):
        row_str = ' ' * body_indent

        row_str += ', '.join(['0x' + x for x in row['data']])

        if row_idx == len(output_code['rows']) - 1:
            # i suck at math; sorry if this seems hideous.
            if len(output_code['rows']) > 1:
                row_str += ' ' * (int(previous_row_len - (offset_width + 10)) - len(row_str) + 4)
            else:
                row_str += ' '
        else:
            row_str += ', '

        row_str += '// 0x%s\n' % format(row['offset'], '0%dx' % offset_width)
        previous_row_len = len(row_str)

        formatted_code += row_str

    formatted_code += '};'

    print(formatted_code)

def usage(e_code, extra_msg = None):
    print("Usage: python3 hex2array_c.py HEX_STRING [-h|--help]",
        file = sys.stdout if e_code == 0 else sys.stderr)

    print("Use '-' to read the hex string from STDIN.", end = '\n\n')
    print("Examples:")

    usage_indent = 4
    help_str_indent = 0

    for example in usage_examples:
        print((' ' * usage_indent) + example)

    print("\nOptions:")

    for action in extra_args_parser._actions:
        if action.metavar is None:
            action.metavar = ''

        _len = 0

        _len += len(', '.join(action.option_strings))
        _len += len(' %s' % action.metavar)

        if len(action.metavar) > 0:
            _len += usage_indent * 2

        if _len > help_str_indent:
            help_str_indent = _len

    for action in extra_args_parser._actions:
        if action.metavar is None:
            action.metavar = ''

        usage_str = ' ' * usage_indent

        usage_str += ', '.join(action.option_strings)
        usage_str += ' %s' % action.metavar

        padding = (help_str_indent - len(usage_str))

        if padding > 0:
            usage_str += ' ' * padding
        else:
            usage_str += ' ' * usage_indent

        usage_str += action.help

        if action.default is not None:
            usage_str += " The default is '%s'." % type(action.default)(action.default)

        print(usage_str)

    print("\nhttps://github.com/neosophaux")

    if extra_msg is not None:
        symbol = '+' if e_code == 0 else '-'

        print("\nError message:")
        print("[ %s ] %s" % (symbol, extra_msg))

    sys.exit(e_code)

def parse_args():
    parser = ArgumentParser(add_help = False)

    parser.add_argument(
        '-n', '--array-name',
        help = 'The name to give to the generated array.',
        type = str,
        metavar = 'NAME',
        default = 'data'
    )

    parser.add_argument(
        '-a', '--array-type',
        help = 'The data type of the generated array.',
        type = str,
        metavar = 'TYPE',
        default = 'const char'
    )

    parser.add_argument(
        '-w', '--array-width',
        help = "The number of array elements per row.",
        type = int,
        metavar = 'WIDTH',
        default = 8
    )

    parser.add_argument(
        '-s', '--byte-length',
        help = "The byte length of each array element.",
        type = int,
        metavar = 'LENGTH',
        default = 1
    )

    parser.add_argument(
        '-t', '--size',
        help = 'Trim the input to the specified size.',
        type = int,
        metavar = 'SIZE'
    )

    parser.add_argument(
        '-e', '--swap-endianness',
        help = 'Swap the byte ordering of the generated array.',
        action = 'store_true'
    )

    global extra_args_parser
    extra_args_parser = parser

    return parser.parse_args(sys.argv[2:])

extra_args_parser = None
extra_args = parse_args()

try:
    if '-h' in sys.argv or '--help' in sys.argv:
        usage(0)

    if sys.argv[1] == '-':
        stdin_cap = io.BytesIO(sys.stdin.buffer.read())
        try:
            hexstr = ''.join([line.decode(sys.stdin.encoding).strip() for line in stdin_cap.readlines()])

            if re.match('[A-Fa-f0-9]+', hexstr) is None:
                raise UnicodeDecodeError('', b'', 0, 0, '')
        except UnicodeDecodeError:
            stdin_cap.seek(0)
            hexstr = stdin_cap.read().hex()
    else:
        hexstr = sys.argv[1]

    hexstr = re.sub('[^A-Fa-f0-9]', '', hexstr.replace('0x', ''))

    if len(hexstr) % 2 != 0:
        usage(1, 'Invalid hex string. Input string has an uneven length.')
    
    hexstr = bytes.fromhex(hexstr)
    data_width = max(min(extra_args.byte_length, 64), 1) # cap at 512 bits or 8 bits(minimum).
    owidth = extra_args.array_width

    if extra_args.size is not None:
        if abs(extra_args.size) != len(hexstr):
            if extra_args.size >= 0:
                hexstr = hexstr[extra_args.size:]
            else:
                hexstr = hexstr[:extra_args.size]
        else:
            usage(1, 'Failed to trim. Trim size exceeded the byte length of the input.')

    if data_width != 1 and data_width % 2 != 0: # byte length MUST BE EVEN!!
        usage(1, "Invalid byte length '%d'." % data_width)

    if owidth > len(hexstr):
        owidth = len(hexstr)
except Exception as e:
    if isinstance(e, IndexError):
        usage(1, 'missing parameters')

    raise e
    usage(1, str(e))

main(HexStream(hexstr, data_width, extra_args.swap_endianness))
