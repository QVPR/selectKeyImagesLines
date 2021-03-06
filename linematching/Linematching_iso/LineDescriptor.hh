/*
 * LineDescriptor.hh
 *
 *  Created on: Dec 12, 2011
 *      Author: lz
 */

#ifndef LINEDESCRIPTOR_HH_
#define LINEDESCRIPTOR_HH_


#include "EDLineDetector.hh"
#include "LineStructure.hh"
//#include <Filter/Gauss.hh>
//#include <Filter/Rescale.hh>

#include <opencv2/line_descriptor.hpp>
#include <map>
struct OctaveLine{
  unsigned int octaveCount;//the octave which this line is detected
  unsigned int lineIDInOctave;//the line ID in that octave image
  unsigned int lineIDInScaleLineVec;//the line ID in Scale line vector
  float lineLength; //the length of line in original image scale
};


/* This class is used to generate the line descriptors from multi-scale images  */
class LineDescriptor
{
public:
	LineDescriptor();
	LineDescriptor(unsigned int numOfBand, unsigned int widthOfBand);
	~LineDescriptor();
	enum{
		NearestNeighbor=0, //the nearest neighbor is taken as matching
		NNDR=1//nearest/next ratio
	};
  /*This function is used to detect lines from multi-scale images.*/
    int GetLineDescriptor(cv::Mat & image, ScaleLines &keyLines);
    int OctaveKeyLines(cv::Mat & image, ScaleLines &keyLines);
    //int OctaveKeyLines(BIAS::Image<unsigned char> & image, ScaleLines &keyLines);
	void findLineDesc(ScaleLines &keyLines);
    void computeBinaryLineDesc(ScaleLines &keyLines);
    void computeBinaryLineDescFull(ScaleLines &keyLines);
  //int GetLineDescriptor(BIAS::Image<unsigned char> & image,
    //	ScaleLines &keyLines);
  int MatchLineByDescriptor(ScaleLines &keyLinesLeft, ScaleLines &keyLinesRight,
  		std::vector<short> &matchLeft, std::vector<short> &matchRight,
  		int criteria=NNDR);
  int LineMatchingBinary(ScaleLines &keyLinesLeft, ScaleLines &keyLinesRight,std::vector<unsigned int> &matchResult);
  float LowestThreshold;//global threshold for line descriptor distance, default is 0.35
  float NNDRThreshold;//the NNDR threshold for line descriptor distance, default is 0.6
  int bDistThreshold;
private:
    template<class T>
    void sample(T *igray,T *ogray, float factor, int width, int height)
	{

		int swidth = (int)((float) width / factor);
		int sheight = (int)((float) height / factor);

		for(int j=0; j < sheight; j++)
		 for(int i=0; i < swidth; i++)
			ogray[j*swidth + i] = igray[(int)((float) j * factor) * width + (int) ((float) i*factor)];

	}
	/*Compute the line descriptor of input line set. This function should be called
	 *after OctaveKeyLines() function; */
	int ComputeLBD_(ScaleLines &keyLines);
	/*For each octave of image, we define an EDLineDetector, because we can get gradient images (dxImg, dyImg, gImg)
	 *from the EDLineDetector class without extra computation cost. Another reason is that, if we use
	 *a single EDLineDetector to detect lines in different octave of images, then we need to allocate and release
	 *memory for gradient images (dxImg, dyImg, gImg) repeatedly for their varying size*/
	std::vector<EDLineDetector*> edLineVec_;

	int ksize_; //the size of Gaussian kernel: ksize X ksize, default value is 5.
	unsigned int  numOfOctave_;//the number of image octave
	unsigned int  numOfBand_;//the number of band used to compute line descriptor
	unsigned int  widthOfBand_;//the width of band;
    std::vector<float> gaussCoefL_;//the local gaussian coefficient apply to the orthogonal line direction within each band;
    std::vector<float> gaussCoefG_;//the global gaussian coefficient apply to each Row within line support region
    cv::Ptr<cv::line_descriptor::BinaryDescriptorMatcher> bdm;
    inline int get2Pow( int i )
    {
      if (i >= 0 && i <= 7);
         return 1 << i;
    }

    unsigned char binaryConversion( float* f1, float* f2 )
    {
      uchar result = 0;
      for ( int i = 0; i < 8; i++ )
      {
        if( f1[i] > f2[i] )
          result += (uchar) get2Pow( i );
      }

      return result;

    }
};






#endif /* LINEDESCRIPTOR_HH_ */
