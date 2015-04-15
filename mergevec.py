###############################################################################
# Copyright (c) 2014, Blake Wulfe
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###############################################################################



import sys
import glob
import struct
import argparse
import traceback


def exception_response(e):
	exc_type, exc_value, exc_traceback = sys.exc_info()
	lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
	for line in lines:
		print(line)

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', dest='vec_directory')
	parser.add_argument('-o', dest='output_filename')
	args = parser.parse_args()
	return (args.vec_directory, args.output_filename)

def merge_vec_files(vec_directory, output_vec_file):
	
	
	# Check that the .vec directory does not end in '/' and if it does, remove it.
	if vec_directory.endswith('/'):
		vec_directory = vec_directory[:-1]
	# Get .vec files
	files = glob.glob('{0}/*.vec'.format(vec_directory))

	# Check to make sure there are .vec files in the directory
	if len(files) <= 0:
		print('Vec files to be mereged could not be found from directory: {0}'.format(vec_directory))
		sys.exit(1)
	# Check to make sure there are more than one .vec files
	if len(files) == 1:
		print('Only 1 vec file was found in directory: {0}. Cannot merge a single file.'.format(vec_directory))
		sys.exit(1)
		

	# Get the value for the first image size
	prev_image_size = 0
	try:
		with open(files[0], 'rb') as vecfile:
			content = ''.join(vecfile.readlines())
			val = struct.unpack('<iihh', content[:12])
			prev_image_size = val[1]
	except IOError as e:
		print('An IO error occured while processing the file: {0}'.format(f))
		exception_response(e)


	# Get the total number of images
	total_num_images = 0
	for f in files:
		try:
			with open(f, 'rb') as vecfile:	
				content = ''.join(vecfile.readlines())
				val = struct.unpack('<iihh', content[:12])
				num_images = val[0]
				image_size = val[1]
				if image_size != prev_image_size:
					err_msg = "err".format(f, image_size, prev_image_size)
					sys.exit(err_msg)

				total_num_images += num_images
		except IOError as e:
			print('An IO error occured while processing the file: {0}'.format(f))
			exception_response(e)

	
	# Iterate through the .vec files, writing their data (not the header) to the output file
	# '<iihh' means 'little endian, int, int, short, short'
	header = struct.pack('<iihh', total_num_images, image_size, 0, 0)
	try:
		with open(output_vec_file, 'wb') as outputfile:
			outputfile.write(header)

			for f in files:
				with open(f, 'rb') as vecfile:
					content = ''.join(vecfile.readlines())
					data = content[12:]
					outputfile.write(data)
	except Exception as e:
		exception_response(e)


if __name__ == '__main__':
	vec_directory, output_filename = get_args()
	if not vec_directory:
		sys.exit('mergvec requires a directory of vec files. Call mergevec.py with -v /your_vec_directory')
	if not output_filename:
		sys.exit('mergevec requires an output filename. Call mergevec.py with -o your_output_filename')

	merge_vec_files(vec_directory, output_filename)

