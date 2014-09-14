#!/usr/bin/env python
from wand.image import Image
from wand.font import Font
from wand.color import Color
import argparse
import os
import subprocess

ap = argparse.ArgumentParser(description='[intensifying intensifies]')
ap.add_argument('-t', '--text', help='caption at the bottom')
ap.add_argument('-i', '--image', required=True, help='path to image')
ap.add_argument('--font-size', help='YELLING')
ap.add_argument('--flash-text', action='store_true', default=False)
ap.add_argument('-o', '--outfile', nargs='?', default='out.gif')
ap.add_argument('--no-wiggle', action='store_false', dest='wiggle', default=True)
ap.add_argument('--intensity', help='twerk moar')
args = ap.parse_args()

def cropshift(i, img, intensity):
	if i == 0:
		return img[:-1 * intensity, :]
	if i == 1:
		return img[:, :-1 * intensity]
	if i == 2:
		return img[intensity:, :]
	if i == 3:
		return img[:, intensity:]

print args
if not os.path.isdir('./frames'):
	os.mkdir('./frames')

with Image(file=open(args.image)) as img:
	gif = img.convert('gif')
	for x in range(4):
		frame = gif.clone()
		if args.wiggle:
			frame = cropshift(x, frame, int(args.intensity))
		color = Color('#FFFFFF')
		if args.flash_text and (x == 1 or x == 3):
			color = Color('FF0000')
		if (args.text):
			frame.caption(text=args.text,
				font=Font("./Impact.ttf", 48, color),
				gravity='south')
		frame.save(filename=('./frames/%d.gif' % x))

subprocess.call(['convert', './frames/*.gif',
	'-delay', '10000',
	'-loop', '0',
	'-coalesce',
	'out.gif'])
