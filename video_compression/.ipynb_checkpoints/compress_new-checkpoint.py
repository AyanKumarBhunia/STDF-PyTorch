import os
import glob
import yaml
import os.path as op
import multiprocessing as mp
from generate_video_cfg_New import generate_vid_cfg

def _compress(cmd, tmp_save_bit_path):
    os.system(cmd)
    os.remove(f'{tmp_save_bit_path}')

if __name__ == "__main__":
    # load parameters
    with open('option.yml', 'r') as fp:
        opts_dict = yaml.load(fp, Loader=yaml.FullLoader)

    assert opts_dict['system'] == 'ubuntu', 'Not implemented.'
    dir_dataset = opts_dict['dir_dataset']
    qp = opts_dict['qp']

    phase = 'UGC_Orig_YUV'
    src_folder = '/home/ayanisizeco/STDF-PyTorch/Dataset/UGC/'
    target_folder = '/home/ayanisizeco/STDF-PyTorch/Dataset/XIPH_HD/UGC_Codec_YUV/'
    generate_vid_cfg(src_folder, phase)
# ===== run ===== #
    enc_path = 'TAppEncoderStatic'
    enc_cfg_path = f'encoder_cfg_LDP/encoder_LDP_QP{qp}.cfg'
    vid_lst = glob.glob(op.join(src_folder, phase, '*.yuv'))
    pool = mp.Pool()  # default processes: cpu core num
    for idx_vid, vid_path in enumerate(vid_lst):
        vid_name = vid_path.split('/')[-1].split('.')[-2]
        vid_cfg_path = f'video_cfg/{phase}/{vid_name}.cfg'

        save_cmp_path = os.path.join(target_folder, os.path.basename(vid_path))
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
