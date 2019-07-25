# FileMaker-Server-Zabbix-Templates
Soliant FileMaker Server Zabbix Templates

These are the Zabbix templates that we have developed to monitor FileMaker Server deployments.

See the guides on how to get started with these: https://www.soliantconsulting.com/labs/filemaker-zabbix

The short version:
Typically you'll want to download and import all of the templates into your Zabbix server.  And then for each FileMaker Server you want to monitor, select the template for your FileMaker Server's operating system.  That master template will inherit the sub templates that apply to that OS.

The "scripts" folder contains the script we use to talk the FileMaker Server Admin API to retrieve some configuration settings.  FM Cloud and macOS use the python script, Windows servers need the PowerShell script.  See the Agent configuration guide for more details.
