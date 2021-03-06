# Selection of Reference Images Based on Line Segment Matching 
Bista SR, Giordano PR, Chaumette F. Appearance-based indoor navigation by IBVS using line segments. IEEE Robotics and Automation Letters. 2016 Jan 26;1(1):423-30.
## Build

	1. Get Source codes from the repository
		$ git clone https://github.com/suuman/selectKeyImagesLines.git
	
	2. Build executables required for mapping. 
		$ ./build_linematching.sh
	
The above command will build executables detectinesED and matchlines to ./linematching folder and is equivalent to the following commands
	
	        $ cd linematching/Linematching_iso && mkdir build $$ cd build 
	        $ cmake .. && make -j8
 
## Usage
 The code for the mapping is in Matlab. Make sure the line detection and matching codes have been properly built and executables have been placed in the correct folder. For selecting the reference images, we need to provide the path of the image sequence folder and the folder to store the reference images.

	1. Open selectRefImages.m
	
	2. Set the path of the image sequence. e.g imseq = '../roboroom/imgs_acquired'
	
	3. Set the path to store the reference images. e.g refimpath='../roboroom/ref_imgs'
	
	4. Run selectRefImages.m

The reference image folder will contain

	1. Reference Images.
	
	2. The text files with the detected line segments and their descriptors. 
       There is one .txt file for each reference image.

## Running with Octave

1. Install Octave with image toolbox `sudo apt install octave octave-image`
2. Start octave command prompt `octave --no-gui`
3. Load image package `>> pkg load image`
4. Run selectRefImages `>> selectRefImages`
