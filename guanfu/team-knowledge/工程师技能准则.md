# 工程师技能准则

> 工程师（CTO/Echo）的技能标准和行为规范。
> 本文档由工程师编写，所有成员可提出修改意见。
> 最后更新：2026-03-28

---

## 一、核心职责

工程师的核心职责是**用代码解决问题**，并确保解决方案：
1. **正确** - 功能实现正确，结果可验证
2. **可维护** - 代码清晰，他人能理解和修改
3. **可测试** - 有测试覆盖，敢重构
4. **安全** - 无漏洞，不泄露数据

---

## 二、代码标准（必须遵守）

### 2.1 代码质量

| 标准 | 要求 | 检验方式 |
|------|------|----------|
| 类型提示 | 所有函数必须有 type hints | 代码审查 |
| 错误处理 | 所有 I/O 操作必须有 try/except | 代码审查 |
| 单一职责 | 函数不超过 50 行 | 代码审查 |
| 命名规范 | 变量/函数用 snake_case，类用 PascalCase | PEP 8 |
| 注释 | 解释"为什么"，不解释"是什么" | 代码审查 |

### 2.2 安全底线

- ❌ 硬编码密码/凭证
- ❌ 用户输入不验证直接用于 SQL/命令
- ❌ 直接在 master/main 分支操作
- ❌ 使用未经测试的第三方库
- ✅ 所有外部输入必须验证
- ✅ 凭证通过环境变量或配置文件读取
- ✅ 破坏性操作前必须用户确认

### 2.3 错误处理规范

```python
# ✅ 正确示例
def read_file(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {path}")
    except PermissionError:
        raise PermissionError(f"无权限读取: {path}")

# ❌ 错误示例
def read_file(path):
    return open(path).read()  # 无类型提示、无错误处理
```

### 2.4 模块化规范

```
项目结构示例：
├── src/              # 源代码
│   ├── __init__.py
│   ├── core.py        # 核心逻辑
│   └── utils.py       # 工具函数
├── tests/             # 测试
│   ├── __init__.py
│   └── test_core.py
├── docs/              # 文档
├── README.md          # 项目说明
└── requirements.txt   # 依赖
```

---

## 三、版本控制规范

### 3.1 Commit Message 格式

```
<类型>: <简短描述>

<可选的详细说明>

类型：
- feat: 新功能
- fix: 修复 bug
- test: 添加测试
- docs: 文档更新
- refactor: 重构
- chore: 杂项
```

**示例：**
```
feat: 添加用户认证模块

- 实现 JWT token 验证
- 添加 refresh token 逻辑
- 更新 README 说明
```

### 3.2 分支管理

- ❌ 禁止直接在 main/master 分支操作
- ✅ 功能开发使用 feature/xxx 分支
- ✅ 合并前必须 code review
- ✅ 测试通过后才能合并

---

## 四、测试规范

### 4.1 测试覆盖率要求

| 模块类型 | 最低覆盖率 |
|----------|-----------|
| 核心业务逻辑 | 80% |
| 工具函数 | 70% |
| 接口/API | 60% |

### 4.2 测试命名

```python
class TestUserAuthentication:
    def test_login_success(self):
        """正常登录返回用户信息"""
        ...
    
    def test_login_wrong_password(self):
        """密码错误返回 401"""
        ...
    
    def test_login_user_not_found(self):
        """用户不存在返回 404"""
        ...
```

---

## 五、文档规范

### 5.1 README.md 必须包含

```markdown
# 项目名称

## 功能描述
一句话说明项目做什么。

## 安装
```bash
pip install -r requirements.txt
```

## 使用
```python
from project import main

main()
```

## 测试
```bash
pytest tests/ -v
```

## 依赖
- Python >= 3.10
- 第三方库列表
```

### 5.2 函数文档

```python
def calculate_t_loss(i_decay: float, delta_r: float, w_rate: float) -> float:
    """
    计算信任损耗 T_loss。
    
    T_loss = α·I_decay + β·ΔR + γ·W_rate
    
    Args:
        i_decay: 信息衰减率，范围 [0, 1]
        delta_r: 决策分歧轮次，非负整数
        w_rate: 返工率，范围 [0, 1]
    
    Returns:
        T_loss 值，范围 [0, 1]
    
    Raises:
        ValueError: 参数超出有效范围
    
    Example:
        >>> calculate_t_loss(0.1, 2, 0.05)
        0.115
    """
    ...
```

---

## 六、今天学到的教训（2026-03-28）

### 6.1 阁主指出的问题

**问题：** 代码标准流于表面，追求"能跑"而非"正确"。

**具体表现：**
- 认为功能实现就够了，忽略可维护性
- 无类型提示、无错误处理、无模块化
- print 代替 logging
- 没有 README

**根本原因：**
- 追求速度，忽略质量
- 认为"自己能看懂"就够了
- 忽略团队协作需求

### 6.2 正确的态度

| 错误态度 | 正确态度 |
|----------|----------|
| "能跑就行" | "能跑 + 能维护 + 能测试" |
| "我看得懂就行" | "任何人都能看懂" |
| "事后补文档" | "代码即文档" |
| "功能优先" | "正确性优先" |

---

## 七、执行检查清单

每次提交代码前检查：

- [ ] 类型提示完整
- [ ] 错误处理到位
- [ ] 有测试用例
- [ ] README 已更新
- [ ] commit message 规范
- [ ] 无硬编码凭证
- [ ] 代码格式符合 PEP 8

---

## 八、相关文档

- `guanfu/team-knowledge/lessons/` - 历史教训
- `guanfu/team-knowledge/best-practices/` - 最佳实践
- `projects/` - 项目代码

---

*工程师技能准则 v1.0*
*更新者：Echo（工程师）*
*日期：2026-03-28*
