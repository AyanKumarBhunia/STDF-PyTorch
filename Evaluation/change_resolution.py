# fmpeg -i crowdrun.mp4 -pix_fmt yuv444p crowdrun.yuv
# ffmpeg -i crowdrun.mp4 -vf scale=640:360 -sws_flags lanczos -c:v libx264 -preset ultrafast -crf 0 crowdrun_source_360p.mp4
# ffmpeg -i file.mkv -pix_fmt yuv444p file.yuv

import os
import glob
import os.path as op
import multiprocessing as mp
import subprocess

def _compress(cmd):
    os.system(cmd)


if __name__ == "__main__":
    src_folder = '/home/ayanisizeco/STDF-PyTorch/Dataset/XIPH_HD/MP4_Orig/'
    target_folder = '/home/ayanisizeco/STDF-PyTorch/Dataset/XIPH_HD/MP4_Orig_360p/'
    if not os.path.isdir(target_folder):
        os.makedirs(target_folder)
    vid_lst = glob.glob(op.join(src_folder, '*.mp4'))
    # pool = mp.Pool()
    for one_vid_path in vid_lst:
        target_path = os.path.join(target_folder, os.path.basename(one_vid_path).replace("1080p", "360p"))
        cmd = (f'ffmpeg -i {one_vid_path} -vf scale=640:360 -sws_flags lanczos -c:v libx264 -preset ultrafast -crf 0 {target_path}')
        os.system(cmd)
