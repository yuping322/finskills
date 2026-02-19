# A股Skills优化与完善 - 设计文档

## 1. 设计概述

### 1.1 设计目标
基于需求文档，设计一套完整的优化方案，包括性能优化框架、边界条件处理框架、用户体验优化、文档完善和测试覆盖。

### 1.2 设计原则
- **最小侵入性**: 优化不影响现有功能
- **可扩展性**: 框架支持未来新增skills
- **统一性**: 所有skills使用统一的处理方式
- **性能优先**: 优化必须带来可测量的性能提升
- **向后兼容**: 保持与现有代码的兼容性

### 1.3 架构概览
```
┌─────────────────────────────────────────────────────────┐
│                    Skills Layer (56个)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│
│  │ Skill 1  │  │ Skill 2  │  │ Skill 3  │  │  ...     ││
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘│
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                  Framework Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ 性能优化框架  │  │ 边界处理框架  │  │ 输出格式框架  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ 错误处理框架  │  │ 测试框架     │  │ 文档生成工具  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   Data Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ AKShare      │  │ Cache        │  │ Health Check │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 2. 核心组件设计

### 2.1 性能优化框架

#### 2.1.1 缓存管理器 (CacheManager)

**职责**: 统一管理数据缓存，支持内存缓存和文件缓存

**接口设计**:
```python
class CacheManager:
    def get(self, key: str, ttl: int = 300) -> Optional[Any]
    def set(self, key: str, value: Any, ttl: int = 300) -> None
    def invalidate(self, pattern: str) -> None
    def get_stats(self) -> CacheStats
```

**缓存策略**:
- L1缓存: 内存缓存（LRU，最大1000条）
- L2缓存: 文件缓存（Parquet格式，最大10GB）
- TTL: 默认5分钟，可配置
- 缓存键格式: `{skill_name}:{view_name}:{params_hash}`

**性能目标**:
- 缓存命中率 > 80%
- 缓存查询延迟 < 10ms
- 内存占用 < 500MB

#### 2.1.2 增量计算引擎 (IncrementalEngine)

**职责**: 支持增量计算，避免重复计算全量数据

**接口设计**:
```python
class IncrementalEngine:
    def compute_delta(self, old_data: DataFrame, new_data: DataFrame) -> DataFrame
    def merge_results(self, old_result: Any, delta_result: Any) -> Any
    def should_use_incremental(self, data_size: int) -> bool
```

**增量策略**:
- 数据量 < 1000条: 全量计算
- 数据量 >= 1000条: 增量计算
- 增量阈值: 新增数据 < 10%时使用增量

#### 2.1.3 并行处理器 (ParallelProcessor)

**职责**: 支持多进程/多线程并行处理

**接口设计**:
```python
class ParallelProcessor:
    def map(self, func: Callable, data: List[Any], workers: int = 4) -> List[Any]
    def batch_process(self, func: Callable, batches: List[Any]) -> List[Any]
```

**并行策略**:
- CPU密集型: 使用多进程（ProcessPoolExecutor）
- IO密集型: 使用多线程（ThreadPoolExecutor）
- 默认worker数: CPU核心数 - 1
- 批次大小: 自动根据数据量调整

### 2.2 边界条件处理框架

#### 2.2.1 涨跌停检测器 (LimitDetector)

**职责**: 统一检测和处理涨跌停数据

**接口设计**:
```python
class LimitDetector:
    def detect_limit_up(self, df: DataFrame) -> DataFrame
    def detect_limit_down(self, df: DataFrame) -> DataFrame
    def filter_limit_stocks(self, df: DataFrame, include: bool = False) -> DataFrame
    def add_limit_flags(self, df: DataFrame) -> DataFrame
