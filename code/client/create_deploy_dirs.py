import spur

path_prefix = '/deployments'

shell = spur.LocalShell()
shell.run(['sh', '-c', 'mkdir -p ' + path_prefix + '/build_dir; ' +
                       'mkdir -p ' + path_prefix + '/pre_build_dir; ' +
                       'mkdir -p ' + path_prefix + '/pkg_dir; ' +
                       'mkdir -p ' + path_prefix + '/src_dir; '])
