:: Note: I do not use Windows regularly. This script was contributed by a different user.
:: The following command should be pasted in to the Command Prompt (CMD)
:: PowerShell may or may not work

py.exe -3 __main__.py --api_url "http://127.0.0.1:45869/"  -H "localhost" -P "45868" -r "my-rules" "default-rules" -k "[API Key Here]"
