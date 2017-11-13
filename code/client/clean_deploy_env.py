import spur

path_prefix = '/home/jay'

shell = spur.LocalShell()
shell.run(['sh', '-c', 'rm -r ' + path_prefix + '/fw_test/build_dir/*; ' +
                       'rm -r ' + path_prefix + '/fw_test/pre_build_dir/*; ' +
                       'rm -r ' + path_prefix + '/fw_test/pkg_dir/*; '])
