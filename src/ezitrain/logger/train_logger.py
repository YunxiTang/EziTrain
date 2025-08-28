import os
import numpy as np
import wandb
from tensorboardX import SummaryWriter
from omegaconf import  OmegaConf
from .txt_logger import TxtLogger
import PIL


class TrainLogger:
    """
        Train Logging class to log metrics to wandb/tensorboard 
        (with retrieve running statistics about logged data as an optional).
    """
    def __init__(self, 
                 log_dir: str, 
                 project: str,
                 experiment_name: str,
                 meta_cfg: OmegaConf=None,
                 train_cfg: OmegaConf=None,
                 model_cfg: OmegaConf=None,
                 wandb_entity=None, 
                 wandb_mode: str = 'online', 
                 log_wandb=True, 
                 local_logger=False,
                 log_tb=False):
        """
        Args:
            log_dir (str): directory to store logs
        """
        self._wandb_logger = None
        self._local_logger = None
        self._tb_logger = None
        self._data = dict() 

        if log_tb:
            self._tb_logger = SummaryWriter(os.path.join(log_dir), flush_secs=1, max_queue=1)

        if log_wandb:
            self._wandb_logger = wandb.init(entity=wandb_entity,
                                            project=project,
                                            name=experiment_name,
                                            dir=log_dir,
                                            mode=wandb_mode,
                                            )

            # set up info experiment identification (meta + train + model)
            wandb_config = dict()
            if meta_cfg is not None:
                for (k, v) in meta_cfg.items():
                    wandb_config[k] = v
                    
            if train_cfg is not None:
                for (k, v) in train_cfg.items():
                    wandb_config[k] = v
                    
            if model_cfg is not None:
                for (k, v) in model_cfg.items():
                    wandb_config[k] = v

            wandb.config.update(wandb_config)

        if local_logger:
            path_to_save = os.path.join(log_dir, experiment_name)
            self._local_logger = TxtLogger(path_to_save, experiment_name)
            self._local_logger.log('Logging to local file: {}'.format(path_to_save))


    def log(self, k, v, epoch, data_type='scalar', log_stats=False):
        """
        Record data with logger.
        Args:
            k (str): key string
            v (float or image): value to store
            epoch: current epoch number
            data_type (str): the type of data. either 'scalar' or 'image'
            log_stats (bool): whether to store the mean/max/min/std for all logged data with key k
        """

        assert data_type in ['scalar', 'image']

        if data_type == 'scalar':
            if log_stats or k in self._data: 
                if k not in self._data:
                    self._data[k] = []
                self._data[k].append(v)
                
        # log to tensorboardX
        if self._tb_logger is not None:
            if data_type == 'scalar':
                self._tb_logger.add_scalar(k, v, epoch)

                if log_stats:
                    stats = self.get_stats(k)
                    for (stat_k, stat_v) in stats.items():
                        stat_k_name = '{}-{}'.format(k, stat_k)
                        self._tb_logger.add_scalar(stat_k_name, stat_v, epoch)

            elif data_type == 'image':
                self._tb_logger.add_images(k, img_tensor=v, global_step=epoch, dataformats="NHWC")
        
        # log to wandb
        if self._wandb_logger is not None:
            try:
                if data_type == 'scalar':
                    self._wandb_logger.log({k: v}, step=epoch)

                    if log_stats:
                        stats = self.get_stats(k)
                        for (stat_k, stat_v) in stats.items():
                            self._wandb_logger.log(
                                {"{}/{}".format(k, stat_k): stat_v}, 
                                step=epoch
                                )

                elif data_type == 'image':
                    image = PIL.Image.fromarray(v)
                    self._wandb_logger.log(
                        {k: wandb.Image(image)},
                        step=epoch
                    )
                
            except Exception as e:
                print("wandb logging: {}".format(e))

        # log to local logger
        if self._local_logger is not None:
            if data_type == 'scalar':
                self._local_logger.log(f'{k}: {v}')
            else:
                raise ValueError("Only scalar data types are supported for local logging.")
                
        return None

    def get_stats(self, k):
        """
        Computes running statistics for a particular key.
        Args:
            k (str): key string
        Returns:
            stats (dict): dictionary of statistics
        """
        stats = dict()
        stats['mean'] = np.mean(self._data[k])
        stats['std'] = np.std(self._data[k])
        stats['min'] = np.min(self._data[k])
        stats['max'] = np.max(self._data[k])
        return stats


    def close(self):
        """
            Run before terminating to make sure all logs are flushed
        """
        if self._wandb_logger is not None:
            self._wandb_logger.finish()
            
        if self._local_logger is not None:
            pass