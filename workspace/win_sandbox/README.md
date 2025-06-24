# Windows Sandbox

see [windows-sandbox-configure](https://learn.microsoft.com/zh-cn/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file)

双击配置文件即可以该配置新建运行沙盒

## 案例

在安全环境中测试某软件，关闭 GPU 虚拟化，禁止联网，对文件夹只读权限，开机打开文件夹

```xml
<Configuration>
  <vGpu>Disable</vGpu>
  <Networking>Disable</Networking>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>C:\Users\Public\Downloads</HostFolder>
      <SandboxFolder>C:\Users\WDAGUtilityAccount\Downloads</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
  </MappedFolders>
  <LogonCommand>
    <Command>explorer.exe C:\users\WDAGUtilityAccount\Downloads</Command>
  </LogonCommand>
</Configuration>
```
