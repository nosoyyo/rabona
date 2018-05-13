from ri import RabonaImage as ri
from parser import RabonaParser as rp
from templates.FIFA18 import Segmentation
i = 'input/1.jpeg'
i = ri(i)
test = rp(i, Segmentation)
