import os
import glob
import os.path as op
import multiprocessing as mp
import subprocess

def _compress(cmd):
    os.system(cmd)


if __name__ == "__main__":
    src_folder = '/home/ayanisizeco/STDF-PyTorch/Dataset/MFQEv2_dataset/test_18/' \
                'enhanced_AAAI_ModelQP37/Trained_On_QP_37_27_17/QP27/'
    target_folder = '/home/ayanisizeco/STDF-PyTorch/Dataset/To_Deliver_MP4/Test0/AAAI20/ModelQP17_27_37_EvalonQP27/'
    if not os.path.isdir(target_folder):
        os.mkdir(target_folder)

    vid_lst = glob.glob(op.join(src_folder, '*.yuv'))
    pool = mp.Pool()
    for one_vid_path in vid_lst:
        width, height = map(int, one_vid_path.split('.')[-2].split('_')[-2].split('x'))
        targ_path = os.path.join(target_folder, one_vid_path.split('/')[-1].split('.')[0] + '_AAAI20_QP27')
        # _AAAI20_QP37 vs _source vs _codec_QP37
        FPS = 25.0
        # FPS = one_vid_path.split('.')[-2].split('_')[-3][-2:]
        # YUV2MP4
        cmd = (f'ffmpeg -f rawvideo -vcodec rawvideo -s {width}x{height} -r {FPS}'
               f' -pix_fmt yuv420p -i {one_vid_path} -c:v libx264 -preset ultrafast -crf 0 {targ_path}.mp4')
        # MKV2MP4
        # cmd = (f'ffmpeg -i {one_vid_path} -c:v libx264 -preset ultrafast -crf 0 {targ_path}.mp4')

        os.system(cmd)
        pool.apply_async(
            func=_compress,
            args=(cmd,),
            callback=None
            )
