# no maximum nfs restriction. for test videos.
# video name: VideoName_widthxheight_nfs.yuv
import glob
import os
import sys
import os.path as op


# dir_dataset = sys.argv[1]
# tab = sys.argv[2]  # test_18 | train_108


def generate_vid_cfg(dir_dataset, tab):
    # raw_video_dir = op.join(dir_dataset, f'{tab}/raw') # OLD AAAI One
    raw_video_dir = op.join(dir_dataset, f'{tab}/') # NEW New One
    cfg_save_dir = f'./video_cfg/{tab}'



    if not os.path.exists(cfg_save_dir):
        os.makedirs(cfg_save_dir)

    # find all raw videos
    raw_video_list = glob.glob(os.path.join(raw_video_dir, "*.yuv"))
    num_videos = len(raw_video_list)
    print(f'{num_videos} videos found.')

    # generate VideoName.cfg and save
    for ite_vid in range(num_videos):
        raw_video_path = raw_video_list[ite_vid]
        raw_video_name = os.path.basename(raw_video_path).split(".")[0]
        # _res = raw_video_name.split("_")[1]
        width = raw_video_name.split("_")[-2].split("x")[0]
        height = raw_video_name.split("_")[-2].split("x")[1]
        nfs = raw_video_name.split("_")[-1]

        cfg_path = os.path.join(cfg_save_dir, raw_video_name + ".cfg")
        fp = open(cfg_path, 'w')
        print(width, height, nfs)

        _str = "#======== File I/O ===============\n"
        fp.write(_str)
        video_path = os.path.join(raw_video_dir, raw_video_name + ".yuv")
        _str = "InputFile                     : " + video_path + "\n"
        fp.write(_str)
        _str = "InputBitDepth                 : 8           # Input bitdepth\n"
        fp.write(_str)
        _str = "InputChromaFormat             : 420         # Ratio of luminance to chrominance samples\n"
        fp.write(_str)
        _str = "FrameRate                     : 50          # Frame Rate per second\n"
        fp.write(_str)
        _str = "FrameSkip                     : 0           # Number of frames to be skipped in input\n"
        fp.write(_str)
        _str = "SourceWidth                   : " + width + "        # Input  frame width\n"
        fp.write(_str)
        _str = "SourceHeight                  : " + height + "        # Input  frame height\n"
        fp.write(_str)
        _str = "FramesToBeEncoded             : " + nfs + "         # Number of frames to be coded\n"
        fp.write(_str)
        _str = "Level                         : 3.1\n"
        fp.write(_str)

        fp.close()
