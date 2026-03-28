# LESSONS.md - 观复阁历史教训时间线

> 本文档按时间线记录每次重大事件教训。
> 所有成员可撰写，COO 维护索引。

---

## 2026-03-22 软件误删事件

**关键词：** 卸载、rmdir、递归删除、INNO SETUP

**核心教训：**
- 卸载必须用正规方式（uninstall_string / msiexec / winget）
- 禁止使用 rmdir /s /q、Remove-Item -Recurse
- 禁止使用通配符（Uninstall *.exe）
- 执行破坏性操作前必须向用户确认

**参考文档：**
- `guanfu/team-knowledge/破坏性操作安全准则.md`
- `guanfu/team-knowledge/团队教训.md`

**教训来源：** 观复执行卸载"智谱清言"和"GLM-PC"时操作失误，导致微信、QQ、向日葵等C盘软件被损坏。

---

*最后更新：2026-03-23*
*更新者：阁影（COO）*
