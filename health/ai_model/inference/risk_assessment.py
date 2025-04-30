# 风险评估模块

import os
import json
import numpy as np
from collections import defaultdict

class RiskAssessor:
    """风险评估类，用于计算疾病概率和风险等级"""
    
    def __init__(self):
        """初始化风险评估器"""
        # 加载疾病数据库
        self.diseases = self._load_diseases()
        # 加载风险阈值
        self.risk_thresholds = {
            "low": 0.3,  # 低风险阈值
            "medium": 0.6  # 中风险阈值，高于此为高风险
        }
        print(f"风险评估模型初始化完成，已加载{len(self.diseases)}种疾病数据")
    
    def _load_diseases(self):
        """加载疾病数据库"""
        # 实际项目中应该从数据库中加载
        # 此处为演示，返回一个简单的字典
        return {
            "普通感冒": {
                "symptoms": {
                    "发热": 0.7,
                    "咳嗽": 0.8,
                    "流涕": 0.9,
                    "喉咙痛": 0.7,
                    "头痛": 0.5
                },
                "department": "呼吸内科",
                "description": "普通感冒是一种常见的上呼吸道感染，通常由病毒引起。",
                "treatment": "多休息，多喝水，可服用对症药物缓解症状。"
            },
            "流行性感冒": {
                "symptoms": {
                    "发热": 0.9,
                    "咳嗽": 0.7,
                    "肌肉酸痛": 0.8,
                    "乏力": 0.8,
                    "头痛": 0.7
                },
                "department": "呼吸内科",
                "description": "流行性感冒是由流感病毒引起的急性呼吸道传染病。",
                "treatment": "充分休息，多饮水，必要时在医生指导下服用抗病毒药物。"
            },
            "偏头痛": {
                "symptoms": {
                    "头痛": 0.95,
                    "恶心": 0.6,
                    "视觉障碍": 0.4,
                    "怕光": 0.5,
                    "怕声": 0.5
                },
                "department": "神经内科",
                "description": "偏头痛是一种常见的神经血管性疾病，特点是反复发作的中重度、搏动性头痛。",
                "treatment": "避免诱因，保持规律作息，必要时服用止痛药或预防性药物。"
            },
            "胃炎": {
                "symptoms": {
                    "腹痛": 0.8,
                    "恶心": 0.7,
                    "呕吐": 0.6,
                    "食欲不振": 0.7,
                    "腹胀": 0.6
                },
                "department": "消化内科",
                "description": "胃炎是胃黏膜的炎症，可由多种因素引起，如幽门螺杆菌感染、药物、压力等。",
                "treatment": "规律饮食，避免刺激性食物，必要时服用抑酸药或抗生素。"
            },
            "支气管炎": {
                "symptoms": {
                    "咳嗽": 0.9,
                    "咳痰": 0.8,
                    "胸闷": 0.6,
                    "气短": 0.5,
                    "发热": 0.4
                },
                "department": "呼吸内科",
                "description": "支气管炎是支气管黏膜的炎症，可由感染或刺激物引起。",
                "treatment": "保持呼吸道湿润，必要时使用祛痰药或抗生素。"
            }
        }
    
    def assess(self, symptoms, patient_info=None):
        """评估疾病风险
        
        Args:
            symptoms: 症状列表，每个症状包含名称、严重程度等信息
            patient_info: 患者基本信息，如年龄、性别、既往病史等
            
        Returns:
            评估结果，包含可能的疾病、风险等级、建议等
        """
        # 计算每种疾病的概率
        disease_probabilities = self._calculate_disease_probabilities(symptoms, patient_info)
        
        # 获取前三种最可能的疾病
        top_diseases = sorted(disease_probabilities.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # 确定风险等级
        max_probability = top_diseases[0][1] if top_diseases else 0
        if max_probability >= self.risk_thresholds["medium"]:
            risk_level = "高"
        elif max_probability >= self.risk_thresholds["low"]:
            risk_level = "中"
        else:
            risk_level = "低"
        
        # 确定推荐科室（取最可能疾病的科室）
        recommended_department = self.diseases[top_diseases[0][0]]["department"] if top_diseases else "全科"
        
        # 生成建议
        advice = self._generate_advice(top_diseases, risk_level)
        
        # 构建结果
        result = {
            "possible_diseases": [
                {
                    "name": disease,
                    "probability": probability,
                    "description": self.diseases[disease]["description"]
                }
                for disease, probability in top_diseases
            ],
            "risk_level": risk_level,
            "recommended_department": recommended_department,
            "advice": advice
        }
        
        return result
    
    def _calculate_disease_probabilities(self, symptoms, patient_info=None):
        """计算各疾病的概率
        
        使用简化的贝叶斯网络计算疾病概率
        
        Args:
            symptoms: 症状列表
            patient_info: 患者信息
            
        Returns:
            各疾病的概率字典
        """
        # 提取症状名称列表
        symptom_names = [symptom["name"] for symptom in symptoms]
        
        # 计算每种疾病的概率
        disease_scores = {}
        for disease_name, disease_data in self.diseases.items():
            # 初始分数
            score = 0.1  # 基础概率
            
            # 计算症状匹配分数
            matched_symptoms = 0
            for symptom_name, relevance in disease_data["symptoms"].items():
                if symptom_name in symptom_names:
                    # 找到对应症状的严重程度
                    severity = 1.0  # 默认严重程度
                    for symptom in symptoms:
                        if symptom["name"] == symptom_name and "severity" in symptom:
                            severity_map = {"轻微": 0.5, "中度": 1.0, "严重": 1.5}
                            severity = severity_map.get(symptom["severity"], 1.0)
                            break
                    
                    # 计算该症状的贡献分数
                    symptom_score = relevance * severity
                    score += symptom_score
                    matched_symptoms += 1
            
            # 根据匹配的症状数量调整分数
            if matched_symptoms > 0:
                # 计算症状覆盖率
                coverage = matched_symptoms / len(disease_data["symptoms"])
                # 调整分数
                score *= (0.5 + 0.5 * coverage)
            else:
                # 没有匹配的症状，分数降低
                score *= 0.1
            
            # 考虑患者信息（如果有）
            if patient_info:
                # 这里可以根据患者年龄、性别、既往病史等调整分数
                # 简化实现，实际项目中应该有更复杂的逻辑
                pass
            
            disease_scores[disease_name] = score
        
        # 归一化概率
        total_score = sum(disease_scores.values())
        if total_score > 0:
            disease_probabilities = {disease: score/total_score for disease, score in disease_scores.items()}
        else:
            disease_probabilities = {disease: 0 for disease in disease_scores}
        
        return disease_probabilities
    
    def _generate_advice(self, top_diseases, risk_level):
        """生成医疗建议
        
        Args:
            top_diseases: 最可能的疾病列表
            risk_level: 风险等级
            
        Returns:
            医疗建议文本
        """
        if not top_diseases:
            return "未能识别明确的疾病，建议咨询全科医生进行进一步检查。"
        
        # 获取最可能疾病的信息
        top_disease = top_diseases[0][0]
        disease_info = self.diseases[top_disease]
        
        # 根据风险等级生成建议
        if risk_level == "高":
            advice = f"您的症状与{top_disease}高度匹配，建议尽快前往{disease_info['department']}就诊。{disease_info['treatment']}"
        elif risk_level == "中":
            advice = f"您的症状可能与{top_disease}有关，建议近期前往{disease_info['department']}就诊。{disease_info['treatment']}"
        else:
            advice = f"您的症状轻微，可能与{top_disease}有关，建议观察，如症状加重请及时就医。{disease_info['treatment']}"
        
        return advice


# 测试代码
if __name__ == "__main__":
    # 初始化风险评估器
    assessor = RiskAssessor()
    
    # 测试症状
    test_symptoms = [
        {"name": "发热", "severity": "中度"},
        {"name": "咳嗽", "severity": "轻微"},
        {"name": "头痛", "severity": "中度"}
    ]
    
    # 评估风险
    result = assessor.assess(test_symptoms)
    
    # 打印结果
    print("风险评估结果:")
    print(f"风险等级: {result['risk_level']}")
    print(f"推荐科室: {result['recommended_department']}")
    print("可能的疾病:")
    for disease in result['possible_diseases']:
        print(f"- {disease['name']} (概率: {disease['probability']:.2f})")
    print(f"\n医疗建议: {result['advice']}")