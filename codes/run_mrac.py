import numpy as np
import os

from envs import MracEnv
from agents import NullAgent
from utils import load_spec

import torch

import fym.logging as logging


BASE_LOG_DIR = os.path.join('data', 'mrac')


def parse_data(env, data):
    data = env.data_postprocessing(data)
    path = os.path.join(BASE_LOG_DIR, env.logger.basename)
    logging.save(path, data)


def main():
    spec = load_spec('spec.json')
    env = MracEnv(spec, data_callback=parse_data)
    agent = NullAgent(env)
    logger = logging.Logger(log_dir=BASE_LOG_DIR, file_name='episodic.h5')

    obs = env.reset()

    while True:
        with torch.no_grad():
            action = agent.act(obs)

        next_obs, reward, done, info = env.step(action)

        logger.record(**info)

        obs = next_obs

        if done:
            break

    env.close()
    logger.close()

    data = logging.load(logger.path)
    data = env.data_postprocessing(data)
    logging.save(logger.path, data)


if __name__ == '__main__':
    main()
