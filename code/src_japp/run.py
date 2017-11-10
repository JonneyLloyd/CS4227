import spur

shell = spur.LocalShell()
shell.run(['sh', '-c', 'cd /home/jay/fw_test; touch TEST_DEPLOY_FILE'])
print('hello world')
