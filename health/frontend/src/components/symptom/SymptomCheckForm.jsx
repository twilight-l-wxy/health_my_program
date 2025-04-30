import React, { useState } from 'react';
import { Form, Input, Button, Steps, Card, Radio, Spin, Result, Typography, Space, Tag } from 'antd';
import { MedicineBoxOutlined, QuestionCircleOutlined, CheckCircleOutlined, LoadingOutlined } from '@ant-design/icons';
import { useDispatch, useSelector } from 'react-redux';

const { TextArea } = Input;
const { Step } = Steps;
const { Title, Paragraph, Text } = Typography;

// 模拟API调用
const mockSubmitSymptom = (data) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        consultation_id: 1,
        next_question: '您的症状持续了多长时间？'
      });
    }, 1000);
  });
};

const mockSubmitAnswer = (data) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      if (data.currentStep < 4) {
        resolve({
          next_question: data.currentStep === 1 ? '您是否有发热症状？' :
                         data.currentStep === 2 ? '您是否有头痛症状？' :
                         '您是否有其他不适？',
          is_last: data.currentStep === 3
        });
      } else {
        resolve({
          is_last: true
        });
      }
    }, 1000);
  });
};

const mockGetResult = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        possible_diseases: [
          {
            name: '普通感冒',
            probability: 0.75,
            description: '普通感冒是一种常见的上呼吸道感染，通常由病毒引起。'
          },
          {
            name: '流行性感冒',
            probability: 0.25,
            description: '流行性感冒是由流感病毒引起的急性呼吸道传染病。'
          }
        ],
        risk_level: '低',
        recommended_department: '呼吸内科',
        advice: '建议多休息，多喝水，如症状加重请及时就医。'
      });
    }, 1500);
  });
};

const SymptomCheckForm = () => {
  const [form] = Form.useForm();
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [consultationId, setConsultationId] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [result, setResult] = useState(null);
  const [answers, setAnswers] = useState([]);

  const handleInitialSubmit = async (values) => {
    setLoading(true);
    try {
      const response = await mockSubmitSymptom(values);
      setConsultationId(response.consultation_id);
      setCurrentQuestion(response.next_question);
      setCurrentStep(1);
    } catch (error) {
      console.error('提交症状失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSubmit = async (values) => {
    setLoading(true);
    const answer = values.answer;
    setAnswers([...answers, { question: currentQuestion, answer }]);
    
    try {
      const response = await mockSubmitAnswer({ answer, consultationId, currentStep });
      
      if (response.is_last) {
        const resultData = await mockGetResult(consultationId);
        setResult(resultData);
        setCurrentStep(5); // 结果步骤
      } else {
        setCurrentQuestion(response.next_question);
        setCurrentStep(currentStep + 1);
      }
    } catch (error) {
      console.error('提交回答失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 0: // 初始症状描述
        return (
          <Form form={form} onFinish={handleInitialSubmit} layout="vertical">
            <Form.Item
              name="chief_complaint"
              label="主要症状"
              rules={[{ required: true, message: '请输入您的主要症状' }]}
            >
              <Input placeholder="例如：头痛、发热、咳嗽等" />
            </Form.Item>
            <Form.Item
              name="symptom_description"
              label="症状描述"
              rules={[{ required: true, message: '请详细描述您的症状' }]}
            >
              <TextArea
                placeholder="请详细描述您的症状，包括：症状表现、持续时间、是否有其他不适等"
                autoSize={{ minRows: 3, maxRows: 6 }}
              />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" loading={loading}>
                开始自查
              </Button>
            </Form.Item>
          </Form>
        );
      case 1: // 问诊问题1
      case 2: // 问诊问题2
      case 3: // 问诊问题3
      case 4: // 问诊问题4
        return (
          <Form form={form} onFinish={handleAnswerSubmit} layout="vertical">
            <Form.Item
              name="answer"
              label={currentQuestion}
              rules={[{ required: true, message: '请回答此问题' }]}
            >
              <Radio.Group>
                <Space direction="vertical">
                  <Radio value="是">是</Radio>
                  <Radio value="否">否</Radio>
                  <Radio value="不确定">不确定</Radio>
                </Space>
              </Radio.Group>
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" loading={loading}>
                下一步
              </Button>
            </Form.Item>
          </Form>
        );
      case 5: // 结果
        return result ? (
          <Result
            status="success"
            title="自查完成"
            subTitle="以下是基于您提供的症状信息生成的初步分析结果"
          >
            <div className="result-content" style={{ textAlign: 'left', marginTop: '20px' }}>
              <Card title="可能的疾病" style={{ marginBottom: '20px' }}>
                {result.possible_diseases.map((disease, index) => (
                  <Card.Grid key={index} style={{ width: '100%' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Text strong>{disease.name}</Text>
                      <Tag color={disease.probability > 0.5 ? 'orange' : 'blue'}>
                        匹配度: {Math.round(disease.probability * 100)}%
                      </Tag>
                    </div>
                    <Paragraph type="secondary">{disease.description}</Paragraph>
                  </Card.Grid>
                ))}
              </Card>
              
              <Card title="风险评估与建议" style={{ marginBottom: '20px' }}>
                <Paragraph>
                  <Text strong>风险等级：</Text>
                  <Tag color={result.risk_level === '低' ? 'green' : result.risk_level === '中' ? 'orange' : 'red'}>
                    {result.risk_level}
                  </Tag>
                </Paragraph>
                <Paragraph>
                  <Text strong>推荐就诊科室：</Text> {result.recommended_department}
                </Paragraph>
                <Paragraph>
                  <Text strong>医疗建议：</Text>
                </Paragraph>
                <Paragraph>{result.advice}</Paragraph>
              </Card>
              
              <div style={{ textAlign: 'center' }}>
                <Paragraph type="secondary">
                  注意：本结果仅供参考，不构成医疗诊断。如有不适，请及时就医。
                </Paragraph>
                <Button type="primary" onClick={() => {
                  setCurrentStep(0);
                  setResult(null);
                  setAnswers([]);
                  setConsultationId(null);
                  setCurrentQuestion('');
                  form.resetFields();
                }}>
                  重新自查
                </Button>
              </div>
            </div>
          </Result>
        ) : (
          <div style={{ textAlign: 'center', padding: '50px' }}>
            <Spin indicator={<LoadingOutlined style={{ fontSize: 24 }} spin />} />
            <p style={{ marginTop: '20px' }}>正在生成分析结果...</p>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="symptom-check-container">
      <Card>
        <Steps current={currentStep} style={{ marginBottom: '30px' }}>
          <Step title="症状描述" icon={<MedicineBoxOutlined />} />
          <Step title="问诊问题" icon={<QuestionCircleOutlined />} />
          <Step title="问诊问题" icon={<QuestionCircleOutlined />} />
          <Step title="问诊问题" icon={<QuestionCircleOutlined />} />
          <Step title="问诊问题" icon={<QuestionCircleOutlined />} />
          <Step title="分析结果" icon={<CheckCircleOutlined />} />
        </Steps>
        
        <div className="step-content">
          {renderStepContent()}
        </div>
        
        {currentStep > 0 && currentStep < 5 && (
          <div style={{ marginTop: '20px' }}>
            <Title level={5}>已回答的问题：</Title>
            {answers.map((item, index) => (
              <div key={index} style={{ marginBottom: '10px' }}>
                <Text type="secondary">问题 {index + 1}：{item.question}</Text>
                <br />
                <Text>回答：{item.answer}</Text>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
};

export default SymptomCheckForm;