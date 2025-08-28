import numpy as np
import ezitrain.torch.pytorch_utils as ptu
from ezitrain.logger import YamlLogger, ZarrLogger, TxtLogger

x = np.array([1.2, 3.4])
x_t = ptu.from_numpy(x)
print(x_t)

logger = YamlLogger(path_to_save="./tmp/test.yml")
logger.log_kv("s", v=1)
logger.save_data()
print(logger.logger_name)


zarr_logger = ZarrLogger(
    path_to_save="./tmp/dummy.zarr", data_ks=["q", "v"], meta_ks=["date"]
)
# zarr_logger.log_meta('date')
zarr_logger.log_data(k="q", v=np.random.randn(10000, 2))
zarr_logger.save_data()

txt_logger = TxtLogger("./tmp/dummy.txt")
txt_logger.log("hello world")