```

**检测规则**:
- 主板/中小板: 涨跌幅 >= ±9.9%
- 创业板/科创板: 涨跌幅 >= ±19.9%
- ST股票: 涨跌幅 >= ±4.9%
- 新股首日: 涨跌幅 >= ±43.9%（创业板/科创板）

**处理策略**:
- 默认: 标注但不过滤
- 可配置: 完全过滤涨跌停股票
- 输出: 添加 `is_limit_up`, `is_limit_down` 字段

#### 2.2.2 停牌检测器 (SuspensionDetector)

**职责**: 统一检测和处理停牌数据

**接口设计**:
```python
class SuspensionDetector:
    def detect_suspension(self, df: DataFrame) -> DataFrame
    def fill_suspension_data(self, df: DataFrame, method: str = 'ffill') -> DataFrame
    def add_suspension_flags(self, df: DataFrame) -> DataFrame
```

**检测规则**:
- 成交量 = 0 且 成交额 = 0
- 涨跌幅 = 0 且 换手率 = 0
- 查询停牌公告数据（如果可用）

**处理策略**:
- 前值填充 (ffill): 使用最近一个交易日的数据
- 标注: 添加 `is_suspended` 字段
- 警告: 停牌超过5天时输出警告

#### 2.2.3 数据质量评估器 (DataQualityAssessor)

**职责**: 评估数据完整性和质量

**接口设计**:
```python
class DataQualityAssessor:
    def assess(self, df: DataFrame) -> QualityReport
    def get_completeness_score(self, df: DataFrame) -> float
    def get_missing_fields(self, df: DataFrame) -> List[str]
    def should_proceed(self, quality_score: float, threshold: float = 0.8) -> bool
```

**评估指标**:
- 完整性: 非空字段比例
- 一致性: 数据范围和类型检查
- 时效性: 数据更新时间
- 质量评分: 0-100分

**质量阈值**:
- >= 90分: 优秀，正常处理
- 70-90分: 良好，添加警告
- 50-70分: 一般，降级处理
- < 50分: 差，返回错误

### 2.3 输出格式框架

#### 2.3.1 输出格式标准 (OutputSchema)

**统一JSON Schema**:
```json
{
  "metadata": {
    "skill_name": "string",
    "view_name": "string",
    "timestamp": "ISO8601",
    "data_quality_score": "float",
    "execution_time_ms": "int"
  },
  "data": {
    "summary": {
      "total_count": "int",
      "key_metrics": {}
    },
    "items": [],
    "pagination": {
      "page": "int",
      "page_size": "int",
      "total_pages": "int"
    }
  },
  "warnings": [],
  "visualization_hints": {
    "chart_type": "string",
    "x_axis": "string",
    "y_axis": "string"
  }
}
```

#### 2.3.2 输出格式化器 (OutputFormatter)

**职责**: 统一格式化输出数据

**接口设计**:
```python
class OutputFormatter:
    def format(self, data: Any, schema: OutputSchema) -> Dict
    def add_metadata(self, output: Dict, metadata: Dict) -> Dict
    def add_visualization_hints(self, output: Dict, hints: Dict) -> Dict
    def validate(self, output: Dict) -> bool
```

### 2.4 错误处理框架

#### 2.4.1 错误码定义

**错误码格式**: `{类别}{编号}` (例如: D001, P001, S001)

**错误类别**:
- D (Data): 数据相关错误 (D001-D099)
- P (Parameter): 参数相关错误 (P001-P099)
- S (System): 系统相关错误 (S001-S099)
- A (AKShare): AKShare接口错误 (A001-A099)

**常见错误码**:
```python
ERROR_CODES = {
    'D001': '数据缺失',
    'D002': '数据质量不足',
    'D003': '数据格式错误',
    'P001': '参数缺失',
    'P002': '参数格式错误',
    'P003': '参数超出范围',
    'S001': '系统超时',
    'S002': '内存不足',
    'A001': 'AKShare接口失败',
    'A002': 'AKShare数据为空',
}
```

#### 2.4.2 错误处理器 (ErrorHandler)

**接口设计**:
```python
class ErrorHandler:
    def handle(self, error: Exception) -> ErrorResponse
    def format_error_message(self, error_code: str, details: Dict) -> str
    def get_suggestions(self, error_code: str) -> List[str]
