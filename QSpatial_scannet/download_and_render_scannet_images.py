"""
Code reference: https://github.com/ScanNet/ScanNet
"""
import os
import imageio
import struct
import numpy as np


COMPRESSION_TYPE_COLOR = {-1:'unknown', 0:'raw', 1:'png', 2:'jpeg'}
COMPRESSION_TYPE_DEPTH = {-1:'unknown', 0:'raw_ushort', 1:'zlib_ushort', 2:'occi_ushort'}


class RGBDFrame():

    def load(self, file_handle):
        self.camera_to_world = np.asarray(struct.unpack('f'*16, file_handle.read(16*4)), dtype=np.float32).reshape(4, 4)
        self.timestamp_color = struct.unpack('Q', file_handle.read(8))[0]
        self.timestamp_depth = struct.unpack('Q', file_handle.read(8))[0]
        self.color_size_bytes = struct.unpack('Q', file_handle.read(8))[0]
        self.depth_size_bytes = struct.unpack('Q', file_handle.read(8))[0]
        self.color_data = b''.join(struct.unpack('c'*self.color_size_bytes, file_handle.read(self.color_size_bytes)))
        self.depth_data = b''.join(struct.unpack('c'*self.depth_size_bytes, file_handle.read(self.depth_size_bytes)))
        
    def decompress_color(self, compression_type):
        if compression_type == 'jpeg':
            return self.decompress_color_jpeg()
        else:
            raise

    def decompress_color_jpeg(self):
        return imageio.imread(self.color_data)


class SensorData:

    def __init__(self, filename):
        self.version = 4
        self.load(filename)

    def load(self, filename):
        with open(filename, 'rb') as f:
            version = struct.unpack('I', f.read(4))[0]
            assert self.version == version
            strlen = struct.unpack('Q', f.read(8))[0]
            self.sensor_name = b''.join(struct.unpack('c'*strlen, f.read(strlen)))
            self.intrinsic_color = np.asarray(struct.unpack('f'*16, f.read(16*4)), dtype=np.float32).reshape(4, 4)
            self.extrinsic_color = np.asarray(struct.unpack('f'*16, f.read(16*4)), dtype=np.float32).reshape(4, 4)
            self.intrinsic_depth = np.asarray(struct.unpack('f'*16, f.read(16*4)), dtype=np.float32).reshape(4, 4)
            self.extrinsic_depth = np.asarray(struct.unpack('f'*16, f.read(16*4)), dtype=np.float32).reshape(4, 4)
            self.color_compression_type = COMPRESSION_TYPE_COLOR[struct.unpack('i', f.read(4))[0]]
            self.depth_compression_type = COMPRESSION_TYPE_DEPTH[struct.unpack('i', f.read(4))[0]]
            self.color_width = struct.unpack('I', f.read(4))[0]
            self.color_height =  struct.unpack('I', f.read(4))[0]
            self.depth_width = struct.unpack('I', f.read(4))[0]
            self.depth_height =  struct.unpack('I', f.read(4))[0]
            self.depth_shift =  struct.unpack('f', f.read(4))[0]
            num_frames =  struct.unpack('Q', f.read(8))[0]
            self.frames = []
            for i in range(num_frames):
                frame = RGBDFrame()
                frame.load(f)
                self.frames.append(frame)
            
    def export_color_images(self, output_dir, image_size=None, specified_frames=[]):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        print(f"Exporting {len(specified_frames)} color frames to {output_dir}")
        
        for f in specified_frames: #range(0, len(self.frames), frame_skip):
            color = self.frames[int(f)].decompress_color(self.color_compression_type)
            if image_size is not None:
                import cv2
                color = cv2.resize(color, (image_size[1], image_size[0]), interpolation=cv2.INTER_NEAREST)
                
            imageio.imwrite(os.path.join(output_dir, str(f) + '.jpg'), color)


scannet_id_and_frame = {
    'scene0015_00': ['0'],
    'scene0019_00': ['400'],
    'scene0025_00': ['500'],
    'scene0025_02': ['400'],
    'scene0030_00': ['2300'],
    'scene0030_02': ['900'],
    'scene0050_01': ['0'],
    'scene0084_00': ['600'],
    'scene0144_00': ['0', '700'],
    'scene0164_00': ['1600', '1700', '800'],
    'scene0169_00': ['0'],
    'scene0169_01': ['1000'],
    'scene0193_01': ['200', '400'],
    'scene0217_00': ['0', '1100', '400'],
    'scene0222_00': ['4800'],
    'scene0257_00': ['1200', '300'],
    'scene0278_00': ['0', '300'],
    'scene0278_01': ['0'],
    'scene0304_00': ['1500'],
    'scene0329_00': ['0'],
    'scene0329_02': ['1000'],
    'scene0351_00': ['0'],
    'scene0353_00': ['2000'],
    'scene0353_01': ['100', '2100'],
    'scene0378_00': ['0', '1800'],
    'scene0378_01': ['0', '1500', '900'],
    'scene0406_02': ['800'],
    'scene0423_01': ['0'],
    'scene0427_00': ['900'],
    'scene0430_00': ['2300'],
    'scene0458_01': ['0'],
    'scene0462_00': ['300'],
    'scene0488_00': ['100'],
    'scene0535_00': ['400'],
    'scene0553_02': ['700', '900'],
    'scene0580_00': ['0'],
    'scene0591_01': ['1000', '1300', '1700', '300', '1400'],
    'scene0593_01': ['400'],
    'scene0595_00': ['0'],
    'scene0598_01': ['600'],
    'scene0599_00': ['300'],
    'scene0599_02': ['2100'],
    'scene0606_00': ['0'],
    'scene0608_01': ['1900'],
    'scene0608_02': ['0', '2300'],
    'scene0616_00': ['0'],
    'scene0616_01': ['1400', '2200'],
    'scene0621_00': ['2300'],
    'scene0629_00': ['1400'],
    'scene0633_00': ['300'],
    'scene0643_00': ['0', '100', '1500', '300', '500'],
    'scene0644_00': ['0', '900'],
    'scene0645_01': ['1900', '2900'],
    'scene0647_00': ['600', '500'],
    'scene0647_01': ['800', '200'],
    'scene0651_00': ['400'],
    'scene0653_01': ['0', '3900', '4700'],
    'scene0678_00': ['2400', '700'],
    'scene0678_01': ['0', '2100', '800'],
    'scene0678_02': ['1300', '700'],
    'scene0696_01': ['900'],
    'scene0701_01': ['800'],
    'scene0025_01': ['1500'],
    'scene0300_00': ['0'],
    'scene0406_00': ['700'],
    'scene0583_00': ['100']
}


def main():
    
    ###### Download scans from ScanNet
    # To get `download-scannet.py`, you will need to first request the data access from ScanNet.
    # check the link: https://github.com/ScanNet/ScanNet
    for scan_id, _ in scannet_id_and_frame.items():
        # This step requires keyboard input to proceed. You might want to look into `download-scannet.py` to automate this step.
        command = f"python download-scannet.py -o scannet_dataset --id {scan_id} --type .sens --skip_existing"
        os.system(command)
    
    ###### Extract corresponding frames
    for scan_id, specified_frames in scannet_id_and_frame.items():    
        sd = SensorData(os.path.join("scannet_dataset", "scans", scan_id, f"{scan_id}.sens"))
        color_output_dir = os.path.join("images", scan_id, "color")
        sd.export_color_images(color_output_dir, specified_frames=specified_frames)
        

if __name__ == '__main__':
    main()