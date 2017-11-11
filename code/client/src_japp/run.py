import spur

shell = spur.LocalShell()
""" Replace 'jay' below with your own username"""
shell.run(['sh', '-c', 'cd /home/jay/fw_test; touch TEST_DEPLOY_FILE'])
print('hello world')
