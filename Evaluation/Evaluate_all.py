import os
import glob
import os.path as op
import multiprocessing as mp
import subprocess


def get_cmd_evaluate(encoded_file, original_input_file):

    cmd = (f'LD_LIBRARY_PATH=/home/ayanisizeco/ffmpeg/libs_antihacking /home/ayanisizeco/ffmpeg/ffmpeg_antihacking' 
           f'-i  {encoded_file}'
           f'-i {original_input_file} -lavfi libvmaf="model_path='
           f'./model/vmaf_v0.6.1.pkl:psnr=1:ssim=1:ms_ssim=1:log_fmt=json:log_path=./vmaf.json" -f null -')
    return cmd

def _compress(cmd):
    os.system(cmd)


if __name__ == "__main__":
    raw_folder = '/home/ayanisizeco/STDF-PyTorch/Dataset/To_Deliver_MP4/Test0/source/'
    sample_folder = '/home/ayanisizeco/STDF-PyTorch/Dataset/To_Deliver_MP4/Test0/AAAI20/'
    vid_lst = glob.glob(op.join(raw_folder, '*.yuv'))
    pool = mp.Pool()

    for one_vid_path in vid_lst:
    #Get the video paths
        original_input_file = one_vid_path
        encoded_file = one_vid_path.split('_')

        cmd = get_cmd_evaluate(encoded_file, original_input_file)
        (nb_frames, err)  = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()

        #
