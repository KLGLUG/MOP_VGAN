# MOP_VGAN
<b><a href="https://docs.google.com/presentation/d/1bQT2CmVgG1ku7ndb1TVb1bsB5l2_IjWhC478SEBqkSU/edit?usp=sharing">Controlled Video Generation by Discerning Physical Properties using a Physics Interpreter</a></b>

We propose a framework that learns physical properties of the content/object from unlabeled data.
We propose an unsupervised representation learning GAN, which explicitly encodes basic physical laws into the structure and use them, with automatically discovered observations from videos, as supervision.
We further explore directly mapping visual inputs to these physical properties, inverting a part of the generative process using deep learning.
<a href="https://drive.google.com/open?id=1ei3PhtyqmWdf3-xAOuhNSn5p5Z1-MjxF">

Instructions:
1) Use process_data.py on the directory of dataset you want to convert it into sequence of individual frames.
2) Run avg_runner which inturn uses generator and discriminator to generate required model.
Note: Use appropriate arguments to train and test.
