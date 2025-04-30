# 症状识别模块

import os
import json
import numpy as np
import torch
import jieba
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class SymptomRecognizer:
    """症状识别类，用于从用户描述中识别症状关键词"""
    
    def __init__(self, model_path=None):
        """初始化症状识别器
        
        Args:
            model_path: 模型路径，如果为None则使用配置中的默认路径
        """
        # 在实际项目中，这里应该加载训练好的模型
        # 此处为演示，使用简化的实现
        self.symptom_keywords = self._load_symptom_keywords()
        self.symptom_synonyms = self._load_symptom_synonyms()
        
        # 模拟模型加载
        self.model_loaded = True
        print(f"症状识别模型初始化完成，已加载{len(self.symptom_keywords)}个症状关键词")
    
    def _load_symptom_keywords(self):
        """加载症状关键词库"""
        # 实际项目中应该从数据库或文件中加载
        # 此处为演示，返回一个简单的字典
        return {
            "头痛": {
                "body_part": "头部",
                "severity_levels": ["轻微", "中度", "严重"],
                "common_causes": ["疲劳", "压力", "偏头痛", "感冒", "鼻窦炎"]
            },
            "发热": {
                "body_part": "全身",
                "severity_levels": ["低烧", "中烧", "高烧"],
                "common_causes": ["感染", "炎症", "感冒", "流感"]
            },
            "咳嗽": {
                "body_part": "呼吸道",
                "severity_levels": ["轻微", "中度", "严重"],
                "common_causes": ["感冒", "过敏", "哮喘", "支气管炎"]
            },
            "腹痛": {
                "body_part": "腹部",
                "severity_levels": ["轻微", "中度", "严重"],
                "common_causes": ["消化不良", "胃炎", "肠炎", "阑尾炎"]
            },
            "恶心": {
                "body_part": "消化系统",
                "severity_levels": ["轻微", "中度", "严重"],
                "common_causes": ["消化不良", "晕动病", "食物中毒", "胃炎"]
            }
        }
    
    def _load_symptom_synonyms(self):
        """加载症状同义词库"""
        # 实际项目中应该从数据库或文件中加载
        # 此处为演示，返回一个简单的字典
        return {
            "头痛": ["头疼", "脑袋疼", "头部疼痛", "颅痛"],
            "发热": ["发烧", "体温升高", "发高烧", "低烧", "中烧", "高烧"],
            "咳嗽": ["咳", "干咳", "湿咳", "久咳", "咳痰"],
            "腹痛": ["肚子疼", "肚痛", "腹部疼痛", "胃痛"],
            "恶心": ["想吐", "反胃", "作呕", "胃部不适"]
        }
    
    def recognize(self, text):
        """从文本中识别症状
        
        Args:
            text: 用户描述的症状文本
            
        Returns:
            识别出的症状列表，每个症状包含名称、置信度等信息
        """
        # 使用jieba分词
        words = jieba.lcut(text)
        
        # 识别症状关键词
        recognized_symptoms = []
        for word in words:
            # 直接匹配关键词
            if word in self.symptom_keywords:
                recognized_symptoms.append({
                    "name": word,
                    "confidence": 0.9,
                    "info": self.symptom_keywords[word]
                })
                continue
            
            # 匹配同义词
            for symptom, synonyms in self.symptom_synonyms.items():
                if word in synonyms:
                    recognized_symptoms.append({
                        "name": symptom,
                        "confidence": 0.8,
                        "info": self.symptom_keywords[symptom]
                    })
                    break
        
        # 去重（可能有同一症状的不同表达）
        unique_symptoms = {}
        for symptom in recognized_symptoms:
            name = symptom["name"]
            if name not in unique_symptoms or symptom["confidence"] > unique_symptoms[name]["confidence"]:
                unique_symptoms[name] = symptom
        
        return list(unique_symptoms.values())


class QuestionGenerator:
    """问题生成类，根据已知症状生成下一个问诊问题"""
    
    def __init__(self):
        """初始化问题生成器"""
        # 加载问题模板
        self.question_templates = self._load_question_templates()
        print("问题生成器初始化完成")
    
    def _load_question_templates(self):
        """加载问题模板"""
        # 实际项目中应该从数据库或文件中加载
        # 此处为演示，返回一个简单的字典
        return {
            "duration": "您的{symptom}持续了多长时间？",
            "severity": "您的{symptom}程度如何？",
            "frequency": "您的{symptom}多久发作一次？",
            "trigger": "有什么因素会加重或缓解您的{symptom}？",
            "associated": "除了{symptom}，您还有其他不适吗？"
        }
    
    def generate_next_question(self, recognized_symptoms, answered_questions):
        """生成下一个问诊问题
        
        Args:
            recognized_symptoms: 已识别的症状列表
            answered_questions: 已回答的问题列表
            
        Returns:
            下一个问题的字典，包含问题文本、类型等信息
        """
        if not recognized_symptoms:
            return {
                "text": "请描述您的症状",
                "type": "open"
            }
        
        # 选择主要症状（置信度最高的）
        main_symptom = max(recognized_symptoms, key=lambda x: x["confidence"])
        
        # 根据已回答的问题选择下一个问题类型
        answered_types = [q["type"] for q in answered_questions]
        
        if "duration" not in answered_types:
            question_type = "duration"
        elif "severity" not in answered_types:
            question_type = "severity"
        elif "frequency" not in answered_types:
            question_type = "frequency"
        elif "trigger" not in answered_types:
            question_type = "trigger"
        else:
            question_type = "associated"
        
        # 生成问题文本
        question_text = self.question_templates[question_type].format(symptom=main_symptom["name"])
        
        # 根据问题类型设置选项
        options = None
        if question_type == "duration":
            options = ["不到24小时", "1-3天", "4-7天", "一周以上", "一个月以上"]
        elif question_type == "severity":
            options = ["轻微", "中度", "严重"]
        elif question_type == "frequency":
            options = ["持续存在", "每天多次", "每天一次", "每周几次", "偶尔发作"]
        
        return {
            "text": question_text,
            "type": question_type,
            "options": options
        }


# 测试代码
if __name__ == "__main__":
    # 初始化症状识别器
    recognizer = SymptomRecognizer()
    
    # 测试症状识别
    test_text = "我最近总是头疼，而且有时候会发烧，感觉很不舒服"
    symptoms = recognizer.recognize(test_text)
    print("识别出的症状:")
    for symptom in symptoms:
        print(f"- {symptom['name']} (置信度: {symptom['confidence']})")
    
    # 初始化问题生成器
    generator = QuestionGenerator()
    
    # 测试问题生成
    next_question = generator.generate_next_question(symptoms, [])
    print(f"\n下一个问题: {next_question['text']}")
    if next_question['options']:
        print("选项:")
        for option in next_question['options']:
            print(f"- {option}")