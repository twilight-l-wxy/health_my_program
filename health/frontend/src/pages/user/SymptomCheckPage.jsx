import React from 'react';
import { Typography, Divider, Alert, Card, Row, Col } from 'antd';
import SymptomCheckForm from '../../components/symptom/SymptomCheckForm';

const { Title, Paragraph } = Typography;

const SymptomCheckPage = () => {
  return (
    <div className="symptom-check-page">
      <Typography>
        <Title level={2}>症状自查</Title>
        <Paragraph>
          智医通症状自查系统基于人工智能技术，通过分析您描述的症状，提供初步的健康评估和就医建议。
          请尽可能详细地描述您的症状，以获得更准确的分析结果。
        </Paragraph>
        
        <Alert
          message="免责声明"
          description="本系统提供的分析结果仅供参考，不构成医疗诊断。如有不适，请及时就医。"
          type="warning"
          showIcon
          style={{ marginBottom: '20px' }}
        />
      </Typography>
      
      <Divider />
      
      <Row gutter={[24, 24]}>
        <Col xs={24} lg={16}>
          <SymptomCheckForm />
        </Col>
        
        <Col xs={24} lg={8}>
          <Card title="使用指南" className="guide-card">
            <Paragraph>
              <strong>第1步：</strong> 输入您的主要症状和详细描述
            </Paragraph>
            <Paragraph>
              <strong>第2-5步：</strong> 回答系统提出的问题，这些问题将帮助系统更准确地理解您的健康状况
            </Paragraph>
            <Paragraph>
              <strong>第6步：</strong> 查看分析结果，包括可能的疾病、风险评估和就医建议
            </Paragraph>
          </Card>
          
          <Card title="注意事项" className="notice-card" style={{ marginTop: '20px' }}>
            <Paragraph>
              • 如遇紧急情况，请立即拨打急救电话或前往最近的医院就诊
            </Paragraph>
            <Paragraph>
              • 系统可能需要您提供更多信息，请耐心回答所有问题
            </Paragraph>
            <Paragraph>
              • 您的健康数据将被严格保密，仅用于提供更准确的分析结果
            </Paragraph>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default SymptomCheckPage;