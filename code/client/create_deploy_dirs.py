import spur

path_prefix = '/home/jay'

shell = spur.LocalShell()
shell.run(['sh', '-c', 'mkdir -p ' + path_prefix + '/fw_test/build_dir; ' +
                       'mkdir -p ' + path_prefix + '/fw_test/pre_build_dir; ' +
                       'mkdir -p ' + path_prefix + '/fw_test/pkg_dir; ' +
                       'mkdir -p ' + path_prefix + '/fw_test/src_dir; '])