```

**错误响应格式**:
```json
{
  "error_code": "D001",
  "error_message": "数据缺失：缺少必需字段 '股票代码'",
  "details": {
    "missing_fields": ["股票代码"],
    "data_source": "stock_zh_a_hist"
  },
  "suggestions": [
    "检查日期参数是否正确",
    "确认该日期是否为交易日",
    "查看FAQ: https://..."
  ],
  "faq_link": "https://..."
}
```

### 2.5 测试框架

#### 2.5.1 单元测试模板

**测试结构**:
```python
class TestSkillName:
    def setup_method(self):
        # 初始化测试数据
        pass
    
    def test_normal_case(self):
        # 测试正常情况
        pass
    
    def test_edge_case(self):
        # 测试边界情况
        pass
    
    def test_error_case(self):
        # 测试异常情况
        pass
```

**Mock数据生成器**:
```python
class MockDataGenerator:
    def generate_stock_data(self, count: int = 100) -> DataFrame
    def generate_limit_up_data(self, count: int = 10) -> DataFrame
    def generate_suspended_data(self, count: int = 5) -> DataFrame
```

#### 2.5.2 集成测试框架

**测试流程**:
1. 准备测试数据
2. 调用skill的view
3. 验证输出格式
4. 验证数据正确性
5. 验证性能指标

**性能基准**:
- 响应时间 < 5秒（全市场分析）
- 响应时间 < 1秒（单股分析）
- 内存占用 < 1GB
- CPU使用率 < 80%

## 3. 数据流设计

### 3.1 性能优化数据流

```
用户请求
  ↓
检查缓存 → 命中 → 返回缓存结果
  ↓ 未命中
判断是否增量计算
  ↓ 是
获取增量数据 → 增量计算 → 合并结果
  ↓ 否
获取全量数据 → 判断是否并行
  ↓ 是
分批并行处理 → 合并结果
  ↓ 否
串行处理
  ↓
缓存结果
  ↓
返回结果
```

### 3.2 边界条件处理数据流

```
原始数据
  ↓
数据质量评估 → 质量不足 → 返回错误
  ↓ 质量合格
涨跌停检测 → 添加标识
  ↓
停牌检测 → 添加标识 → 前值填充
  ↓
数据缺失处理 → 填充/删除
  ↓
处理后数据
```

### 3.3 输出格式化数据流

```
处理结果
  ↓
添加元数据（时间戳、质量评分等）
  ↓
添加摘要信息（总数、关键指标）
  ↓
添加可视化提示
  ↓
格式验证
  ↓
输出JSON
```

## 4. 详细设计

### 4.1 P2-5: 全市场分析性能优化

**目标skills**:
- quant-factor-screener
- factor-crowding-monitor
- market-breadth-monitor
- small-cap-growth-identifier
- undervalued-stock-screener

**优化方案**:

1. **数据获取优化**
   - 使用缓存避免重复获取
   - 批量获取替代单个获取
   - 异步获取多个数据源

2. **计算优化**
   - 向量化计算替代循环
   - 使用NumPy/Pandas优化操作
   - 预计算常用指标

3. **并行处理**
   - 按行业/板块分组并行
   - 每组独立计算
   - 最后合并结果

**实现示例**:
```python
class MarketWideAnalyzer:
    def __init__(self):
        self.cache = CacheManager()
        self.parallel = ParallelProcessor()
    
    def analyze(self, date: str):
        # 1. 检查缓存
        cache_key = f"market_data:{date}"
        data = self.cache.get(cache_key)
        
        if data is None:
            # 2. 获取数据
            data = self._fetch_market_data(date)
            self.cache.set(cache_key, data)
        
        # 3. 分组并行处理
        groups = self._split_by_industry(data)
        results = self.parallel.map(self._analyze_group, groups)
        
        # 4. 合并结果
        return self._merge_results(results)
