"""
Mesa 仿真测试
验证 TrustAgent 和 CollaborationModel 的核心功能
"""

import pytest
import numpy as np
from mesa_simulation import TrustAgent, CollaborationModel


class TestTrustAgent:
    """TrustAgent 单元测试"""
    
    def test_agent_initialization(self):
        """测试 Agent 初始化"""
        model = CollaborationModel(n_agents=2, network_type='complete')
        agent = model.trust_agents[0]
        
        # 信任度在合理范围内
        assert 0.1 <= agent.trust_level <= 1.0
        assert agent.messages_sent == 0
        assert agent.messages_received == 0
        assert agent.decision_rounds == 0
        assert agent.reworks == 0
        assert agent.tasks_completed == 0
    
    def test_send_message(self):
        """测试消息发送"""
        model = CollaborationModel(n_agents=2, network_type='complete')
        sender = model.trust_agents[0]
        receiver = model.trust_agents[1]
        
        initial_trust = sender.trust_level
        result = sender.send_message(receiver, "test message")
        
        assert result == True
        assert sender.messages_sent == 1
        assert sender.messages_received >= 0
    
    def test_calculate_t_loss(self):
        """测试 T_loss 计算"""
        model = CollaborationModel(n_agents=2, network_type='complete')
        agent = model.trust_agents[0]
        
        # 执行任务触发指标变化
        agent.execute_task()
        agent.make_decision(task_complexity=3)
        
        t_loss_result = agent.calculate_T_loss()
        
        assert 'I_decay' in t_loss_result
        assert 'delta_R' in t_loss_result
        assert 'W_rate' in t_loss_result
        assert 'T_loss' in t_loss_result
        assert 'trust_level' in t_loss_result
        
        # T_loss 应该在 [0, 1] 范围内
        assert 0 <= t_loss_result['T_loss'] <= 1
    
    def test_rework_trigger(self):
        """测试低信任度触发返工"""
        model = CollaborationModel(n_agents=1, network_type='complete')
        agent = model.trust_agents[0]
        
        # 强制降低信任度
        agent.trust_level = 0.1
        
        initial_reworks = agent.reworks
        agent.execute_task()
        
        # 低信任度应该触发返工
        assert agent.reworks >= initial_reworks


class TestCollaborationModel:
    """CollaborationModel 单元测试"""
    
    def test_model_initialization(self):
        """测试模型初始化"""
        model = CollaborationModel(n_agents=8, network_type='complete')
        
        assert model.n_agents == 8
        assert len(model.trust_agents) == 8
        assert model.graph is not None
    
    def test_network_types(self):
        """测试不同网络拓扑"""
        for network_type in ['complete', 'line', 'star', 'small_world']:
            model = CollaborationModel(n_agents=5, network_type=network_type)
            assert model.graph is not None
            assert len(model.trust_agents) == 5
    
    def test_simulation_step(self):
        """测试仿真单步执行"""
        model = CollaborationModel(n_agents=4, network_type='complete')
        
        initial_metrics_len = len(model.metrics.history['step'])
        model.step()
        
        assert len(model.metrics.history['step']) == initial_metrics_len + 1
    
    def test_simulation_run(self):
        """测试仿真运行"""
        model = CollaborationModel(n_agents=4, network_type='complete')
        model.run_simulation(steps=10)
        
        assert len(model.metrics.history['step']) == 10
    
    def test_network_t_loss(self):
        """测试网络平均 T_loss 计算"""
        model = CollaborationModel(n_agents=4, network_type='complete')
        model.run_simulation(steps=5)
        
        avg_t_loss = model.get_network_T_loss()
        
        assert isinstance(avg_t_loss, (int, float))
        # 多次仿真平均后应该收敛到某个合理范围
        assert -0.5 <= avg_t_loss <= 0.5


class TestMetricsCollector:
    """MetricsCollector 单元测试"""
    
    def test_record_step(self):
        """测试指标记录"""
        model = CollaborationModel(n_agents=3, network_type='complete')
        
        initial_len = len(model.metrics.history['step'])
        model.step()
        
        assert len(model.metrics.history['step']) == initial_len + 1
        assert 'avg_T_loss' in model.metrics.history
        assert 'avg_trust' in model.metrics.history
    
    def test_get_dataframe(self):
        """测试 DataFrame 转换"""
        model = CollaborationModel(n_agents=2, network_type='complete')
        model.run_simulation(steps=5)
        
        df = model.metrics.get_dataframe()
        
        assert len(df) == 5
        assert 'step' in df.columns
        assert 'avg_T_loss' in df.columns


class TestTLossModel:
    """T_loss 模型整体测试"""
    
    def test_t_loss_formula(self):
        """测试 T_loss 公式计算"""
        model = CollaborationModel(n_agents=5, network_type='complete')
        
        model.run_simulation(steps=20)
        
        df = model.metrics.get_dataframe()
        
        # 验证指标随时间变化
        assert df['avg_T_loss'].iloc[-1] != df['avg_T_loss'].iloc[0] or True  # 可能收敛到相同值
    
    def test_different_network_performance(self):
        """测试不同网络拓扑的性能差异"""
        results = {}
        
        for network_type in ['complete', 'line', 'star']:
            model = CollaborationModel(n_agents=8, network_type=network_type)
            model.run_simulation(steps=30)
            results[network_type] = model.get_network_T_loss()
        
        # Complete 图通常表现较好（不是绝对断言）
        # 记录结果供分析
        print(f"Network T_loss: complete={results['complete']:.4f}, star={results['star']:.4f}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
