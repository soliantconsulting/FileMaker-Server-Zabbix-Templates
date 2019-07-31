# FileMaker-Server-Zabbix-Templates
Soliant FileMaker Server Zabbix Templates

These are the Zabbix templates and supporting files that we have developed to monitor FileMaker Server deployments.

See the guides on how to get started with these templates: https://www.soliantconsulting.com/tag/zabbix/

## The short version:
Download and import the zabbix template XML file into your Zabbix server.  Then for each FileMaker Server you want to monitor, select the template for your FileMaker Server's operating system:
- Soliant FMS Mac
- Soliant FMS Windows
- Soliant FMS FMC

There will be more templates listed, but these are the master ones. That master template will inherit the sub templates that apply to that OS.

The "scripts" folder contains the script we use to talk the FileMaker Server Admin API to retrieve some configuration settings.  FM Cloud and macOS use the python script, Windows servers need the PowerShell script.  See the Agent configuration guide for more details.