```

### 4.2 P2-6: 实时监控数据更新优化

**目标skills**:
- intraday-microstructure-analyzer
- hot-rank-sentiment-monitor
- limit-up-pool-analyzer
- event-driven-detector

**优化方案**:

1. **智能刷新机制**
   - 仅在交易时间刷新
   - 根据数据变化频率调整刷新间隔
   - 使用增量更新

2. **数据变化检测**
   - 计算数据哈希值
   - 仅在哈希变化时更新
   - 跳过无变化的数据

3. **资源优化**
   - 限制并发请求数
   - 使用连接池
   - 及时释放资源

**实现示例**:
```python
class RealtimeMonitor:
    def __init__(self):
        self.last_hash = {}
        self.update_interval = 60  # 秒
    
    def should_update(self, key: str, data: Any) -> bool:
        current_hash = hash(str(data))
        last_hash = self.last_hash.get(key)
        
        if last_hash != current_hash:
            self.last_hash[key] = current_hash
            return True
        return False
    
    def adaptive_interval(self, change_rate: float):
        # 根据变化率调整刷新间隔
        if change_rate > 0.5:
            self.update_interval = 30
        elif change_rate > 0.2:
            self.update_interval = 60
        else:
            self.update_interval = 120
```

### 4.3 P2-8/9/10: 边界条件处理

**统一处理流程**:

1. **数据预处理**
   ```python
   def preprocess_data(df: DataFrame) -> DataFrame:
       # 1. 涨跌停检测
       df = LimitDetector().add_limit_flags(df)
       
       # 2. 停牌检测
       df = SuspensionDetector().add_suspension_flags(df)
       
       # 3. 数据质量评估
       quality = DataQualityAssessor().assess(df)
       
       if quality.score < 50:
           raise DataQualityError(f"数据质量不足: {quality.score}")
       
       # 4. 数据缺失处理
       df = handle_missing_data(df)
       
       return df
   ```

2. **配置化处理策略**
   ```python
   BOUNDARY_CONFIG = {
       'limit_up_down': {
           'detect': True,
           'filter': False,  # 不过滤，仅标注
           'add_warning': True
       },
       'suspension': {
           'detect': True,
           'fill_method': 'ffill',
           'max_days': 5
       },
       'missing_data': {
           'threshold': 0.8,  # 80%完整性
           'fill_method': 'ffill',
           'drop_if_critical': True
       }
   }
   ```

### 4.4 P3-11/12: 用户体验优化

**输出格式统一**:

所有skills的输出遵循统一schema，包含：
- metadata: 元数据（skill名称、时间戳、质量评分等）
- data: 实际数据（summary + items）
- warnings: 警告信息
- visualization_hints: 可视化建议

**错误提示优化**:

每个错误包含：
- error_code: 错误码
- error_message: 清晰的错误描述
- details: 详细信息
- suggestions: 可操作的建议
- faq_link: FAQ链接

### 4.5 P3-13/14: 文档完善

**示例文档结构**:

每个skill的SKILL.md添加：

1. **使用示例** (3-5个)
   - 基础用法
   - 高级用法
   - 边界情况

2. **FAQ** (5-10个)
   - 常见错误
   - 参数说明
   - 结果解读

3. **可视化建议**
   - 推荐图表类型
   - 数据字段映射
   - 示例代码

**文档生成工具**:
```python
class DocGenerator:
    def generate_examples(self, skill_name: str) -> str
    def generate_faq(self, skill_name: str) -> str
    def generate_viz_guide(self, skill_name: str) -> str
