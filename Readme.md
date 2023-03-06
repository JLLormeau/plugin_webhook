# Plugin Webhook
![image](https://user-images.githubusercontent.com/40337213/223125054-62b49f14-5f77-4f82-ae98-95d37b2605ba.png)

[Download ZIP](https://github.com/JLLormeau/plugin_webhook/raw/main/custom.remote.python.webhook.zip)
[Doc](https://github.com/JLLormeau/plugin_webhook/blob/main/Dynatrace_PluginWebhook.pdf)

0) Prerequisite : Token scope: `problems read`, `problems write`
1) Upload `custom.remote.python.webhook.zip` on UI
3) Unzip  `custom.remote.python.webhook.zip` on AG 
4) Restart `remotepluginmodule` service on AG
5) Configure endpoint on UI 


![image](https://user-images.githubusercontent.com/40337213/223127129-6727168e-7c1a-470b-9aac-e15f647d5510.png)

## Generate endpoint from notification (optionnal)

0) Prerequisite : 
- Token scope: `configurations read`, `configurations write`
- Python 3.6+, module requests

1) Set variable 

       export MyTenan=yyyy.live.dynatrace.com (without https://)
       export MyToken=xxxx
       export ActiveGateId=zzzz
       
2) run the python script 

       python3 Create_webhook_from_notification.py 
