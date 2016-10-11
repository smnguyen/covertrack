Each step is defined by a tuple of `dict`s, where each `dict` contains the `name` of a function to call, and a key-value pair for each parameter of the function.

## Input files
`input_parent_dir`: Absolute directory path where raw image files are stored
`output_parent_dir`: Absolute directory path where output folder is created. The created folder will have the same basename as `input_parent_dir`

## Initial set-up
`first_frame`, `last_frame`: Limits the frames used for tracking. 0-indexed. To use all frames, set both to `None`.

`setup_args`: Only one function should be provided in this tuple. If more than one tuple is provided, the results of the last set-up function will be used to run the rest of the steps. Below is a description of the functions that can be used in this step.
  * `retrieve_files`:
    * Arguments:
      * `channels` - A list of color(?) channels captured by the frames
    * Description: Sorts the images in `input_parent_dir` into groups of channels. An image belongs to a channel if the channel is a substring in the image filename. NOTE: The order of channels is very important, as later steps will only run on frames of the first channel.
  * `retrieve_files_glob`
    * Arguments:
      * `channels` - A list of color(?) channels captured by the frames
      * `patterns` - A list of filename patterns, the same size as `channels`.
    * Description: Sorts the images in `input_parent_dir` into groups of channels. `channels` and `patterns` are parallel lists, i.e. the channel at index 0 corresponds to the pattern at index 0. An image is from the index 0 channel if it its filename matches the index 0 pattern. NOTE: The order of channels is very important, as later steps will only run on frames of the first channel.

## Preprocessing
`preprocess_args`: Multiple functions can be provided in this tuple. If multiple functions are provided, the functions will run on an image in the order that they are listed. To limit a preprocessing function to only run on a single channel, provide a value in the function argument's `dict` for the key `ch` that matches one of the channels provided in the list of channels for the `setup_args` function.
  * `hist_matching`
    * Arguments:
      * `BINS` (default 10000): The number of bins to be used in the histogram matching
      * `QUANT` (default 100): The number of points at which the histograms should match
    * Description: Given a frame, this function matches its grayscale values to the previous frame. For more details, see the [SimpleITK documentation](https://itk.org/Doxygen/html/classitk_1_1HistogramMatchingImageFilter.html) for notes on implementation and [MATLAB documentation](https://www.mathworks.com/help/images/ref/imhistmatch.html) for visual examples.
  * `n4_illum_correction`
    * TODO Ask about:
      * `adaptive_thresh` implementation
      * What does 'illum' mean?
    * Arguments:
      * `FILTERINGSIZE` (default 50): The standard deviation of the Gaussian kernel applied to determine the background (i.e. how much blur should be applied).
      * `RATIO` (default 1.5): Used to determine background vs. foreground. For example, if you set `RATIO` to 3.0, it will pick the pixels 300 percent brighter than the blurred image to be the background(?).
    * Description: Applies a variant of the [N3 algorithm](https://en.wikibooks.org/wiki/MINC/Tools/N3) to clean up noise in the image. See implementation details in the [SimpleITK documentation](https://itk.org/Doxygen/html/classitk_1_1N4BiasFieldCorrectionImageFilter.html).
  * `n4_illum_correction_downsample`
    * Arguments:
      * `DOWN` (default 2): The scale at which to downscale the image before applying the N4 algorithm.
      * `RATIO` (default 1.05): Used to determine background vs. foreground. For example, if you set `RATIO` to 3.0, it will pick the pixels 300 percent brighter than the blurred image to be the background(?).
      * `FILTERINGSIZE` (default 50): The standard deviation of the Gaussian kernel applied to determine the background (i.e. how much blur should be applied).
      * `OFFSET` (default 10): The minimum value of pixels in the image after applying the N4 correction. Used to avoid errors when applying log transformations.
    * Description: Similar to `n4_illum_correction`, but downscales the image before applying the N4 algorithm, and scales the image back up afterwards. This is faster, but is more insensitive to local illum bias.
  * `background_subtraction_wavelet`
    * Arguments:
      * `level` (default 7):
      * `OFFSET` (default 10): The minimum value of pixels in the image after applying the N4 correction. Used to avoid errors when applying log transformations.
    * Description: Uses Haar wavelet subtraction to remove the background of each frame.
  * `smooth_curvature_anisotropic`
    * Arguments:
      * `NUMITER` (default 10): The number of iterations to run the filter before stopping. Generally, the more iterations, the more diffused the image will become.
    * Description: Performs anisotropic diffusion on the image using the modified curvature diffusion equation. At a high level, this blurs the image, but in such a way that major structures in the image become more apparent. See the end of [this PDF](http://www.mia.uni-saarland.de/weickert/Papers/book.pdf) for images demonstrating the effect.
  * `background_subtraction_prcblock`
  * `background_subtraction_wavelet_hazen`