```

### 4.6 P3-15/16: 测试覆盖

**测试策略**:

1. **单元测试**
   - 每个核心函数都有测试
   - 覆盖正常、边界、异常情况
   - 使用mock数据

2. **集成测试**
   - 端到端测试每个view
   - 使用真实数据或高质量mock
   - 验证输出格式和性能

3. **性能测试**
   - 测试响应时间
   - 测试资源占用
   - 测试并发能力

**测试覆盖率目标**: > 80%

## 5. 实施计划

### 5.1 第1周: P2-5 全市场分析性能优化

**任务**:
1. 实现CacheManager
2. 实现ParallelProcessor
3. 优化5个skills
4. 性能测试和验证

**交付物**:
- `view-service/performance/cache_manager.py`
- `view-service/performance/parallel_processor.py`
- 优化后的5个skills
- 性能测试报告

### 5.2 第2周: P2-6 实时监控优化

**任务**:
1. 实现智能刷新机制
2. 实现数据变化检测
3. 优化4个skills
4. 资源使用测试

**交付物**:
- `view-service/performance/realtime_monitor.py`
- 优化后的4个skills
- 资源使用测试报告

### 5.3 第3-4周: P2-8/9/10 边界条件处理

**任务**:
1. 实现LimitDetector
2. 实现SuspensionDetector
3. 实现DataQualityAssessor
4. 应用到所有56个skills
5. 集成测试

**交付物**:
- `view-service/boundary/limit_detector.py`
- `view-service/boundary/suspension_detector.py`
- `view-service/boundary/data_quality_assessor.py`
- 更新后的56个skills
- 边界条件测试报告

### 5.4 第5周: P3-11/12 用户体验优化

**任务**:
1. 定义统一OutputSchema
2. 实现OutputFormatter
3. 实现ErrorHandler
4. 应用到所有56个skills

**交付物**:
- `view-service/output/output_schema.py`
- `view-service/output/output_formatter.py`
- `view-service/error/error_handler.py`
- 更新后的56个skills

### 5.5 第6周: P3-13/14 文档完善

**任务**:
1. 实现DocGenerator
2. 为所有56个skills生成示例
3. 为所有56个skills生成FAQ
4. 为20个skills添加可视化建议

**交付物**:
- `tools/doc_generator.py`
- 更新后的56个SKILL.md
- 可视化指南文档

### 5.6 第7-8周: P3-15/16 测试覆盖

**任务**:
1. 实现MockDataGenerator
2. 为所有56个skills添加单元测试
3. 为所有56个skills添加集成测试
4. 生成测试覆盖率报告

**交付物**:
- `tests/mock_data_generator.py`
- `tests/unit/test_*.py` (56个)
- `tests/integration/test_*.py` (56个)
- 测试覆盖率报告

## 6. 验收标准

### 6.1 性能指标

| 指标 | 目标 | 验证方法 |
|------|------|----------|
| 全市场分析响应时间 | < 5秒 | 性能测试 |
| 单股分析响应时间 | < 1秒 | 性能测试 |
| 缓存命中率 | > 80% | 缓存统计 |
| 内存占用 | < 1GB | 资源监控 |
| CPU使用率 | < 80% | 资源监控 |

### 6.2 质量指标

| 指标 | 目标 | 验证方法 |
|------|------|----------|
| 测试覆盖率 | > 80% | pytest-cov |
| 代码复杂度 | < 10 | radon |
| 文档完整性 | 100% | 人工检查 |
| 输出格式一致性 | 100% | Schema验证 |

### 6.3 功能指标

| 指标 | 目标 | 验证方法 |
|------|------|----------|
| 涨跌停检测准确率 | > 99% | 单元测试 |
| 停牌检测准确率 | > 99% | 单元测试 |
| 数据质量评估准确率 | > 95% | 集成测试 |
| 错误提示清晰度 | 100% | 人工检查 |

## 7. 风险和缓解

### 7.1 性能优化风险

**风险**: 优化可能引入新的bug

**缓解措施**:
- 充分的单元测试和集成测试
- 渐进式优化，每次优化后验证
- 保留回滚方案

### 7.2 兼容性风险

**风险**: 修改可能影响现有功能

**缓解措施**:
- 保持接口向后兼容
- 使用配置开关控制新功能
- 完整的回归测试

### 7.3 时间风险

**风险**: 工作量可能超出预期

**缓解措施**:
- 分批实施，优先核心功能
- 每周review进度
- 必要时调整范围

## 8. 技术栈

- **语言**: Python 3.8+
- **数据处理**: Pandas, NumPy
- **缓存**: Redis (可选), 文件缓存
- **并行处理**: concurrent.futures
- **测试**: pytest, pytest-cov, pytest-mock
- **文档**: Markdown
- **代码质量**: black, flake8, mypy, radon

## 9. 参考资料

- 现有代码: `view-service/`
- 健康检查机制: `view-service/AKSHARE_HEALTH_CHECK.md`
- 回测框架: `view-service/backtest_framework.py`
- 问题列表: `docs/待修复问题优先级列表.md`
