import io
import sys

def usage(e_code, extra_msg = None):
    print("usage: python3 hex2array_c.py <hex string> <array width> [-h|--help] [array name]",
        file = sys.stdout if e_code == 0 else sys.stderr)

    if extra_msg is not None:
        symbol = '+' if e_code == 0 else '-'

        print("[ %s ] %s" % (symbol, extra_msg))

    sys.exit(e_code)

try:
    if '-h' in sys.argv or '--help' in sys.argv:
        usage(0)

    # will throw an error if the width is NaN AND if the number of required params
    # wasn't met.
    owidth = int(sys.argv[2])

    if sys.argv[1] == '-':
        stdin_cap = io.BytesIO(sys.stdin.buffer.read())
        try:
            hexstr = ''.join([line.decode(sys.stdin.encoding).strip() for line in stdin_cap.readlines()])
        except UnicodeDecodeError:
            stdin_cap.seek(0)
            hexstr = stdin_cap.read().hex()
    else:
        hexstr = sys.argv[1]

    hexstr = hexstr.replace('0x', '').replace(' ', '')

    if len(hexstr) % 2 != 0:
        usage(1, 'Invalid hex string. Input string has an uneven length.')
    
    hexstr = bytes.fromhex(hexstr)

    if len(sys.argv) > 3:
        array_name = sys.argv[3]
    else:
        array_name = 'data'

    if owidth > len(hexstr):
        owidth = len(hexstr)
except Exception as e:
    if isinstance(e, IndexError):
        usage(1, 'missing parameters')
    
    usage(1, str(e))

# opening brace convention - adjust as you please.
if True:
    opening_brace = ' = {\n'
else:
    opening_brace = ' =\n{\n'

body_indent = 4
output_code = {
    'header': 'const char %s[%d]',
    'rows': [{
        'offset': 0,
        'data': []
    }]
}

def main():
    for offset, byte in enumerate(hexstr):
        last_row = output_code['rows'][-1]

        if len(last_row['data']) == owidth:
            output_code['rows'].append({
                'offset': offset,
                'data': []
            })

            last_row = output_code['rows'][-1]

        last_row['data'].append(byte)

    formatted_code = output_code['header'] % (array_name, len(hexstr))
    formatted_code += opening_brace

    for row_idx, row in enumerate(output_code['rows']):
        row_str = ' ' * body_indent

        row_str += ', '.join(['0x' + format(b, '02x') for b in row['data']])

        if row_idx == len(output_code['rows']) - 1:
            row_str += ' ' * (((owidth - len(row['data'])) * 6) + 1)
        else:
            row_str += ', '

        row_str += ' // 0x%s\n' % format(row['offset'], '08x')

        formatted_code += row_str

    formatted_code += '};'

    print(formatted_code)

main()
