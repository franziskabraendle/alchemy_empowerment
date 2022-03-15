# Exploration as Empowerment

Project at the Computational Principles for Intelligence lab in Tübingen, GER.
This code and data can be used to replicate the results from "Intrinsically Motivated Exploration as Empowerment" by Brändle, Stocks, Tenenbaum, Gershman and Schulz.

## Installation
Install the requirements from "requirements.txt".

## data
Most behavioral data and generated data necessary to exactly replicate the results from the paper can be found at https://keeper.mpdl.mpg.de/d/28c50dc3a6bf4d10995d/ . Copy all the folders labeled "data" in the respective sub folders. Additionally copy the folder "fastText" into the resources subfolder.
The behavioral data of the ~29000 participants of the original game can be shared upon reasonable request by contacting me via "franziska.braendle@tuebingen.mpg.de"

## Usage

The code for the additional experiments "Tiny Alchemy", "Tiny Pixels" can be found in the folder "additionalexperiments". The code for the validation experiment, as well as the data generation for and analysis of this experiment lies in the same folder.

To clean the datasets and for an initial look (Figure 1c), as well as the percentage of immediate usage of elements (Figure 2a), run:
`python -m empowermentexploration.resources.playerdata`
To switch between the different datasets, adapt the code in the "main" file. To have more detailed analyses, run the different files in "BehaviorAnalysis_RCode".

To recreate the data for the "probability of continuing analysis" (Figure 2b), run the code in "regression/stoppingregression_RCode".

To run the different models (Figure 2c), adapt the main file in the main file of "models", and run it with: `python -m empowermentexploration.models`.

For the regression analysis (Figure 2d), run the code in "regression/modelcomparison_RCode". To replicate the predictions of the different models first adapt & run the main file of regression by running `python -m explorationempowerment.regression`.

To replicate the creation of the approximated gametrees, adapt and run
`python -m explorationempowerment.gametree`.

All the analyses can be done for Tiny Pixels / Tiny Alchemy, by adapting the respective main files (Figure 3).

## Credits
If you have any cquestions, or for any additional information contact me via franziska.braendle@tuebingen.mpg.de.
The code was written by Lena Stocks and Franziska Brändle. This project was created together with Eric Schulz. Thank you for all your support!

MIT © Lena Stocks, Franziska Brändle
