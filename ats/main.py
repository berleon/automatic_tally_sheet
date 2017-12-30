#! /usr/bin/env python

import argparse
import yaml
from ats.latex import LatexTemplate
import os
import qrcode
import tempfile
import base64
import zlib
import json

tmp_dir = tempfile.gettempdir()


def get_qr_code(config, name=None):
    if name is None:
        assert type(config) == str
        name = config

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L
    )
    qr.add_data(config)
    qr.make(fit=True)
    img = qr.make_image()

    filename = os.path.join(tmp_dir, name + '.png')
    print(filename)
    img.save(filename)
    return filename


def config_to_base64(config):
    x = json.dumps(config).encode('utf8')
    x = zlib.compress(x)
    return base64.b85encode(x).decode('utf8')


POSITIONS = ['tl', 'tr', 'tlc', 'trc', 'bl', 'br']
EDGE_POSITIONS = ['tl', 'tr', 'bl', 'br']


def split_config(config):
    base64_config = config_to_base64(config)
    n = len(base64_config)
    per_name = n // len(POSITIONS)
    splited = []
    for i, name in enumerate(POSITIONS):
        if i + 1 == len(POSITIONS):
            end = None
        else:
            end = per_name*(i+1)
        substring = base64_config[per_name*i:end]
        splited.append((name, substring))
    return splited


def check_names(names):
    for name in names:
        if len(name) >= 15:
            raise Exception("Name too long: {}".format(name))


def run(args, names, items, output_name, output_dir):
    check_names(names)
    names = sorted(names)
    names.extend([str(i+1) for i in range(args.placeholders)])
    qr_width = 3
    left = 0.3
    right = 26.0
    margin = 0.2
    positions = {
        'left': left,
        'left_center': right - 2*(qr_width + margin),
        'right_center': right - (qr_width + margin),
        'right': right,
        'top': -0.3,
        'bottom': -17.3,
    }
    config = {
        'names': names,
        'items': items
    }
    print(config)

    if 'fontsize' not in config:
        config['fontsize'] = 10
    config['positions'] = positions
    config['qr_code_width'] = 3

    filenames = {}
    for name, config_data in split_config(config):
        print(name, type(name))
        filenames[name] = get_qr_code("{}:{}".format(name, config_data), name)

    items = config['items']
    n_cols = sum([item['boxes'] for item in items])
    os.makedirs(output_dir, exist_ok=True)
    tmp = LatexTemplate('tally_list.tex')

    tmp.compile(os.path.join(output_dir, output_name),
                filenames=filenames,
                rule_thick=1.0,
                rule_very_thick=1.3,
                n_cols=n_cols,
                show_fridge_question=len(items) >= 3,
                **config)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('names', type=str, help='name file')
    parser.add_argument('items', type=str, help='items file')
    parser.add_argument('--placeholders', default=5, type=int, help='number of placeholder fields')
    parser.add_argument('-o', '--output-dir', type=str, default='output', help='output directory')
    args = parser.parse_args()
    with open(args.names, 'r') as f:
        names = yaml.load(f)
    with open(args.items, 'r') as f:
        items = yaml.load(f)

    items_basename = os.path.basename(args.items)
    output_name, _ = os.path.splitext(items_basename)
    output_name += '.tex'
    run(args, names, items, output_name, args.output_dir)


if __name__ == "__main__":
    main()
