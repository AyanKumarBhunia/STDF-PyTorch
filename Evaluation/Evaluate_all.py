import os
import glob
import os.path as op
import multiprocessing as mp
import subprocess
import json
import pickle
import numpy as np

def get_cmd_evaluate(encoded_file, original_input_file, vmaf_file):

    cmd = (f'LD_LIBRARY_PATH=/home/ayanisizeco/ffmpeg/libs_antihacking /home/ayanisizeco/ffmpeg/ffmpeg_antihacking' 
           f' -i  {encoded_file}'
           f' -i {original_input_file} -lavfi libvmaf="model_path='
           f'/home/ayanisizeco/ffmpeg/model/vmaf_v0.6.1.pkl:psnr=1:ssim=1:ms_ssim=1:log_fmt=json:log_path={vmaf_file}"'
           f' -f null -')
    return cmd


def _compress(cmd):
    os.system(cmd)

class Counter():
    def __init__(self):
        self.reset()

    def reset(self):
        self.file_name = []
        self.Codec_VMAF = []
        self.Codec_PSNR = []
        self.Codec_SSIM = []
        self.Codec_MSSSIM = []
        self.Enhanced_VMAF = []
        self.Enhanced_PSNR = []
        self.Enhanced_SSIM = []
        self.Enhanced_MSSSIM = []

    def accum(self, filename, Codec_Score, enhanced_score):

        self.file_name.append(filename)
        self.Codec_VMAF.append(Codec_Score[0])
        self.Codec_PSNR.append(Codec_Score[1])
        self.Codec_SSIM.append(Codec_Score[2])
        self.Codec_MSSSIM.append(Codec_Score[3])

        self.Enhanced_VMAF.append(enhanced_score[0])
        self.Enhanced_PSNR.append(enhanced_score[1])
        self.Enhanced_SSIM.append(enhanced_score[2])
        self.Enhanced_MSSSIM.append(enhanced_score[3])

    def get_ave(self):
        self.avg_Codec_VMAF = np.mean(self.Codec_VMAF)
        self.avg_Codec_PSNR = np.mean(self.Codec_PSNR)
        self.avg_Codec_SSIM = np.mean(self.Codec_SSIM)
        self.avg_Codec_MSSSIM = np.mean(self.Codec_MSSSIM)

        self.avg_Enhanced_VMAF = np.mean(self.Enhanced_VMAF)
        self.avg_Enhanced_PSNR = np.mean(self.Enhanced_PSNR)
        self.avg_Enhanced_SSIM = np.mean(self.Enhanced_SSIM)
        self.avg_Enhanced_MSSSIM = np.mean(self.Enhanced_MSSSIM)

        with open('company_data.pkl', 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

        VMAF_Gain = self.avg_Enhanced_VMAF  - self.avg_Codec_VMAF
        PSNR_Gain = self.avg_Enhanced_PSNR  - self.avg_Codec_PSNR
        SSIM_Gain = self.avg_Enhanced_SSIM  - self.avg_Codec_SSIM
        MSSSIM_Gain = self.avg_Enhanced_MSSSIM  - self.avg_Codec_MSSSIM

        print(f'VMAF_gain: {VMAF_Gain} \n PSNR_Gain: {PSNR_Gain} \n '
              f'SSIM_Gain: {SSIM_Gain} \n MSSSIM_Gain: {MSSSIM_Gain}')


if __name__ == "__main__":
    raw_folder = '/home/ayanisizeco/STDF-PyTorch/Dataset/To_Deliver_MP4/Test0/source/'
    enhanced_folder = '/home/ayanisizeco/STDF-PyTorch/Dataset/To_Deliver_MP4/Test0/AAAI20/'
    codec_folder = '/home/ayanisizeco/STDF-PyTorch/Dataset/To_Deliver_MP4/Test0/codec/'

    vmaf_folder = './Results'
    vid_lst = glob.glob(op.join(enhanced_folder, '*.mp4'))
    util_counter = Counter()
    # pool = mp.Pool()

    for one_vid_path in vid_lst:

        enhanced_file = one_vid_path
        filename = os.path.basename(enhanced_file).split('_AAAI')[0]
        original_input_file = os.path.join(raw_folder, filename + '_source.mp4')
        codec_file = os.path.join(codec_folder, filename + '_codec_QP37.mp4')

        vmaf_file = os.path.join(vmaf_folder,  filename + '_enhanced.json')
        cmd = get_cmd_evaluate(enhanced_file, original_input_file, vmaf_file)
        os.system(cmd)
        with open(vmaf_file) as f:
            data = json.load(f)
        enhanced_score = [data['VMAF score'], data['PSNR score'], data['SSIM score'], data['MS-SSIM score']]

        # (evaluate_results, err)  = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
        # pool.apply_async(func=_compress, args=(cmd,), callback=None)

        vmaf_file = os.path.join(vmaf_folder, filename + '_codec.json')
        cmd = get_cmd_evaluate(codec_file, original_input_file, vmaf_file)
        os.system(cmd)
        with open(vmaf_file) as f:
            data = json.load(f)
        codec_score = [data['VMAF score'], data['PSNR score'], data['SSIM score'], data['MS-SSIM score']]

        util_counter.accum(filename, codec_score, enhanced_score)

    util_counter.get_ave()

        #
