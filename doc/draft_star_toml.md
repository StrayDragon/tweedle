- 根据预设的路径派发配置文件(软链接等手段)
- 建立同步文件仓库联系,为同步仓库提供管理接口

预设文件(stubs)字段需能够表现:
- [ ] pre-required apps 前置需求应用
- [ ] configs lookup path 应用配置查找路径,由表及里
  - user path 当前用户路径
  - root path 需要root权限的路径
  - $ENV condition path 有环境变量条件的路径 **ps:** 此状态无法直接写在配置中,需要重构stub状态


1.检查当前用户配置与内置默认情况的hit程度
  - 如果全部hit,则进行下一步
  - 否则开始自动探测模式(由表及里的进行测试,首个作为hit)
  - [ ] 重构1.的代码
2.将所有配置集中管理(用git管理),到自身的配置文件夹中
  - git 子命令设置(init,add,commit,remote(optional),push(optional))
3.派发配置,作软链接
