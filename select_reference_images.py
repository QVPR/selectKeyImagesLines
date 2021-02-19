import os
import cv2
import numpy as np
import subprocess

def get_images(directory):
	image_extensions = ['.png', '.bmp', '.jpg', '.tif','.jpeg','.pgm','.ppm']
	return [file for file in os.listdir(directory) if os.path.splitext(file)[1] in image_extensions]

def detect_lines(image, outfile):
	return subprocess.call(['selectKeyImagesLines/linematching/detectlinesED',image,outfile])

def match_lines(l1,l2,ml):
	return subprocess.call(['selectKeyImagesLines/linematching/matchlines',l1,l2,ml])

def copy_file(file,destination):
	return subprocess.call(['cp',file,destination])

def get_image_file_number(image_name):
	return image_name[len('frame'):].split('.')[0]

def get_matched_lines_in_3v(linesmatch,matchindex,lines):
	npts = matchindex.shape[0]
	matchedlines = np.array(2,2*npts,3)

	matchedlines[0,0:2:2*npts,0] = linesmatch[matchindex[:,0],0].T
	matchedlines[1,0:2:2*npts,0] = linesmatch[matchindex[:,0],1].T
	matchedlines[0,1:2:2*npts,0] = linesmatch[matchindex[:,0],2].T
	matchedlines[1,1:2:2*npts,0] = linesmatch[matchindex[:,0],3].T

	matchedlines[0,0:2:2*npts,1] = linesmatch[matchindex[:,1],4].T
	matchedlines[1,0:2:2*npts,1] = linesmatch[matchindex[:,1],5].T
	matchedlines[0,1:2:2*npts,1] = linesmatch[matchindex[:,1],6].T
	matchedlines[1,1:2:2*npts,1] = linesmatch[matchindex[:,1],6].T

	matchedlines[0,0:2:2*npts,2] = lines[matchindex[:,1],0].T
	matchedlines[1,0:2:2*npts,2] = lines[matchindex[:,1],1].T
	matchedlines[0,1:2:2*npts,2] = lines[matchindex[:,1],2].T
	matchedlines[1,1:2:2*npts,2] = lines[matchindex[:,1],3].T

base_folder = os.path.expanduser('~/linenav_officetest/')
output_directory = base_folder + 'ref_imgs/'
if not os.path.exists(output_directory):
	os.mkdir(output_directory)
min_line_num_threshold = 20

image_list = get_images(base_folder)

ct = 0
sfc = 0
for i, image_name in enumerate(image_list):
	image = cv2.imread(base_folder + image_name, cv2.IMREAD_GRAYSCALE)
	image_number = get_image_file_number(image_name)
	cv2.imwrite('tmpimg.pgm', image)
	
	status = detect_lines('tmpimg.pgm','edlines.out')
	lines = np.loadtxt('edlines.out')

	ct += 1
	if ct == 1:
		linest = lines
		pr = 1
		lines_match = []

		np.savetxt('lines_l.tmp', lines)
		copy_file(image_name, output_directory)
		np.savetxt(output_directory + 'kl_' + image_number + '.txt', lines)
	else:
		np.savetxt('lines_r.tmp', lines)
		status = match_lines('lines_l.tmp','lines_r.tmp','matched.lines')
		match_index = np.loadtxt('matched.lines')
		
		if len(match_index) < 10:
			status=1
			sfc += 1
			if sfc > 2:
				ct = 0
				sfc = 0
		else:
			sfc=0

		if status == 0:
			dt = lines
			linest = np.loadtxt('lines_l.tmp')
			lines = np.loadtxt('lines_r.tmp')

			lines_prev = linest[np.uint32(match_index[:,0]),:]
			linest = lines[np.uint32(match_index[:,1]),:]

			np.savetxt('lines_t.tmp',lines_prev)

			if ct > 2:
				# finish this!
				try:
					matched_lines = get_matched_lines_in_3v(lines_match, match_index, lines)
					# [TT,scorecheck,validindex] = calLineReconsError(matched_lines)
				except:
					ct = 0
					continue

			lines_match.append(np.hstack([lines_prev[:,:4],linest[:,:4]]))

image = cv2.imread(base_folder + image_list[-1], cv2.IMREAD_GRAYSCALE)
image_number = get_image_file_number(image_list[-1])
cv2.imwrite('tmpimg.pgm', image)
status = detect_lines('tmpimg.pgm','edlines.out')
lines = np.loadtxt('edlines.out')
copy_file(image_name, output_directory)
np.savetxt(output_directory + 'kl_' + image_number + '.txt', lines)

subprocess.call(['rm','*.tmp','*.out','*.pgm'])