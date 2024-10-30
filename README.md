
# Helper code to evaluate Q-Spatial Bench

Q-Spatial Bench is a benchmark designed to measure the **quantitative spatial reasoning** 📏 in large vision-language models.

🔥 The paper associated with Q-Spatial Bench is accepted by EMNLP 2024 main track!

- Our paper: *Reasoning Paths with Reference Objects Elicit Quantitative Spatial Reasoning in Large Vision-Language Models* [[arXiv link](https://arxiv.org/abs/2409.09788)]
- Project website: [[link](https://andrewliao11.github.io/spatial_prompt/)]



# Usage


## Dataset Download
Download the dataset from HuggingFace Hub
```python
from datasets import load_dataset
dataset = load_dataset("andrewliao11/Q-Spatial-Bench")
```

The dataset object has the following structure:
```
DatasetDict({
    QSpatial_plus: Dataset({
        features: ['question', 'answer_value', 'answer_unit', 'question_type', 'image_path', 'image'],
        num_rows: 101
    })
    QSpatial_scannet: Dataset({
        features: ['question', 'answer_value', 'answer_unit', 'question_type', 'image_path', 'image'],
        num_rows: 170
    })
})
```

### For QSpatial_scannet

You need to manually download them from ScanNet. To access the images in ScanNet, one needs to request the permission at [here](https://github.com/ScanNet/ScanNet?tab=readme-ov-file#scannet-data). Once you have the permission, you will get the instructions via email. Specifically, in the email, you have have the access to a python file named `download-scannet.py`. 

Once you have `download-scannet.py`, run the following code to download the images used in QSpatial-ScanNet
```
mv download-scannet.py <REPO_ROOT>/QSpatial_scannet
cd <REPO_ROOT>/QSpatial_scannet
python download_and_render_scannet_images.py
```


## Iterate over the Dataset

We provide an example ipython notebook under `examples/iterate_over_dataset.ipynb`

## Evaluation

We provide an example ipython notebook under `examples/evaluate_success_rate.ipynb`


# Citation
```bibtex
@misc{liao2024reasoningpathsreferenceobjects,
      title={Reasoning Paths with Reference Objects Elicit Quantitative Spatial Reasoning in Large Vision-Language Models}, 
      author={Yuan-Hong Liao and Rafid Mahmood and Sanja Fidler and David Acuna},
      year={2024},
      eprint={2409.09788},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2409.09788}, 
}
```

Feel free to reach out to Yuan-Hong Liao <andrew@cs.toronto.edu> for any questions.
