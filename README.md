[![GitHub][github-shield]][github-url]
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)

<br >
<div align="center">
<h3 align="center">Bachelor's Thesis: Direct Decipherment and Transcription <br > of Historical Handwritten Ciphered Document Images</h3>
</div>

<br >

## Abstract
This bachelor’s thesis main topic will be the direct decipherment of historical documents by proposing a joint end-to-end approach. The usual techniques use a pipeline approach, causing a high level of dependance between tasks; the mistakes from the previous phases concatenate into the next one. However, there are not many studies on the possibility of directly deciphering these images.

<br />

## Author 
Marina Bermúdez Granados - <a href="https://github.com/nara-on">nara-on</a> <br />

<br />

## Project Structure

      .
      ├── ciphers                        # Directory containing the cipher fonts for the image generation
      └── code
          ├── classes                    # Directory with the source code for the data augmentation and the ciphers
          ├── models                     # Directory with the source code of the models and the experiments
          └── trials                     # Directory with some testing code
      └── databases
          ├── copiale_alphabet           # Directory with images of the Copiale alphabet
          ├── data                       # Directory with json files to organize training, testing, and validation
          └── trials                     # Directory with some testing code
      ├── texts                          # Directory containing different text files to generate images
      └── visuals
          ├── documentation              # Directory for the documentation of the project
          └── plots                      
              ├── pkl                    # Directory with visuals from the pkl files
              ├── terminal               # Directory with visuals from the terminal
              └── wandb                  # Directory with visuals from wandb
          └── results_model_v2           # Directory for the different result logs of the second model

<br />

## Images 
<div align="center">
   <h4>Sequence to Sequence Model with Attention</h4>
   <img src="https://github.com/Nara-On/DecipherAndTranscribe/blob/main/visuals/documentation/seq2seq-attention.png" width="700">
   <br />
   <br />
   <br />
   
   <h4>Qualitative Results for the Transcription Task</h4>
   <img src="https://github.com/Nara-On/DecipherAndTranscribe/blob/main/visuals/documentation/qualitative_t.png" width="700">
   <br />
   <br />
   <br />
   
   <h4>Qualitative Results for the Direct Decipherment Task</h4>
   <img src="https://github.com/Nara-On/DecipherAndTranscribe/blob/main/visuals/documentation/qualitative_d.png" width="700">
</div>

<br />
<br />

## Version History
* 5.2
    * Final touches
* 5.1
    * Final results included
* 5.0
    * New model updated
* 4.4
    * Final Training on transcription task added
* 4.3
    * Training results on transcription task added
    * Visuals added
    * Updates to code
* 4.2
    * Configuration of the first training
* 4.1
    * Updates to the databases
* 4.0
    * Models added
* 3.0
    * Version 2 of Copiale added
    * Copiale class added
    * Cipher Generator class added
* 2.2
    * Comments added
* 2.1
    * Small corrections
    * More texts added
* 2.0
    * Texts added
    * Funtion gen_lines_rand() modified and renamed
    * Funtion gen_txt() modified
    * Funtion gen_lines() added
    * Funtion gen_lines_nums() added
    * Funtion gen_single_lines() added
    * Funtion gen_single_txt() added
* 1.0
    * Creation of gen_cipher.py
    * Funtion gen_lines() added
    * Funtion gen_txt() added
* Initial commit
    * Creation of repository


[github-shield]: https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white
[github-url]: https://github.com/Nara-On
