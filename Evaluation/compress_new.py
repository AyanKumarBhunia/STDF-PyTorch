import os
import glob
import yaml
import os.path as op
import multiprocessing as mp
from generate_video_cfg import generate_vid_cfg

def _compress(cmd, tmp_save_bit_path):
    os.system(cmd)
    os.remove(f'{tmp_save_bit_path}')


# load parameters
with open('option.yml', 'r') as fp:
    opts_dict = yaml.load(fp, Loader=yaml.FullLoader)

assert opts_dict['system'] == 'ubuntu', 'Not implemented.'
dir_dataset = opts_dict['dir_dataset']
qp = opts_dict['qp']

# for phase in ['test_18', 'train_108']:
for phase in ['train_108']:
    # ===== unzip ======
    # zip_name_pre = phase + '.z*'
    zip_name = phase + '.zip'
    print(f'\nunziping {zip_name}...')
    zip_path = op.join(dir_dataset, zip_name)
    target_path = dir_dataset  # inside: test_18/
    os.system(f'zip -s 0 {zip_path} --out unsplit.zip')
    os.system(f'unzip unsplit.zip -d {target_path}')
    os.remove('unsplit.zip')
    #os.remove(f'{op.join(dir_dataset, zip_name_pre)}')
    print('> done.')

    # === generate video configuration files ===
    print(f'\ngenerating cfg...')
    # os.system(f'python scripts/generate_video_cfg.py {dir_dataset} {phase}')
    generate_vid_cfg(dir_dataset, phase)
    print('> done.')

    # ===== run ===== #
    enc_path = 'TAppEncoderStatic'
    enc_cfg_path = f'encoder_cfg_LDP/encoder_LDP_QP{qp}.cfg'
    vid_lst = glob.glob(op.join(dir_dataset, phase, 'raw', '*.yuv'))
    pool = mp.Pool()  # default processes: cpu core num
    for idx_vid, vid_path in enumerate(vid_lst):
        vid_name = vid_path.split('/')[-1].split('.')[-2]
        vid_cfg_path = f'video_cfg/{phase}/{vid_name}.cfg'
        save_cmp_path = vid_path.replace('raw', f'HM16.5_LDP/QP{qp}')
        save_log_path = save_cmp_path.replace('.yuv', '.txt')
        tmp_save_bit_path = save_cmp_path.replace('.yuv', '.bin')

        save_dir = op.dirname(save_cmp_path)
        if not op.exists(save_dir):
            os.makedirs(save_dir)

        cmd = (
            f'./{enc_path} -c {enc_cfg_path} -c {vid_cfg_path} -o ' 
            f'{save_cmp_path} -b {tmp_save_bit_path} >{save_log_path}'
            )  # sh ./ will cause error!

        print(f'\n{idx_vid + 1}/{len(vid_lst)}: compressing {vid_name}...')
        pool.apply_async(
            func=_compress,
            args=(cmd, tmp_save_bit_path, ),
            callback=None
            )
    pool.close()
    pool.join()
    print("> done.")
