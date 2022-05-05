import ipdb
from omegaconf import DictConfig
from tqdm import tqdm

from character_encoder.src.datamodules.latent_bbox_datamodule import (
    LatentBboxDataModule,
)


def debug(config: DictConfig):
    # Initialize dataset
    data_module = LatentBboxDataModule(
        split_dir=config.datamodule.split_dir,
        unity_dir=config.datamodule.unity_dir,
        prcpt_dir=config.datamodule.raft_dir,
        n_frames=config.model.n_frames,
        stride=config.model.stride,
        frame_size=config.model.frame_size,
        batch_size=config.compnode.batch_size,
        num_workers=config.compnode.num_workers,
    )

    train_dataloader = data_module.train_dataloader()

    ipdb.set_trace()
    for batch in tqdm(train_dataloader):
        ipdb.set_trace()
