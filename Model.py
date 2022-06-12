LOAD_TORCH = True
import time
if LOAD_TORCH:
    USE_NNPACK=0
    from fastbook import platform
    from torch import load
    import pathlib
    plt = platform.system()
    if plt == 'Linux': 
        pathlib.WindowsPath = pathlib.PosixPath


#eval "$(/home/rangoiv/miniconda3/bin/conda shell.bash hook)"
class Model:
    
    def __init__(self):
        if LOAD_TORCH:
            self.learn_inf = load('export.pkl')
        print("[MODEL] Model loaded!")

    def predict(self, t):
        if LOAD_TORCH:   
            start = time.time()
            ret = self.learn_inf.predict(t)[0]  
            print("Length", time.time() - start)
            return ret 


model = Model()

#"E:\source\Python\dataset\kvadrat\Kvadrat1.png"
#"E:\source\repos\SDL\Tryoutdataset\test\Test0.png"
