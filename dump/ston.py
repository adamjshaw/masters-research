####
#!/usr/bin/env python

import cine, os, subprocess, struct
from math import *

sparse_location = '2013_12_05_bigtf_psi50_spacer6_dye_I.sparse' 
s4d_location = '2013_12_05_bigtf_psi50_spacer6_dye_I.s4d' 

sparse = cine.open(sparse_location)
#print "zero offset: %d\n" % sparse.zero_offset
#print "block offsets:"
#for i,j in enumerate(sparse.block_offsets[:10]):
    #sparse.f.seek(sparse.zero_offset + j)
    #block_length = struct.unpack('Q', sparse.f.read(struct.calcsize('Q')))[0]
    #desc, header_size, data_size = struct.unpack('8s2Q', sparse.f.read(24))
    #print "block %d: length %u header_length %u position %u " % (i, data_size, header_size, sparse.zero_offset + j + 8 + header_size)
#    a = sparse.read_block(i)
#print sparse.max_blocks, len(sparse.block_offsets)
height, width = sparse.header['im_height'], sparse.header['im_width']
s4d = cine.Sparse4D(s4d_location)
num_frames = len(s4d) #number of volumes in the experiment
#print num_frames
setup_info = s4d.header['3dsetup']
exec(setup_info)
#print cine_depth
#print len(sparse.block_offsets)
[a0, a1], a2 = frame_shape[:2], display_frames[-1] - display_frames[0]
nrrd_command = 'unu make -h -i %s -s %d %d %d -cn cell cell cell -t ushort -en little -e gzip -spc LPS -orig "(0,0,0)" -dirs "(1,0,0) (0,1,0) (0,0,1)" -o %s.nrrd' % (sparse_location, a1, a0, a2, sparse_location)
subprocess.Popen(nrrd_command, shell=True)
'''for f in range(1):
	raw_out = '2014_10_21_EXAMPLE_FRAME_%03d.raw'%f
	raw = open(raw_out, 'wb')
	for i in range(340,341):
		slice = sparse[i].astype('f')
		slice_reduced = slice / slice.max() * 2.**12.
		raw.write(slice_reduced.astype('u2').tostring())
	raw.close()
	os.system('gzip '+raw_out)
'''
'''for f in range(num_frames):
	raw_out = '2014_10_21_EXAMPLE_FRAME_%03d.raw'%f
	raw = open(raw_out, 'wb')
	for i in range(f * cine_depth + len(display_frames)):
		slice = sparse[i].astype('f')
		slice_reduced = slice / slice.max() * 2.**12.
		raw.write(slice_reduced.astype('u2').tostring())
	raw.close()
	os.system('gzip '+raw_out)
'''

output = \
"NRRD0006\n\
type: unsigned short\n\
dimension: 3\n\
space: left-posterior-superior\n\
sizes: 384 384 385\n\
space directions: (1,0,0) (0,1,0) (0,0,1)\n\
centerings: cell cell cell\n\
endian: little\n\
encoding: zrl\n\
space origin: (0,0,0)\n\
data file: SKIPLIST 2\n"
print num_frames, cine_depth
start = 0
for f in range(num_frames):
  print f
  full_output = output
  nrrd_out = open("%s-%03d.nhdr" % (sparse_location, f), "w")
  nrrd_out.write(output) 
  for i in display_frames:
    i += f * cine_depth
    sparse.f.seek(sparse.zero_offset + sparse.block_offsets[i])
    block_length = struct.unpack('Q', sparse.f.read(struct.calcsize('Q')))[0]
    desc, header_size, data_size = struct.unpack('8s2Q', sparse.f.read(24))
    #print "block %d: length %u header_length %u position %u " % (i, data_size, header_size, sparse.zero_offset + sparse.block_offsets[i] + 8 + header_size)
    out_line = "%u %s\n" % (sparse.zero_offset + sparse.block_offsets[i] + 8 + header_size, sparse_location)
    nrrd_out.write(out_line)
  nrrd_out.close()
  start = i
